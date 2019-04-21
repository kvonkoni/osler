#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from anytree.exporter import DotExporter
from graphviz import Source, render

from osler.graph import Node
from osler.diagnosis import diagnosable, undiagnosable

class Issue(object):

    def __init__(self, name, description, candidates, severity=0):
        self.name = name.replace(" ", "_")
        self.id = self.name
        self.description = description
        self.candidates = candidates
        self.severity = severity
        self.prevalence = 0.0
        for s in list(self.candidates):
            self.prevalence += s.prevalence
        self.validate()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def parent(self, parent_node):
        return Node(self, parent_node)
    
    def validate(self):
        if not diagnosable(self.candidates):
            raise Exception("Candidate diagnoses must be diagnosable: can't differentiate {}.".format(str(undiagnosable(self.candidates))))
