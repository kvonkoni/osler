#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
import itertools
#nltk.download()

class Assertion:
    id_iter = itertools.count()
    ID = {}

    def __init__(self, proposition, question, instruction='', ease=1.0, description='', parent=None):
        self.id = next(self.id_iter)
        self.proposition = proposition
        self.question = question
        self.instruction = instruction
        self.ease = ease
        self.name = proposition.replace(" ", "_")
        self.description = description
        self.node = anytree.Node(self.name, parent=parent)
        self.parent = parent
        Assertion.ID["a"+str(self.id)] = self

    def __str__(self):
        return self.name

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Assertion):
            return self.Equivalent(other)
        else:
            return False

    def Parent(self, parent):
        self.parent = parent
        self.node.parent = parent.node

    def Equivalent(self, other):
        if self.proposition == other.proposition:
            return True
        else:
            return False
