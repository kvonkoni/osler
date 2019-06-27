#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis
from osler.issue import Issue
from osler.graph import Node
from osler.engine import Matrix

class TestEngine(unittest.TestCase):

    def test_init(self):
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

        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis 1', 'Remedy 1', {criterionA, criterionNB, criterionC, criterionX}, 0.2)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis 2', 'Remedy 2', {criterionNA, criterionNC, criterionD, criterionY, criterionX}, 0.2)
        diagnosis3 = Diagnosis('Diagnosis 3', 'Diagnosis 3', 'Remedy 3', {criterionNA, criterionC, criterionX}, 0.2)
        diagnosis4 = Diagnosis('Diagnosis 4', 'Diagnosis 4', 'Remedy 4', {criterionNA, criterionNC, criterionND, criterionE, criterionX}, 0.2)
        diagnosis5 = Diagnosis('Diagnosis 5', 'Diagnosis 5', 'Remedy 5', {criterionNA, criterionNC, criterionND, criterionNE, criterionX}, 0.2)

        #Defining an issue

        issue = Issue('Issue I', 'Issue I', {diagnosis1, diagnosis2, diagnosis3, diagnosis4, diagnosis5})

        #Building a test tree using the engine

        matrix = Matrix(issue)
        matrix.construct_tree()

        #Building a test tree manually

        #For diagnosis 1
        #I->C->A->1

        inode = Node(issue)
        aCnode = assertionC.parent(inode)

        cCnode = criterionC.parent(aCnode)
        aAnode = assertionA.parent(cCnode)
        cAnode = criterionA.parent(aAnode)
        diagnosis1.parent(cAnode)


        #For diagnosis 2
        #I->C->D->2

        cNCnode = criterionNC.parent(aCnode)
        aDnode = assertionD.parent(cNCnode)
        cDnode = criterionD.parent(aDnode)
        diagnosis2.parent(cDnode)


        #For diagnosis 3
        #I->C->A->3

        cNAnode = criterionNA.parent(aAnode)
        diagnosis3.parent(cNAnode)


        #For diagnosis 4
        #I->C->D->->E->4

        cNDnode = criterionND.parent(aDnode)
        aEnode = assertionE.parent(cNDnode)
        cEnode = criterionE.parent(aEnode)
        diagnosis4.parent(cEnode)



        #For diagnosis 4
        #I->C->D->->E->4

        cNEnode = criterionNE.parent(aEnode)
        diagnosis5.parent(cNEnode)

        # Assert that the manually-generated tree is equal to the engine-generated tree
        self.assertTrue(matrix.tree == inode)

if __name__ == '__main__':
    unittest.main()
 