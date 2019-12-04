#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion

class TestAssertion(unittest.TestCase):

    def test_init(self):
        assertion = Assertion("This is an assertion", 1.3)
        self.assertEqual(assertion.proposition, "This is an assertion")
        self.assertEqual(assertion.test_difficulty, 1.3)
        self.assertFalse(assertion.cannot_preceed)

    def test_equivalent(self):
        assertion1 = Assertion("This is an assertion", 1.3)
        assertion2 = Assertion("This is an assertion", 1.3)
        self.assertTrue(assertion1==assertion2)
    
    def test_non_equivalent(self):
        assertion1 = Assertion("This is an assertion", 1.3)
        assertion2 = Assertion("This is a different assertion", 1.5)
        self.assertFalse(assertion1==assertion2)

if __name__ == '__main__':
    unittest.main()
