from functools import reduce
from collections import Counter
from numpy import matrix, zeros

class Matrix:
    def __init__(self, issue):
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
        self.matrix[:,[a, b]] = self.matrix[:,[b, a]]

    def SwapRows(self, a, b):
        self.matrix[[a, b],:] = self.matrix[[b, a],:]

def Test(issue):
    matrix = Matrix(issue)
    print(matrix)
    matrix.SwapRows(0,2)
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
