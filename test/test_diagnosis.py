#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from pando.assertion import Assertion
from pando.criterion import Criterion
from pando.diagnosis import Diagnosis

class TestCriterion(unittest.TestCase):

    def test_init(self):
        assertion = Assertion("This is an assertion", "This is the question that tests the assertion?", "These are instructions on how to test the assertion", 1.3, "Here are more details")
        criterion = Criterion(assertion, True)
        self.assertEqual(criterion.assertion, assertion)
        self.assertEqual(criterion.truth_value, True)

if __name__ == '__main__':
    unittest.main()
 