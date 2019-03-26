#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
#nltk.download()
from pando.graph import Node
from pando.criterion import Criterion

class Assertion(object):

    def __init__(self, proposition, question, instruction='', ease=1.0, description=''):
        self.proposition = proposition
        self.question = question
        self.instruction = instruction
        self.ease = ease
        self.name = proposition.replace(" ", "_")
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if self.proposition == other.proposition:
            return True
        else:
            return False

    def parent(self, parent_node):
        return Node(self, parent_node)
    
    def true(self):
        return Criterion(self, True)
    
    def false(self):
        return Criterion(self, False)
