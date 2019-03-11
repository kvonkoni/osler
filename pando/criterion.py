#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
import itertools
from pando.common import Pando
from pando.graph import Node

class Criterion(Pando):
    id_iter = itertools.count()
    ID = {}
    list = []

    @classmethod
    def AddToClass(cls, id, instance):
        cls.ID[id] = instance
        cls.list.append(instance)

    @classmethod
    def Search(cls, assertion, truth_value, criterialist=None):
        if not criterialist:
            criterialist = cls.list
        criterion = Criterion(assertion, truth_value)
        for c in criterialist:
            if c == criterion:
                return c

    def __init__(self, assertion, truth_value):
        self.id = "c"+str(next(self.id_iter))
        self.assertion = assertion
        self.truth_value = truth_value
        self.name = assertion.name+'_is_'+str(truth_value)
        self.AddToClass(self.id, self)
        self.AddToGlobal(self.id, self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Criterion):
            return self.Equivalent(other)
        else:
            return False

    def Parent(self, parent_node):
        node = Node(self, parent_node)
        etenode = parent_node.etenode.add_child(name=self.name)
        node.etenode = etenode
        return node

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
