#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
#nltk.download()

class Assertion:
    list = []

    def __init__(self, proposition, question, instruction='', ease=1.0, description='', parent=None):
        Assertion.list.append(self)
        self.proposition = proposition
        self.question = question
        self.instruction = instruction
        self.ease = ease
        self.name = proposition.replace(" ", "_")
        self.description = description
        self.node = anytree.Node(self.name)
        self.parent = parent

    def Equivalent(self, other):
        if self.proposition == other.proposition:
            return True
        else:
            return False

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Assertion):
            return self.equivalent(other)
        else:
            return False
