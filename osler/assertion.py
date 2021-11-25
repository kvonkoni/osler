#!/usr/bin/env python3

import logging
log = logging.getLogger(__name__)

from .graph import Node
from .criterion import Criterion

class Assertion(object):

    def __init__(self, proposition, test_difficulty=0.0, **kwargs):
        self.proposition = proposition
        self.name = proposition.replace(" ", "_")
        self.test_difficulty = test_difficulty
        self.metadata = kwargs
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
    
    def true(self):
        return Criterion(self, True)
    
    def false(self):
        return Criterion(self, False)

    def parent(self, parent_node):
        return Node(self, parent_node)