from functools import reduce
from pando.diagnosis import CompareDiagnoses

def ConstructTree(issue):
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
        residual = diagnosislist[i+1]
        for d in diagnosislist[i+2:]:
            residual = residual + d
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
