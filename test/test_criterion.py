#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion

class TestCriterion(unittest.TestCase):

    def test_init(self):
        assertion = Assertion("This is an assertion", 1.3)
        criterion = Criterion(assertion, True)
        self.assertEqual(criterion.assertion, assertion)
        self.assertEqual(criterion.truth_value, True)
        self.assertEqual(criterion.name, "This_is_an_assertion_is_True")
    
    def test_equivalence(self):
        assertion1 = Assertion("This is an assertion", 1.3)
        criterion1 = Criterion(assertion1, True)
        assertion2 = Assertion("This is an assertion", 1.3)
        criterion2 = Criterion(assertion2, True)
        self.assertTrue(criterion1==criterion2)
        self.assertFalse(criterion1.opposite(criterion2))
    
    def test_opposites(self):
        assertion = Assertion("This is an assertion", 1.3)
        criterion1 = Criterion(assertion, True)
        criterion2 = Criterion(assertion, False)
        self.assertTrue(criterion1.opposite(criterion2))
        self.assertFalse(criterion1==criterion2)

if __name__ == '__main__':
    unittest.main()
 