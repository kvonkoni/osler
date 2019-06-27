#!/usr/bin/env python

import os, sys, unittest
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis
from osler.issue import Issue
from osler.graph import Node

class TestNode(unittest.TestCase):

    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()
 