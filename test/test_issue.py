#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis
from osler.issue import Issue

class TestIssue(unittest.TestCase):

    def test_init(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis description 1', 'Diagnosis remedy 1', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis description 2', 'Diagnosis remedy 2', {assertionA.false, assertionB.false, assertionC.true, assertionX.false}, 0.5)
        diagnosis3 = Diagnosis('Diagnosis 3', 'Diagnosis description 3', 'Diagnosis remedy 3', {assertionA.true, assertionB.false, assertionC.false, assertionX.false}, 0.25)
        issue = Issue("Issue name", "Issue description", {diagnosis1, diagnosis2, diagnosis3})
        self.assertEqual(issue.name, "Issue_name")
        self.assertEqual(issue.description, "Issue description")
        self.assertEqual(issue.candidates, {diagnosis1, diagnosis2, diagnosis3})
    
    def test_validate(self):
        assertionA = Assertion("assertion A", "is assertion A true?")
        assertionB = Assertion("assertion B", "is assertion B true?")
        assertionC = Assertion("assertion C", "is assertion C true?")
        assertionX = Assertion("assertion X", "is assertion X true?")
        diagnosis1 = Diagnosis('Diagnosis 1', 'Diagnosis description 1', 'Diagnosis remedy 1', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.25)
        diagnosis2 = Diagnosis('Diagnosis 2', 'Diagnosis description 2', 'Diagnosis remedy 2', {assertionA.true, assertionB.false, assertionC.true, assertionX.false}, 0.5)
        with self.assertRaises(Exception):
            issue = Issue("Issue name", "Issue description", {diagnosis1, diagnosis2})

if __name__ == '__main__':
    unittest.main()
 