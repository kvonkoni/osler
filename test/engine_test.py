import os,sys,math,csv
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion
from pando.criterion import Criterion
from pando.diagnosis import Diagnosis, CompareDiagnoses
from pando.issue import Issue
from pando.engine import ConstructTree

#Defining assertions

assertionA = Assertion("assertion A", "is assertion A true?")
assertionB = Assertion("assertion B", "is assertion B true?")
assertionC = Assertion("assertion C", "is assertion C true?")
assertionX = Assertion("assertion X", "is assertion X true?")

#Defining criteria

criterionA = Criterion(assertionA, True)
criterionB = Criterion(assertionB, False)
criterionC = Criterion(assertionC, True)

criterionD = Criterion(assertionA, False)
criterionE = Criterion(assertionC, False)

criterionX = Criterion(assertionX, True)

#Defining diagnoses

diagnosisB = Diagnosis('Diagnosis B', 'Diagnosis B', 'Remedy B', {criterionD, criterionE, criterionX}, 0.5)
diagnosisA = Diagnosis('Diagnosis A', 'Diagnosis A', 'Remedy A', {criterionA, criterionB, criterionC, criterionX}, 0.25)
diagnosisC = Diagnosis('Diagnosis C', 'Diagnosis C', 'Remedy C', {criterionD, criterionC, criterionX}, 0.15)

#Defining an issue

issue = Issue('Issue A', 'Issue A', {diagnosisA, diagnosisB})

#Testing tree functions

CompareDiagnoses(diagnosisA, diagnosisB)
CompareDiagnoses(diagnosisB, diagnosisC)
CompareDiagnoses(diagnosisA, diagnosisC)

#Building a test tree

ConstructTree(issue)

#issue.to_image("test_dot.dot")
issue.to_png("test_dot.png")
