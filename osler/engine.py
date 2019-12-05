#!/usr/bin/env python

import logging
log = logging.getLogger(__name__)

from collections import Counter
from numpy import matrix, zeros, delete, argwhere, reshape, array_equal, concatenate
from copy import copy

from osler.graph import Node, OslerTree
from osler.criterion import Criterion

class Matrix(object):
    
    def __init__(self, issue):
        self.progenitor = Node(issue)
        self.node = self.progenitor
        self.candidatelist = list(issue.candidates)
        assertions = set()
        criteria = set()
        for d in self.candidatelist:
            assertions.update(d.assertions)
            criteria.update(d.criteria)
        self.assertionlist = list(assertions)
        self.criterionlist = list(criteria)

        # Column = Assertion
        # Row = Diagnosis
        matrix = zeros((len(self.candidatelist), len(self.assertionlist)))
        for i in range(len(self.candidatelist)):
            for j in range(len(self.assertionlist)):
                for c in list(self.candidatelist[i].criteria):
                    if c.assertion == self.assertionlist[j]:
                        if c.truth_value:
                            matrix[i, j] = 1
                        else:
                            matrix[i, j] = 2
        self.matrix = matrix
        self.tree = OslerTree(issue.name, self.node)

    def print_matrix(self):
        print("{{Matrix is ({} diagnoses by {} assertions)".format(len(self.candidatelist), len(self.assertionlist)))
        print(self.assertionlist)
        for i in range(len(self.matrix)):
            print(str(self.matrix[i])+" "+str(self.candidatelist[i]))
        print("}")
    
    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return self.__str__()

    def swap_assertions(self, a, b):
        if a != b:
            self.matrix[:,[a, b]] = self.matrix[:,[b, a]]
            self.assertionlist[a], self.assertionlist[b] = self.assertionlist[b], self.assertionlist[a]

    def swap_diagnoses(self, a, b):
        if a != b:
            self.matrix[[a, b],:] = self.matrix[[b, a],:]
            self.candidatelist[a], self.candidatelist[b] = self.candidatelist[b], self.candidatelist[a]

    def move_assertion_to_first_position(self, a):
        if a > 0:
            column_ids = [i for i in range(len(self.matrix[0,:]))]
            column_ids.remove(a)
            column_ids.insert(0, a)
            self.matrix = self.matrix[:,column_ids]
            self.assertionlist = self.assertionlist[column_ids]

    def sort_diagnoses_by_assertion_truth_value(self):
        arg_sort = self.matrix[:,0].argsort()
        self.matrix = self.matrix[arg_sort]
        self.candidatelist = [self.candidatelist[i] for i in arg_sort]
    
    def sort_matrix_by_assertions(self):
        arg_sort = self.matrix[0,:].argsort()
        self.matrix = self.matrix[:,arg_sort]
        self.assrtionlist = [self.assertionlist[i] for i in arg_sort]

    def delete_assertion(self, a):
        self.matrix = delete(self.matrix, a, 1)
        self.assertionlist = delete(self.assertionlist, a)

    def clear_irrelevant_assertions(self):
        # Delete any assertions in the matrix that have no diagnostic value
        # e.g. assertion is true for every potential diagnosis
        dellist = []
        for i in range(len(self.matrix[0,:])):
            truth_set = set(self.matrix[:,i])
            if len(truth_set) <= 1:
                dellist.append(i)
            elif 0 in truth_set and len(truth_set) == 2:
                dellist.append(i)
        self.delete_assertion(dellist)
    
    def calculate_selection_measure_of_column(self, a, method="halving"):
        num_diagnoses = len(self.matrix[0,:])
        if method == "halving":
            count = Counter(self.matrix[:,a])
            return (count[0])**2+(count[1]-num_diagnoses/2.0)**2+(count[1]-num_diagnoses/2.0)**2

    def select_next_assertion(self):
        num_diagnoses = len(self.matrix[0,:])
        measures = [0 for _ in range(num_diagnoses)]
        for i in range(num_diagnoses):
            measures[i] = self.calculate_selection_measure_of_column(i)
            index = measures.index(min(measures))
        return index

    def split_by_truth_value(self):
        # For the assertion in position 0, split the matrix instance into 3 smaller matrix objects....
        # One for assertion = True, one for False, and one for N/A
        index_null = reshape(argwhere(self.matrix[:,0]==0),-1)
        index_one = reshape(argwhere(self.matrix[:,0]==1),-1)
        index_two = reshape(argwhere(self.matrix[:,0]==2),-1)

        # Creating 3 idntical copies of the current matrix instance
        matrix_null = copy(self)
        matrix_one = copy(self)
        matrix_two = copy(self)

        # For each matrix instance, remove the assertions with the other truth values
        matrix_null.matrix = self.matrix[index_null,:]
        matrix_null.candidatelist = [self.candidatelist[i] for i in index_null]
        matrix_null.projenitor = self.assertionlist[0]
        matrix_one.matrix = self.matrix[index_one,:]
        matrix_one.candidatelist = [self.candidatelist[i] for i in index_one]
        matrix_one.projenitor = self.assertionlist[0]
        matrix_two.matrix = self.matrix[index_two,:]
        matrix_two.candidatelist = [self.candidatelist[i] for i in index_two]
        matrix_two.projenitor = self.assertionlist[0]
        return (matrix_null, matrix_one, matrix_two)

    def combine(self, other):
        # Given two matrix objects with the same assertion lists
        if array_equal(self.assertionlist, other.assertionlist):
            if self.matrix.size > 0 and other.matrix.size > 0:
                self.matrix = concatenate((self.matrix, other.matrix), axis=0)
                self.candidatelist = concatenate((self.candidatelist, other.candidatelist))
            elif self.matrix.size == 0:
                self.matrix = other.matrix.copy()
                self.candidatelist = other.candidatelist.copy()
            elif other.matrix.size == 0:
                pass
        else:
            raise TypeError("matrix mismatch")
        return self

    def construct_tree(self, debug=False):
        
        if debug:
            self.print_matrix()
        
        # Choosing the next assertion
        self.clear_irrelevant_assertions()
        id = self.select_next_assertion()
        #if self.assertionlist[id].cannot_preceed:
        #    if any self.assertionlist.cannot_proceed[id] assertion exists in the list self.assertionlist
        #        id = id_of_self.assertionlist[cannot_proceed item index]
        #    pass
        self.move_assertion_to_first_position(id)
        self.sort_diagnoses_by_assertion_truth_value()
        
        # Linking the next assertion to the progenitor
        progenitor_node = self.assertionlist[0].parent(self.progenitor)
        
        # Splitting the matrix based on truth value
        matrix_null, matrix_one, matrix_two = self.split_by_truth_value()
        
        if debug:
            print("Matrix 0:")
            matrix_null.print_matrix()
            print("Matrix 1:")
            matrix_one.print_matrix()
            print("Matrix 2:")
            matrix_two.print_matrix()
            print("")
        
        # Combining the the "null" matrix into both the ones and zeros matrices, inheriting their respective progenitors
        if len(matrix_null.candidatelist) > 1:
            matrix_one.combine(matrix_null)
            matrix_two.combine(matrix_null)
        
        # Linking the "true" matrix to the assertion and deleting the previous assertion
        if len(matrix_one.candidatelist) > 1:
            criterion_true = Criterion.search(self.assertionlist[0], True, self.criterionlist)
            criterion_true_node = criterion_true.parent(progenitor_node)
            matrix_one.progenitor = criterion_true_node
            matrix_one.delete_assertion(0)
            matrix_one.construct_tree(debug)
        elif len(matrix_one.candidatelist) == 1:
            criterion_true = Criterion.search(self.assertionlist[0], True, self.criterionlist)
            criterion_true_node = criterion_true.parent(progenitor_node)
            matrix_one.candidatelist[0].parent(criterion_true_node)
        
        # Linking the "false" matrix to the assertion and deleting the previous assertion
        if len(matrix_two.candidatelist) > 1:
            criterion_false = Criterion.search(self.assertionlist[0], False, self.criterionlist)
            criterion_false_node = criterion_false.parent(progenitor_node)
            matrix_two.progenitor = criterion_false_node
            matrix_two.delete_assertion(0)
            matrix_two.construct_tree(debug)
        elif len(matrix_two.candidatelist) == 1:
            criterion_false = Criterion.search(self.assertionlist[0], False, self.criterionlist)
            criterion_false_node = criterion_false.parent(progenitor_node)
            matrix_two.candidatelist[0].parent(criterion_false_node)
