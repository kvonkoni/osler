from functools import reduce
from pando.diagnosis import CompareDiagnoses

def Test(issue):

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
