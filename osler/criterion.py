#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from osler.graph import Node

class Criterion(object):

    @classmethod
    def search(cls, assertion, truth_value, criterialist):
        criterion = Criterion(assertion, truth_value)
        for c in criterialist:
            if c == criterion:
                return c

    def __init__(self, assertion, truth_value):
        self.assertion = assertion
        self.truth_value = truth_value
        self.name = assertion.name+'_is_'+str(truth_value)
        self.id = self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if self.assertion == other.assertion and (self.truth_value == other.truth_value):
            return True
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
