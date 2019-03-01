from pando.criterion import CommonCriteria, AssertionSetFromCriterionSet
from pando.diagnosis import DifferentialCriteria

def CompareDiagnoses(diagA, diagB):
    common_criteria = diagA.criteria.intersection(diagB.criteria)
    differential_criteria = DifferentialCriteria(diagA, diagB)
    inconsequential_criteria = diagA.criteria.union(diagB.criteria).difference(common_criteria.union(differential_criteria))

    common_assertions = set()
    for c in list(common_criteria):
        common_assertions.add(c.assertion)
    differential_assertions = set()
    for d in list(differential_criteria):
        differential_assertions.add(d.assertion)
    inconsequential_assertions = set()
    for i in list(inconsequential_criteria):
        inconsequential_assertions.add(i.assertion)

    print("Common Criteria:")
    for c in list(common_criteria):
        print(c.name)
    print("Differential Criteria")
    for d in list(differential_criteria):
        print(d.name)
    print("Inconsequential Criteria")
    for i in list(inconsequential_criteria):
        print(i.name)

    print("Common Assertions:")
    for c in list(common_assertions):
        print(c.name)
    print("Differential Assertions")
    for d in list(differential_assertions):
        print(d.name)
    print("Inconsequential Assertions")
    for i in list(inconsequential_assertions):
        print(i.name)

    return differential_criteria

def ConstructTree(issue):
    diagnosislist = list(issue.candidates)
    diagnosislist.sort(key = lambda x: x.prevalence, reverse=True)

    num_diagnoses = len(diagnosislist)

    for i in range(1, num_diagnoses):
        differential_criteria = CompareDiagnoses(diagnosislist[i], diagnosislist[i-1])
        differential_assertions = AssertionSetFromCriterionSet(differential_criteria)
        assertionlist = list(differential_assertions)
        assertionlist.sort(key = lambda x: x.ease)
        diagnosislist[i].parent = assertionlist[0]
        diagnosislist[i].node.parent = assertionlist[0].node
        for j in range(len(assertionlist[:-1])):
            assertionlist[j].parent = assertionlist[j+1]
            assertionlist[j].node.parent = assertionlist[j+1].node
        assertionlist[len(assertionlist[:-1])].parent = issue
        assertionlist[len(assertionlist[:-1])].node.parent = issue.node
