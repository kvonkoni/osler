import os,sys,math,csv
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion
from pando.criterion import Criterion
from pando.diagnosis import Diagnosis, CompareDiagnoses
from pando.issue import Issue

#Defining assertions

assertionA = Assertion("assertion A", "is assertion A true?")
assertionB = Assertion("assertion B", "is assertion B true?")
assertionC = Assertion("assertion C", "is assertion C true?")
assertionX = Assertion("assertion X", "is assertion X true?")
assertionY = Assertion("assertion Y", "is assertion Y true?")

#Defining criteria

criterionA = Criterion(assertionA, True)
criterionB = Criterion(assertionB, False)
criterionC = Criterion(assertionC, True)

criterionD = Criterion(assertionA, False)
criterionE = Criterion(assertionC, False)

criterionX = Criterion(assertionX, True)
criterionY = Criterion(assertionY, False)

#Defining diagnoses

diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis 1', 'Remedy 1', {criterionA, criterionB, criterionC, criterionX}, 0.25)
diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis 2', 'Remedy 2', {criterionD, criterionE, criterionY, criterionX}, 0.15)
diagnosis3 = Diagnosis('Diagnosis 3', 'Diagnosis 3', 'Remedy 3', {criterionD, criterionC, criterionX}, 0.5)

#Defining an issue

issue = Issue('Issue I', 'Issue I', {diagnosis1, diagnosis2, diagnosis3})

#Building a test tree

#--> top level criteria are common criteria
#I->X
#assertionX.node.parent = issue.node
assertionC.node.parent = issue.node

#--> second level criteria are second-third diagnosis differentials
#C->A->1
diagnosis1.node.parent = criterionA.node
criterionA.assertion.node.parent = criterionC.node
#criterionC.assertion.node.parent = criterionX.node #--> top-level differential criteria should link to bottom-level common criteria

#C->B->Y->2
diagnosis2.node.parent = criterionE.node
#criterionY.assertion.node.parent = criterionB.node
#criterionB.assertion.node.parent = criterionE.node
#criterionE.assertion.node.parent = criterionX.node #--> top-level differential criteria should link to bottom-level common criteria

#C->A->3
diagnosis3.node.parent = criterionD.node
criterionD.assertion.node.parent = criterionC.node
#criterionC.assertion.node.parent = criterionX.node #--> top-level differential criteria should link to bottom-level common criteria

#Testing tree functions
CompareDiagnoses(diagnosis1, diagnosis2)
CompareDiagnoses(diagnosis2, diagnosis3)
CompareDiagnoses(diagnosis3, diagnosis1)

CompareDiagnoses(diagnosis1, diagnosis2+diagnosis3)
CompareDiagnoses(diagnosis2, diagnosis1+diagnosis3)
CompareDiagnoses(diagnosis3, diagnosis1+diagnosis2)

diagnosis1.info()
diagnosis2.info()
diagnosis3.info()

#issue.to_image("test_dot.dot")
issue.To_png("test_manual.png")
