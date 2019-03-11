#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
import itertools
#nltk.download()
from pando.common import Pando
from pando.graph import Node

class Assertion(Pando):
    id_iter = itertools.count()
    ID = {}

    @classmethod
    def AddToClass(cls, id, instance):
        cls.ID[id] = instance

    def __init__(self, proposition, question, instruction='', ease=1.0, description='', parent=None):
        self.id = "a"+str(next(self.id_iter))
        self.proposition = proposition
        self.question = question
        self.instruction = instruction
        self.ease = ease
        self.name = proposition.replace(" ", "_")
        self.description = description
        self.AddToClass(self.id, self)
        self.AddToGlobal(self.id, self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Assertion):
            return self.Equivalent(other)
        else:
            return False

    def Parent(self, parent_node):
        node = Node(self, parent_node)
        etenode = parent_node.etenode.add_child(name=self.name)
        node.etenode = etenode
        return node

    def Equivalent(self, other):
        if self.proposition == other.proposition:
            return True
        else:
            return False
