#!/usr/bin/env python3

import logging
log = logging.getLogger(__name__)

from .graph import Node

class Criterion(object):

    @classmethod
    def search(cls, assertion, truth_value, criterialist):
        criterion = Criterion(assertion, truth_value)
        for c in criterialist:
            if c == criterion:
                return c

    def __init__(self, assertion, truth_value, **kwargs):
        self.assertion = assertion
        self.truth_value = truth_value
        self.name = assertion.name+'_is_'+str(truth_value)
        self.metadata = kwargs

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Criterion):
            return self.assertion == other.assertion and (self.truth_value == other.truth_value)
        else:
            return False

    def parent(self, parent_node):
        return Node(self, parent_node)

    def opposite(self, other):
        if self.assertion == other.assertion and (self.truth_value != other.truth_value):
            return True
        else:
            return False

def assertion_set_from_criterion_set(criterion_set):
    result = set()
    for c in list(criterion_set):
        result.add(c.assertion)
    return result
