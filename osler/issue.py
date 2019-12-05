#!/usr/bin/env python

import logging
log = logging.getLogger(__name__)

from osler.graph import Node
from osler.diagnosis import diagnosable, undiagnosable

class Issue(object):

    def __init__(self, name, candidates, **kwargs):
        self.name = name.replace(" ", "_")
        self.candidates = candidates
        self.metadata = kwargs
        self.validate()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))
    
    def prevalence(self):
        prevalence = 0.0
        for s in list(self.candidates):
            prevalence += s.prevalence
        return prevalence

    def parent(self, parent_node):
        return Node(self, parent_node)
    
    def validate(self):
        if not diagnosable(self.candidates):
            raise Exception("Candidate diagnoses must be diagnosable: can't differentiate {}.".format(str(undiagnosable(self.candidates))))
