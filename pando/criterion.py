#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
import itertools

class Criterion:
    newid = itertools.count().next
    list = []

    def __init__(self, assertion, truth_value):
        Criterion.list.append(self)
        self.id = resource_cl.newid()
        self.assertion = assertion
        self.truth_value = truth_value
        self.name = assertion.name+'_is_'+str(truth_value)
        self.node = anytree.Node(self.name, parent=self.assertion.node)
        self.parent = self.assertion

    def __str__(self):
        return self.name

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Criterion):
            return self.Equivalent(other)
        else:
            return False

    def Parent(self, parent_criterion):
        self.assertion.parent = parent_criterion
        self.assertion.node.parent = parent_criterion.node

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
