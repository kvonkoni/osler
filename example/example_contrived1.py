#!/usr/bin/env python3

import os
import sys

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis
from osler.issue import Issue
from osler.engine import Matrix

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

diagnosis1 = Diagnosis('Diagnosis 1', {criterionA, criterionNB, criterionC, criterionX}, 0.25)
diagnosis2 = Diagnosis('Diagnosis 2', {criterionNA, criterionNC, criterionD, criterionY, criterionX}, 0.15)
diagnosis3 = Diagnosis('Diagnosis 3', {criterionNA, criterionC, criterionX}, 0.5)
diagnosis4 = Diagnosis('Diagnosis 4', {criterionNA, criterionNC, criterionND, criterionE, criterionX}, 0.25)
diagnosis5 = Diagnosis('Diagnosis 5', {criterionNA, criterionNC, criterionND, criterionNE, criterionX}, 0.025)

#Defining an issue

issue = Issue('Issue I', {diagnosis1, diagnosis2, diagnosis3, diagnosis4, diagnosis5})

#Building a test tree

matrix = Matrix(issue)
matrix.construct_tree()

matrix.to_png("example_contrived1.png")
matrix.to_svg("example_contrived1.svg")
