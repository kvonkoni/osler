#!/usr/bin/env python3

from .common import EntityBase, NodeMixin
from .criterion import Criterion

class Assertion(EntityBase, NodeMixin):

    def __init__(self, proposition, test_difficulty=0.0, **kwargs):
        self.proposition = proposition
        self.name = proposition.replace(" ", "_")
        self.test_difficulty = test_difficulty
        self.metadata = kwargs
        if 'cannot_preceed' in kwargs:
            self.cannot_preceed = kwargs.get('cannot_preceed')
        else:
            self.cannot_preceed = None

    def __eq__(self, other):
        if isinstance(other, Assertion):
            return self.proposition == other.proposition
        else:
            return False
    
    def true(self):
        return Criterion(self, True)
    
    def false(self):
        return Criterion(self, False)