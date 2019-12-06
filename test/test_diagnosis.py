#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis, diagnosable, undiagnosable

class TestDiagnosis(unittest.TestCase):

    def test_init(self):
        assertionA = Assertion("assertion A")
        assertionB = Assertion("assertion B")
        assertionC = Assertion("assertion C")
        assertionX = Assertion("assertion X")
        criterionA = Criterion(assertionA, True)
        criterionC = Criterion(assertionC, True)
        criterionNB = Criterion(assertionB, False)
        criterionX = Criterion(assertionX, True)
        diagnosis = Diagnosis('Diagnosis name', {criterionA, criterionNB, criterionC, criterionX}, 0.25)
        self.assertEqual(diagnosis.name, "Diagnosis_name")
        self.assertEqual(diagnosis.criteria, {criterionA, criterionNB, criterionC, criterionX})
        self.assertEqual(diagnosis.assertions, {assertionA, assertionB, assertionC, assertionX})
        self.assertEqual(diagnosis.prevalence, 0.25)
    
    def test_equality(self):
        assertionA = Assertion("assertion A")
        assertionB = Assertion("assertion B")
        assertionC = Assertion("assertion C")
        assertionX = Assertion("assertion X")
        diagnosis1 = Diagnosis('Diagnosis 1', {assertionA.true(), assertionB.false(), assertionC.true(), assertionX.false()}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', {assertionA.true(), assertionB.false(), assertionC.true(), assertionX.false()}, 0.5)
        diagnosis3 = Diagnosis('Diagnosis 1', {assertionA.true(), assertionB.false(), assertionC.false(), assertionX.false()}, 0.25)
        self.assertTrue(diagnosis1==diagnosis2)
        self.assertFalse(diagnosis1==diagnosis3)
    
    def test_diagnosable(self):
        assertionA = Assertion("assertion A")
        assertionB = Assertion("assertion B")
        assertionC = Assertion("assertion C")
        assertionX = Assertion("assertion X")
        diagnosis1 = Diagnosis('Diagnosis 1', {assertionA.true(), assertionB.false(), assertionC.true(), assertionX.false()}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', {assertionA.true(), assertionB.false(), assertionC.true(), assertionX.false()}, 0.5)
        diagnosis3 = Diagnosis('Diagnosis 3', {assertionA.true(), assertionB.false(), assertionC.false(), assertionX.false()}, 0.25)
        self.assertTrue(diagnosable({diagnosis1, diagnosis3}))
        self.assertFalse(diagnosable({diagnosis1, diagnosis2}))
    
    def test_undiagnosable(self):
        assertionA = Assertion("assertion A")
        assertionB = Assertion("assertion B")
        assertionC = Assertion("assertion C")
        assertionX = Assertion("assertion X")
        diagnosis1 = Diagnosis('Diagnosis 1', {assertionA.true(), assertionB.false(), assertionC.true(), assertionX.false()}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', {assertionA.true(), assertionB.false(), assertionC.true(), assertionX.false()}, 0.5)
        self.assertEqual(undiagnosable({diagnosis1, diagnosis2}), {"Diagnosis_1/Diagnosis_2"})


if __name__ == '__main__':
    unittest.main()
 