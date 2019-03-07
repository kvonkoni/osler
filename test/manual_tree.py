import os,sys,math,csv
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion
from pando.criterion import Criterion
from pando.diagnosis import Diagnosis, CompareDiagnoses
from pando.issue import Issue
from pando.graph import Node
from pando.common import Pando

#Defining assertions

assertionA = Assertion("assertion A", "is assertion A true?")
assertionB = Assertion("assertion B", "is assertion B true?")
assertionC = Assertion("assertion C", "is assertion C true?")
assertionD = Assertion("assertion D", "is assertion D true?")
assertionE = Assertion("assertion E", "is assertion E true?")
assertionX = Assertion("assertion X", "is assertion X true?")
assertionY = Assertion("assertion Y", "is assertion Y true?")

#Defining criteria

criterionA = Criterion(assertionA, True)
criterionB = Criterion(assertionB, True)
criterionC = Criterion(assertionC, True)
criterionD = Criterion(assertionD, True)
criterionE = Criterion(assertionE, True)

criterionNA = Criterion(assertionA, False)
criterionNB = Criterion(assertionB, False)
criterionNC = Criterion(assertionC, False)
criterionND = Criterion(assertionD, False)
criterionNE = Criterion(assertionE, False)

criterionX = Criterion(assertionX, True)
criterionY = Criterion(assertionY, False)

#Defining diagnoses

diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis 1', 'Remedy 1', {criterionA, criterionNB, criterionC, criterionX}, 0.25)
diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis 2', 'Remedy 2', {criterionNA, criterionNC, criterionD, criterionY, criterionX}, 0.15)
diagnosis3 = Diagnosis('Diagnosis 3', 'Diagnosis 3', 'Remedy 3', {criterionNA, criterionC, criterionX}, 0.5)
diagnosis4 = Diagnosis('Diagnosis 4', 'Diagnosis 4', 'Remedy 4', {criterionNA, criterionNC, criterionND, criterionE, criterionX}, 0.25)
diagnosis5 = Diagnosis('Diagnosis 5', 'Diagnosis 5', 'Remedy 5', {criterionNA, criterionNC, criterionND, criterionNE, criterionX}, 0.025)

#Defining an issue

issue = Issue('Issue I', 'Issue I', {diagnosis1, diagnosis2, diagnosis3, diagnosis4, diagnosis5})

#Building a test tree

assertionC.Parent(issue)

diagnosis1.Parent(criterionA)
criterionA.Parent(criterionC)

diagnosis2.Parent(criterionD)
criterionD.Parent(criterionNC)

diagnosis3.Parent(criterionNA)
criterionNA.Parent(criterionC)

diagnosis4.Parent(criterionE)
criterionE.Parent(criterionND)
criterionND.Parent(criterionNC)

diagnosis5.Parent(criterionNE)
criterionNE.Parent(criterionND)
criterionND.Parent(criterionNC)

#Printing information

CompareDiagnoses(diagnosis1, diagnosis2+diagnosis3+diagnosis4+diagnosis5)

#Writing tree image

issue.To_png("test_manual.png")
