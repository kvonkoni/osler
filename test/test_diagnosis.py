#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis

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
        diagnosis = Diagnosis('Diagnosis Name', 'Diagnosis Description', 'Diagnosis Remedy', {criterionA, criterionNB, criterionC, criterionX}, 0.25)
        self.assertEqual(diagnosis.name, "Diagnosis Name")
        self.assertEqual(diagnosis.description, "Diagnosis Description")
        self.assertEqual(diagnosis.remedy, "Diagnosis Remedy")
        self.assertEqual(diagnosis.criteria, {criterionA, criterionNB, criterionC, criterionX})
        self.assertEqual(diagnosis.assertions, {assertionA, assertionB, assertionC, assertionX})
        self.assertEqual(diagnosis.prevalence, 0.25)
        self.assertEqual(diagnosis.comorbidity, set())
    
    def test_equality(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis Description 1', 'Diagnosis Remedy 1', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis Description 2', 'Diagnosis Remedy 2', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.5)
        diagnosis3 = Diagnosis('Diagnosis 1', 'Diagnosis Description 1', 'Diagnosis Remedy 1', {assertionA.true, assertionB.false, assertionC.false, assertionX.false}, 0.25)
        self.assertTrue(diagnosis1==diagnosis2)
        self.assertFalse(diagnosis1==diagnosis3)

if __name__ == '__main__':
    unittest.main()
 