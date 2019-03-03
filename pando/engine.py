def ConstructTree(issue):
    diagnosislist = list(issue.candidates)
    diagnosislist.sort(key = lambda x: x.prevalence)

    num_diagnoses = len(diagnosislist)

    for i in range(1, num_diagnoses):
        for diagnosis in range(len(assertionlist[:-1])):
            differential = CompareDiagnoses(diagnosislist[i], diagnosislist[i-1])
            assertionlist[j].parent = assertionlist[j+1]
            assertionlist[j].node.parent = assertionlist[j+1].node
