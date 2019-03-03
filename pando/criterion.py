#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree

class Criterion:
    list = []

    def __init__(self, assertion, truth_value, parent=None):
        Criterion.list.append(self)
        self.assertion = assertion
        self.truth_value = truth_value
        self.name = assertion.name+'_is_'+str(truth_value)
        self.node = anytree.Node(self.name)
        self.parent = parent

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Criterion):
            return self.Equivalent(other)
        else:
            return False

    def Equivalent(self, other):
        if self.assertion.Equivalent(other.assertion) and (self.truth_value == other.truth_value):
            return True
        else:
            return False

    def Opposite(self, other):
        if self.assertion.Equivalent(other.assertion) and (self.truth_value != other.truth_value):
            return True
        else:
            return False

def AssertionSetFromCriterionSet(criterion_set):
    result = set()
    for c in list(criterion_set):
        result.add(c.assertion)
    return result
