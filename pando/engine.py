from functools import reduce
from collections import Counter
from numpy import matrix, zeros, delete, argwhere, reshape, array_equal, concatenate
from copy import copy
import ete3

from pando.graph import Node
from pando.criterion import Criterion

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

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return self.__str__()

    def swap_columns(self, a, b):
        if a != b:
            self.matrix[:,[a, b]] = self.matrix[:,[b, a]]
            self.assertionlist[a], self.assertionlist[b] = self.assertionlist[b], self.assertionlist[a]

    def swap_rows(self, a, b):
        if a != b:
            self.matrix[[a, b],:] = self.matrix[[b, a],:]
            self.candidatelist[a], self.candidatelist[b] = self.candidatelist[b], self.candidatelist[a]

    def sort_rows_by_column(self, a):
        arg_sort = self.matrix[:,a].argsort()
        self.matrix = self.matrix[arg_sort]
        self.candidatelist = [self.candidatelist[i] for i in arg_sort]

    def delete_column(self, a):
        self.matrix = delete(self.matrix, a, 1)
        self.assertionlist = delete(self.assertionlist, a)

    def clear_irrelevant_assertions(self):
        dellist = []
        for i in range(len(self.matrix[0,:])):
            truth_set = set(self.matrix[:,i])
            if len(truth_set) <= 1:
                dellist.append(i)
            elif 0 in truth_set and len(truth_set) == 2:
                dellist.append(i)
        self.delete_column(dellist)

    def bring_forward_best_assertion(self):
        least = 10**8
        num_diagnoses = len(self.matrix[0,:])
        for i in range(num_diagnoses):
            count = Counter(self.matrix[:,i])
            measure = (count[0])**2+(count[1]-num_diagnoses/2.0)**2+(count[1]-num_diagnoses/2.0)**2
            if measure < least:
                least = measure
                id = i
        self.swap_columns(0, id)

    def split_by_truth_value(self):
        index_null = reshape(argwhere(self.matrix[:,0]==0),-1)
        index_one = reshape(argwhere(self.matrix[:,0]==1),-1)
        index_two = reshape(argwhere(self.matrix[:,0]==2),-1)
        matrix_null = copy(self)
        matrix_one = copy(self)
        matrix_two = copy(self)
        matrix_null.matrix = self.matrix[index_null,:]
        matrix_null.candidatelist = [self.candidatelist[i] for i in index_null]
        matrix_null.projenitor = self.assertionlist[0]
        #matrix_null.DeleteColumn(0)
        matrix_one.matrix = self.matrix[index_one,:]
        matrix_one.candidatelist = [self.candidatelist[i] for i in index_one]
        matrix_one.projenitor = self.assertionlist[0]
        #matrix_one.DeleteColumn(0)
        matrix_two.matrix = self.matrix[index_two,:]
        matrix_two.candidatelist = [self.candidatelist[i] for i in index_two]
        matrix_two.projenitor = self.assertionlist[0]
        #matrix_two.DeleteColumn(0)
        return (matrix_null, matrix_one, matrix_two)

    def combine(self, other):
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
            print(self.assertionlist)
            print(self.candidatelist)
            print(self)
        #Choosing the next assertion
        self.clear_irrelevant_assertions()
        self.bring_forward_best_assertion()
        self.sort_rows_by_column(0)
        #Linking the next assertion to the progenitor
        progenitor_node = self.assertionlist[0].parent(self.progenitor)
        #Splitting the matrix
        matrix_null, matrix_one, matrix_two = self.split_by_truth_value()
        if debug:
            print("Matrix 0:")
            print(matrix_null.assertionlist)
            print(matrix_null.candidatelist)
            print(matrix_null)
            print("Matrix 1:")
            print(matrix_one.assertionlist)
            print(matrix_one.candidatelist)
            print(matrix_one)
            print("Matrix 2:")
            print(matrix_two.assertionlist)
            print(matrix_two.candidatelist)
            print(matrix_two)
            print("")
        #Combining the the "null" matrix into both the ones and zeros matrices, inheriting their respective progenitors
        if len(matrix_null.candidatelist) > 1:
            matrix_one.combine(matrix_null)
            matrix_two.combine(matrix_null)
        #Linking the "true" matrix to the assertion and deleting the previous assertion
        if len(matrix_one.candidatelist) > 1:
            criterion_true = Criterion.search(self.assertionlist[0], True, self.criterionlist)
            criterion_true_node = criterion_true.parent(progenitor_node)
            matrix_one.progenitor = criterion_true_node
            matrix_one.delete_column(0)
            matrix_one.construct_tree(debug)
        elif len(matrix_one.candidatelist) == 1:
            criterion_true = Criterion.search(self.assertionlist[0], True, self.criterionlist)
            criterion_true_node = criterion_true.parent(progenitor_node)
            matrix_one.candidatelist[0].parent(criterion_true_node)
        #Linking the "false" matrix to the assertion and deleting the previous assertion
        if len(matrix_two.candidatelist) > 1:
            criterion_false = Criterion.search(self.assertionlist[0], False, self.criterionlist)
            criterion_false_node = criterion_false.parent(progenitor_node)
            matrix_two.progenitor = criterion_false_node
            matrix_two.delete_column(0)
            matrix_two.construct_tree(debug)
        elif len(matrix_two.candidatelist) == 1:
            criterion_false = Criterion.search(self.assertionlist[0], False, self.criterionlist)
            criterion_false_node = criterion_false.parent(progenitor_node)
            matrix_two.candidatelist[0].parent(criterion_false_node)
