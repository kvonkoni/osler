from pando.criterion import AssertionSetFromCriterionSet

def CompareDiagnoses(diagA, diagB):
    common_assertions = diagA.Common(diagB)#diagA.criteria.intersection(diagB.criteria)
    differential_assertions = diagA.Differential(diagB)
    #inconsequential_assertions = diagA.assertion.union(diagB.assertion).difference(common_assertions.union(differential_assertions))

    print("Common Assertions:")
    for c in list(common_assertions):
        print(c.name)
    print("Differential Assertions:")
    for d in list(differential_assertions):
        print(d.name)
    #print("Inconsequential Assertions")
    #for i in list(inconsequential_assertions):
    #    print(i.name)

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
