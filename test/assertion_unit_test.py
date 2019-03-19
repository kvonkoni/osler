#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion

class TestAssertion(unittest.TestCase):

    def test_proposition(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion?", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.proposition, "This is an assertion")

    def test_question(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion?", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.question, "This is the question that tests the assertion?")

    def test_instruction(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.instruction, "These are instructions on how to test the assertion")

    def test_ease(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.ease, 1.3)

    def test_description(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.description, "Here are more details")

if __name__ == '__main__':
    unittest.main()
