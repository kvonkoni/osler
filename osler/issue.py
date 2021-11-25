#!/usr/bin/env python3

from .common import EntityBase, NodeMixin
from .diagnosis import diagnosable, undiagnosable

class Issue(EntityBase, NodeMixin):

    def __init__(self, name, candidates, **kwargs):
        self.name = name.replace(" ", "_")
        self.candidates = candidates
        self.metadata = kwargs
        self.validate()
    
    def prevalence(self):
        prevalence = 0.0
        for s in list(self.candidates):
            prevalence += s.prevalence
        return prevalence
    
    def validate(self):
        if not diagnosable(self.candidates):
            raise Exception("Candidate diagnoses must be diagnosable: can't differentiate {}.".format(str(undiagnosable(self.candidates))))
