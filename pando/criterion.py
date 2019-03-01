#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from pando.assertion import IsEquivalent

class Criterion:
    list = []

    def __init__(self, assertion, truth_value, description='', parent=None):
        Criterion.list.append(self)
        self.assertion = assertion
        self.truth_value = truth_value
        self.name = assertion.name+'_is_'+str(truth_value)
        self.description = description
        self.node = anytree.Node(self.name)
        self.parent = parent

def CommonCriteria(criterionA, criterionB):
    if IsEquivalent(criterionA.assertion, criterionB.assertion) and (criterionA.truth_value == criterionB.truth_value):
        return True
    else:
        return False

def AssertionSetFromCriterionSet(criterion_set):
    result = set()
    for c in list(criterion_set):
        result.add(c.assertion)
    return result
