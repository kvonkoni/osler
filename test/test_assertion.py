#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion

class TestAssertion(unittest.TestCase):

    def test_init(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion?", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.proposition, "This is an assertion")
        self.assertEqual(assertion.question, "This is the question that tests the assertion?")
        self.assertEqual(assertion.instruction, "These are instructions on how to test the assertion")
        self.assertEqual(assertion.ease, 1.3)
        self.assertEqual(assertion.name, "This_is_an_assertion")
        self.assertEqual(assertion.description, "Here are more details")

    def test_equivalent(self):
        assertion1 = Assertion("This is an assertion", "This is the question that tests the assertion", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        assertion2 = Assertion("This is an assertion", "This is the question that tests the assertion", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertTrue(assertion1==assertion2)
    
    def test_non_equivalent(self):
        assertion1 = Assertion("This is an assertion", "This is the question that tests the assertion", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        assertion2 = Assertion("This is a different assertion", "This is the question that tests the different assertion", "These are instructions on how to test the different assertion", 1.5, "Here are more details")
        self.assertFalse(assertion1==assertion2)

if __name__ == '__main__':
    unittest.main()
