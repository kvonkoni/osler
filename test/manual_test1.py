#!/usr/bin/env python

import os,sys,math,csv
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
import numpy.matlib
from pando.assertion import Assertion
from pando.criterion import Criterion
from pando.diagnosis import Diagnosis
from pando.issue import Issue
from pando.graph import Node

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
criterionNY = Criterion(assertionY, False)

#Defining diagnoses

diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis 1', 'Remedy 1', {criterionA, criterionNB, criterionC, criterionX}, 0.25)
diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis 2', 'Remedy 2', {criterionNA, criterionNC, criterionD, criterionNY, criterionX}, 0.15)
diagnosis3 = Diagnosis('Diagnosis 3', 'Diagnosis 3', 'Remedy 3', {criterionNA, criterionC, criterionX}, 0.5)
diagnosis4 = Diagnosis('Diagnosis 4', 'Diagnosis 4', 'Remedy 4', {criterionNA, criterionNC, criterionND, criterionE, criterionX}, 0.25)
diagnosis5 = Diagnosis('Diagnosis 5', 'Diagnosis 5', 'Remedy 5', {criterionNA, criterionNC, criterionND, criterionNE, criterionX}, 0.025)

#Defining an issue

issue = Issue('Issue I', 'Issue I', {diagnosis1, diagnosis2, diagnosis3, diagnosis4, diagnosis5})

#Building a test tree
# Assertions A, B, C, D, E, X, Y
# 0 = N/A, 1 = True, 2 = False
matrix = [  [1, 2, 1, 0, 0, 1, 0], #1
            [2, 0, 2, 1, 0, 1, 2], #2
            [2, 0, 1, 0, 0, 1, 0], #3
            [2, 0, 2, 2, 1, 1, 0], #4
            [2, 0, 2, 2, 2, 1, 0]] #5

# Remove irrelevant assertions (all the same number in a column excluding zeros)
matrix = [  [1, 1, 0, 0], #1
            [2, 2, 1, 0], #2
            [2, 1, 0, 0], #3
            [2, 2, 2, 1], #4
            [2, 2, 2, 2]] #5

# Sort the columns so that the first question splits the space into the 2 largest groups
#            C, A, D, E
matrix = [  [1, 1, 0, 0], #1
            [2, 2, 1, 0], #2
            [1, 2, 0, 0], #3
            [2, 2, 2, 1], #4
            [2, 2, 2, 2]] #5

# Sort the rows by answer to the first question, link the issue to the first question
#            C, A, D, E
matrix = [  [1, 1, 0, 0], #1
            [1, 2, 0, 0], #3
            [2, 2, 1, 0], #2
            [2, 2, 2, 1], #4
            [2, 2, 2, 2]] #5

# Split the matrix into 2 by answer to the first question, link each answer to the first question to the first question
#            C, A, D, E
matrix1 = [ [1, 1, 0, 0], #1
            [1, 2, 0, 0]] #3

#            C, A, D, E
matrix2 = [ [2, 2, 1, 0], #2
            [2, 2, 2, 1], #4
            [2, 2, 2, 2]] #5

# For each matrix, remove irrelevant assertions (all the same number in a column excluding zeros)
#            A
matrix1 = [ [1], #1
            [2]] #3

#            D, E
matrix2 = [ [1, 0], #2
            [2, 1], #4
            [2, 2]] #5

# For each matrix, sort the columns so that the second question splits the space into the 2 largest groups, link the second question to the answers to the first question (each matrix)
#            A
matrix1 = [ [1], #1
            [2]] #3

#            D, E
matrix2 = [ [1, 0], #2
            [2, 1], #4
            [2, 2]] #5

# For each matrix, split the matrix by answer to the second question,
#            A
matrix1 = [ [1]] #1

#            A
matrix3 = [ [2]] #3

#            C, D, E
matrix2 = [ [2, 1, 0]] #2

#            C, D, E
matrix4 = [ [2, 2, 1], #4
            [2, 2, 2]] #5

#Repeat the process until each matrix is just a row vector. Link each diagnosis to the answer to the last question.

#For diagnosis 1
#I->C->A->1

inode = Node(issue)
aCnode = assertionC.parent(inode)

cCnode = criterionC.parent(aCnode)
aAnode = assertionA.parent(cCnode)
cAnode = criterionA.parent(aAnode)
d1node = diagnosis1.parent(cAnode)


#For diagnosis 2
#I->C->D->2

cNCnode = criterionNC.parent(aCnode)
aDnode = assertionD.parent(cNCnode)
cDnode = criterionD.parent(aDnode)
d2node = diagnosis2.parent(cDnode)


#For diagnosis 3
#I->C->A->3

cNAnode = criterionNA.parent(aAnode)
d3node = diagnosis3.parent(cNAnode)


#For diagnosis 4
#I->C->D->->E->4

cNDnode = criterionND.parent(aDnode)
aEnode = assertionE.parent(cNDnode)
cEnode = criterionE.parent(aEnode)
d4node = diagnosis4.parent(cEnode)



#For diagnosis 4
#I->C->D->->E->4

cNEnode = criterionNE.parent(aEnode)
d5node = diagnosis5.parent(cNEnode)



#Printing information

#Writing tree image

inode.to_png("manual_test1.png")
