#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree

class Issue:
    list = []

    def __init__(self, name, description, candidates, severity=0, parent=None):
        Issue.list.append(self)
        self.name = name
        self.description = description
        self.candidates = candidates
        self.severity = severity
        self.prevalence = 0.0
        for s in list(self.candidates):
            self.prevalence += s.prevalence
        self.node = anytree.Node(self.name)
        self.parent = parent

    def render(self):
        print(anytree.RenderTree(self.node))
