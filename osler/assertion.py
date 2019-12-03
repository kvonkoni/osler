#!/usr/bin/env python

from osler.graph import Node
from osler.criterion import Criterion

class Assertion(object):

    def __init__(self, proposition, question, instruction='', test_difficulty=0.0, description='', **kwargs):
        self.proposition = proposition
        self.name = proposition.replace(" ", "_")
        self.test_difficulty = test_difficulty
        self.true = Criterion(self, True)
        self.false = Criterion(self, False)
        if 'cannot_preceed' in kwargs:
            self.cannot_preceed = kwargs.get('cannot_preceed')
        else:
            self.cannot_preceed = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Assertion):
            return self.proposition == other.proposition
        else:
            return False

    def parent(self, parent_node):
        return Node(self, parent_node)