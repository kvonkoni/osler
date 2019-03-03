from pando.diagnosis import CompareDiagnoses

def ConstructTree(issue):
    diagnosislist = list(issue.candidates)
    diagnosislist.sort(key = lambda x: x.prevalence, reverse=True)

    num_diagnoses = len(diagnosislist)

    common = set()
    for i in range(1, num_diagnoses):
        common_criteria = diagnosislist[i].CommonCriteria(diagnosislist[i-1])
        common = common.union(common_criteria)
    if len(common) != 0:
        commonlist = list(common)
        commonlist.sort(key = lambda x: x.assertion.ease)
        for j in range(len(commonlist)-1):
            commonlist[j].assertion.Parent(commonlist[j+1])
        commonlist[-1].assertion.Parent(issue)
    for i in range(1, num_diagnoses):
            differential = diagnosislist[i].DifferentialCriteria(diagnosislist[i-1])
