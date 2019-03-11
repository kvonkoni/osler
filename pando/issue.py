#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from anytree.exporter import DotExporter
from graphviz import Source, render
import itertools
from pando.common import Pando
from pando.graph import Node

class Issue(Pando):
    id_iter = itertools.count()
    ID = {}

    @classmethod
    def AddToClass(cls, id, instance):
        cls.ID[id] = instance

    def __init__(self, name, description, candidates, severity=0, parent=None):
        self.id = "i"+str(next(self.id_iter))
        self.name = name
        self.description = description
        self.candidates = candidates
        self.severity = severity
        self.prevalence = 0.0
        for s in list(self.candidates):
            self.prevalence += s.prevalence
        self.AddToClass(self.id, self)
        self.AddToGlobal(self.id, self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def Parent(self, parent_node):
        return Node(self, parent_node)
