#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis
from osler.issue import Issue
from osler.graph import Node

class TestNode(unittest.TestCase):
    def test_init(self):
        assertionA = Assertion("assertion A")
        criterionA = Criterion(assertionA, True)

        parent_node = Node(assertionA)
        child_node = Node(criterionA, parent_node)

        self.assertEqual(parent_node.object, assertionA)
        self.assertEqual(parent_node.parent, None)
        self.assertEqual(child_node.parent, parent_node)
        self.assertEqual(child_node.children, [])
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.root, True)
        self.assertEqual(child_node.root, False)
        self.assertEqual(parent_node.leaf, False)
        self.assertEqual(child_node.leaf, True)

    def test_equal(self):
        #Defining assertions

        assertionA = Assertion("assertion A")
        assertionB = Assertion("assertion B")
        assertionC = Assertion("assertion C")
        assertionD = Assertion("assertion D")
        assertionE = Assertion("assertion E")
        assertionX = Assertion("assertion X")
        assertionY = Assertion("assertion Y")

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

        diagnosis1 = Diagnosis('Diagnosis 1', {criterionA, criterionNB, criterionC, criterionX}, 0.2)
        diagnosis2 = Diagnosis('Diagnosis 2', {criterionNA, criterionNC, criterionD, criterionY, criterionX}, 0.2)
        diagnosis3 = Diagnosis('Diagnosis 3', {criterionNA, criterionC, criterionX}, 0.2)
        diagnosis4 = Diagnosis('Diagnosis 4', {criterionNA, criterionNC, criterionND, criterionE, criterionX}, 0.2)
        diagnosis5 = Diagnosis('Diagnosis 5', {criterionNA, criterionNC, criterionND, criterionNE, criterionX}, 0.2)

        #Defining an issue

        issue = Issue('Issue I', {diagnosis1, diagnosis2, diagnosis3, diagnosis4, diagnosis5})

        #Building a test tree manually

        #For diagnosis 1
        #I->C->A->1

        inode1 = Node(issue)
        aCnode1 = assertionC.parent(inode1)

        cCnode1 = criterionC.parent(aCnode1)
        aAnode1 = assertionA.parent(cCnode1)
        cAnode1 = criterionA.parent(aAnode1)
        diagnosis1.parent(cAnode1)


        #For diagnosis 2
        #I->C->D->2

        cNCnode1 = criterionNC.parent(aCnode1)
        aDnode1 = assertionD.parent(cNCnode1)
        cDnode1 = criterionD.parent(aDnode1)
        diagnosis2.parent(cDnode1)


        #For diagnosis 3
        #I->C->A->3

        cNAnode1 = criterionNA.parent(aAnode1)
        diagnosis3.parent(cNAnode1)


        #For diagnosis 4
        #I->C->D->->E->4

        cNDnode1 = criterionND.parent(aDnode1)
        aEnode1 = assertionE.parent(cNDnode1)
        cEnode1 = criterionE.parent(aEnode1)
        diagnosis4.parent(cEnode1)



        #For diagnosis 4
        #I->C->D->->E->4

        cNEnode1 = criterionNE.parent(aEnode1)
        diagnosis5.parent(cNEnode1)

        #Building a second test tree manually

        #For diagnosis 2
        #I->C->A->1

        inode2 = Node(issue)
        aCnode2 = assertionC.parent(inode2)

        cNCnode2 = criterionNC.parent(aCnode2)
        aDnode2 = assertionD.parent(cNCnode2)
        cDnode2 = criterionD.parent(aDnode2)
        diagnosis2.parent(cDnode2)

        #For diagnosis 1
        #I->C->D->2

        cCnode2 = criterionC.parent(aCnode2)
        aAnode2 = assertionA.parent(cCnode2)
        cAnode2 = criterionA.parent(aAnode2)
        diagnosis1.parent(cAnode2)


        #For diagnosis 3
        #I->C->A->3

        cNAnode2 = criterionNA.parent(aAnode2)
        diagnosis3.parent(cNAnode2)


        #For diagnosis 4
        #I->C->D->->E->4

        cNDnode2 = criterionND.parent(aDnode2)
        aEnode2 = assertionE.parent(cNDnode2)
        cEnode2 = criterionE.parent(aEnode2)
        diagnosis4.parent(cEnode2)



        #For diagnosis 5
        #I->C->D->E->5

        cNEnode2 = criterionNE.parent(aEnode2)
        diagnosis5.parent(cNEnode2)

        #Building a third test tree manually

        

        # Assert that the node 1 tree is equal to the node 2 tree
        self.assertEqual(inode1, inode2)

if __name__ == '__main__':
    unittest.main()
 