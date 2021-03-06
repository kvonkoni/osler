#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis, diagnosable, undiagnosable

class TestDiagnosis(unittest.TestCase):

    def test_init(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        criterionA = Criterion(assertionA, True)
        criterionC = Criterion(assertionC, True)
        criterionNB = Criterion(assertionB, False)
        criterionX = Criterion(assertionX, True)
        diagnosis = Diagnosis('Diagnosis name', 'Diagnosis description', 'Diagnosis remedy', {criterionA, criterionNB, criterionC, criterionX}, 0.25)
        self.assertEqual(diagnosis.name, "Diagnosis_name")
        self.assertEqual(diagnosis.description, "Diagnosis description")
        self.assertEqual(diagnosis.remedy, "Diagnosis remedy")
        self.assertEqual(diagnosis.criteria, {criterionA, criterionNB, criterionC, criterionX})
        self.assertEqual(diagnosis.assertions, {assertionA, assertionB, assertionC, assertionX})
        self.assertEqual(diagnosis.prevalence, 0.25)
        self.assertEqual(diagnosis.comorbidity, set())
    
    def test_equality(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis description 1', 'Diagnosis remedy 1', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis description 2', 'Diagnosis remedy 2', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.5)
        diagnosis3 = Diagnosis('Diagnosis 1', 'Diagnosis description 1', 'Diagnosis remedy 1', {assertionA.true, assertionB.false, assertionC.false, assertionX.false}, 0.25)
        self.assertTrue(diagnosis1==diagnosis2)
        self.assertFalse(diagnosis1==diagnosis3)
    
    def test_diagnosable(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis description 1', 'Diagnosis remedy 1', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis description 2', 'Diagnosis remedy 2', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.5)
        diagnosis3 = Diagnosis('Diagnosis 3', 'Diagnosis description 3', 'Diagnosis remedy 3', {assertionA.true, assertionB.false, assertionC.false, assertionX.false}, 0.25)
        self.assertTrue(diagnosable({diagnosis1, diagnosis3}))
        self.assertFalse(diagnosable({diagnosis1, diagnosis2}))
    
    def test_undiagnosable(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis description 1', 'Diagnosis remedy 1', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis description 2', 'Diagnosis remedy 2', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.5)
        self.assertEqual(undiagnosable({diagnosis1, diagnosis2}), {"Diagnosis_1/Diagnosis_2"})


if __name__ == '__main__':
    unittest.main()
 