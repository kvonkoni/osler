#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion

class TestClassMethods(unittest.TestCase):

    def test_ID_dict(self):
        self.assertIsInstance(Assertion.ID, type({}))

    def test_Clear(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion?", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        Assertion.ClearAll()
        self.assertFalse(Assertion.ID)

class TestInit(unittest.TestCase):

    def test_id(self):
        Assertion.ClearAll()
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion?", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        self.assertEqual(assertion.id, "a0")

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

if __name__ == '__main__':
    unittest.main()
