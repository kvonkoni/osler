#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from anytree.exporter import DotExporter
from graphviz import Source, render
import itertools

class Issue:
    newid = itertools.count().next
    list = []

    def __init__(self, name, description, candidates, severity=0, parent=None):
        Issue.list.append(self)
        self.id = resource_cl.newid()
        self.name = name
        self.description = description
        self.candidates = candidates
        self.severity = severity
        self.prevalence = 0.0
        for s in list(self.candidates):
            self.prevalence += s.prevalence
        self.node = anytree.Node(self.name)
        self.parent = parent

    def __str__(self):
        return self.name

    def Parent(self, parent):
        self.parent = parent
        self.node.parent = parent.node

    def Render(self):
        print(anytree.RenderTree(self.node))

    def To_image(self, filename):
        DotExporter(self.node).to_dotfile(filename)
        Source.from_file(filename)
        render("dot", "png", filename)

    def To_png(self, filename):
        DotExporter(self.node).to_picture(filename)
