import os,sys,math,csv
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion
from pando.criterion import Criterion
from pando.diagnosis import Diagnosis
from pando.issue import Issue

from anytree.exporter import DotExporter
import graphviz

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

diagnosisA = Diagnosis('Diagnosis A', 'Diagnosis A', 'Remedy A', {criterionA, criterionB, criterionC, criterionX}, 0.25)
diagnosisB = Diagnosis('Diagnosis B', 'Diagnosis B', 'Remedy B', {criterionD, criterionE, criterionX}, 0.5)

#Defining an issue

issue = Issue('Issue A', 'Issue A', {diagnosisA, diagnosisB})

#Building a test tree

diagnosisA.node.parent = criterionA.node
criterionA.node.parent = assertionA.node
assertionA.node.parent = criterionC.node
criterionC.node.parent = assertionC.node
assertionC.node.parent = criterionX.node
criterionX.node.parent = issue.node

diagnosisB.node.parent = criterionX.node
criterionX.node.parent = assertionX.node
assertionX.node.parent = criterionB.node
criterionB.node.parent = assertionB.node
assertionB.node.parent = issue.node

#Testing tree functions

issue.render()
