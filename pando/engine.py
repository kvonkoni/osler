from functools import reduce
from collections import Counter
from numpy import matrix, zeros, delete, argwhere, reshape, array_equal, concatenate
from copy import copy
import ete3

from pando.common import Pando
from pando.graph import Node
from pando.criterion import Criterion

class Matrix:
    def __init__(self, issue):
        self.progenitor = Node(issue)
        self.node = self.progenitor
        self.candidatelist = list(issue.candidates)
        assertions = set()
        for d in self.candidatelist:
            assertions.update(d.assertions)
        self.assertionlist = list(assertions)

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

    def SwapColumns(self, a, b):
        if a != b:
            self.matrix[:,[a, b]] = self.matrix[:,[b, a]]
            self.assertionlist[a], self.assertionlist[b] = self.assertionlist[b], self.assertionlist[a]

    def SwapRows(self, a, b):
        if a != b:
            self.matrix[[a, b],:] = self.matrix[[b, a],:]
            self.candidatelist[a], self.candidatelist[b] = self.candidatelist[b], self.candidatelist[a]

    def SortRowsByColumn(self, a):
        arg_sort = self.matrix[:,a].argsort()
        self.matrix = self.matrix[arg_sort]
        self.candidatelist = [self.candidatelist[i] for i in arg_sort]

    def DeleteColumn(self, a):
        self.matrix = delete(self.matrix, a, 1)
        self.assertionlist = delete(self.assertionlist, a)

    def ClearIrrelevantAssertions(self):
        dellist = []
        for i in range(len(self.matrix[0,:])):
            truth_set = set(self.matrix[:,i])
            if len(truth_set) <= 1:
                dellist.append(i)
            elif 0 in truth_set and len(truth_set) == 2:
                dellist.append(i)
        self.DeleteColumn(dellist)

    def BringForwardBestAssertion(self):
        least = 10**8
        num_diagnoses = len(self.matrix[0,:])
        for i in range(num_diagnoses):
            count = Counter(self.matrix[:,i])
            measure = (count[0])**2+(count[1]-num_diagnoses/2.0)**2+(count[1]-num_diagnoses/2.0)**2
            if measure < least:
                least = measure
                id = i
        self.SwapColumns(0, id)

    def SplitByTruthValue(self):
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

    def Combine(self, other):
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

    def ConstructTree(self, debug=False):
        if debug:
            print(self.assertionlist)
            print(self.candidatelist)
            print(self)
        #Choosing the next assertion
        self.ClearIrrelevantAssertions()
        self.BringForwardBestAssertion()
        self.SortRowsByColumn(0)
        #Linking the next assertion to the progenitor
        progenitor_node = self.assertionlist[0].Parent(self.progenitor)
        #Splitting the matrix
        matrix_null, matrix_one, matrix_two = self.SplitByTruthValue()
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
            matrix_one.Combine(matrix_null)
            matrix_two.Combine(matrix_null)
        #Linking the "true" matrix to the assertion and deleting the previous assertion
        if len(matrix_one.candidatelist) > 1:
            criterion_true = Criterion.Search(self.assertionlist[0], True)
            criterion_true_node = criterion_true.Parent(progenitor_node)
            matrix_one.progenitor = criterion_true_node
            matrix_one.DeleteColumn(0)
            matrix_one.ConstructTree()
        elif len(matrix_one.candidatelist) == 1:
            criterion_true = Criterion.Search(self.assertionlist[0], True)
            criterion_true_node = criterion_true.Parent(progenitor_node)
            matrix_one.candidatelist[0].Parent(criterion_true_node)
        #Linking the "false" matrix to the assertion and deleting the previous assertion
        if len(matrix_two.candidatelist) > 1:
            criterion_false = Criterion.Search(self.assertionlist[0], False)
            criterion_false_node = criterion_false.Parent(progenitor_node)
            matrix_two.progenitor = criterion_false_node
            matrix_two.DeleteColumn(0)
            matrix_two.ConstructTree()
        elif len(matrix_two.candidatelist) == 1:
            criterion_false = Criterion.Search(self.assertionlist[0], False)
            criterion_false_node = criterion_false.Parent(progenitor_node)
            matrix_two.candidatelist[0].Parent(criterion_false_node)

def Test(issue):
    matrix = Matrix(issue)
    print(matrix.assertionlist)
    print(matrix.candidatelist)
    print(matrix)
    matrix.ClearIrrelevantAssertions()
    matrix.BringForwardBestAssertion()
    matrix.SortRowsByColumn(0)
    print(matrix.assertionlist)
    print(matrix.candidatelist)
    print(matrix)
    matrix_null, matrix_one, matrix_two = matrix.SplitByTruthValue()
    matrix = matrix_null.Combine(matrix_one).Combine(matrix_two)
    print(matrix.assertionlist)
    print(matrix.candidatelist)
    print(matrix)

def Test2(issue):
    assertionlist = []
    for diagnosis in list(issue.candidates):
        assertionlist.extend(list(diagnosis.assertions))
    counter = Counter(assertionlist)
    print([a.name for a in assertionlist])

def Test1(issue):
    num_diagnoses = len(issue.candidates)
    diagnosislist = list(issue.candidates)

    order = []

    for i in range(num_diagnoses):
        temp = diagnosislist.copy()
        d1 = temp.pop(i)
        residual = reduce(lambda x, y: x + y, temp)
        differentials = d1.DifferentialCriteria(residual)
        number_criteria = len(differentials)
        order.append((diagnosislist[i], diagnosislist[i].name, number_criteria))

    order.sort(key = lambda x: x[2], reverse=True)

    for i in range(num_diagnoses-1):
        current = order.pop(i)
        current_diagnosis = current[0]
        remaining_diagnoses = [d[0] for d in order]
        residual = reduce(lambda x, y: x + y, remaining_diagnoses)
        differential = current_diagnosis.DifferentialCriteria(residual)
        differentiallist = list(differential)
        differentiallist.sort(key = lambda x: x.assertion.ease)
        current_diagnosis.Parent(differentiallist[0])
        for j in range(len(differential)-1):
            if differentiallist[j].assertion != differentiallist[j+1].assertion:
                print(differentiallist[j].assertion.name+"-->"+(differentiallist[j+1]).name)
                differentiallist[j].assertion.Parent(differentiallist[j+1])

def LikeliestFirst(issue):
    diagnosislist = list(issue.candidates)
    diagnosislist.sort(key = lambda x: x.prevalence, reverse=True)

    num_diagnoses = len(diagnosislist)

    commoncriteria = reduce(lambda x, y: x + y, diagnosislist)
    common = set()
    for c in list(commoncriteria.criteria):
            common.add(c)

    if len(common) != 0:
        commonlist = list(common)
        commonlist.sort(key = lambda x: x.assertion.ease)
        for j in range(len(commonlist)-1):
            commonlist[j].assertion.Parent(commonlist[j+1])
        commonlist[-1].assertion.Parent(issue)
        for c in commonlist:
            print(c)
        print("...")

    for i in range(0, num_diagnoses-1):
        residual = reduce(lambda x, y: x + y, diagnosislist[i+1])
        differential = diagnosislist[i].DifferentialCriteria(residual)
        #differential = diagnosislist[i].DifferentialCriteria(sum(diagnosislist[i+1:]))

        differentiallist = list(differential)
        differentiallist.sort(key = lambda x: x.assertion.ease)

        for j in range(len(differentiallist)-1):
            print(differentiallist[j])
            print(differentiallist[j+1])
            if differentiallist[j].assertion != differentiallist[j+1].assertion:
                differentiallist[j].assertion.Parent(differentiallist[j+1])

        if len(common) != 0:
            differentiallist[-1].assertion.Parent(commonlist[0])
        else:
            differentiallist[-1].assertion.Parent(issue)
