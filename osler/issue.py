#!/usr/bin/env python3

from .common import DifferentialDiagnosisError, EntityBase
from .diagnosis import Diagnosis, diagnosable, undiagnosable
from .graph import NodeMixin

class Issue(EntityBase, NodeMixin):

    def __init__(self, name: str, candidates: Diagnosis, **kwargs) -> None:
        super().__init__(name.replace(" ", "_"))
        self.candidates = candidates
        self.metadata = kwargs
        self.validate()
    
    def prevalence(self) -> float:
        prevalence = 0.0
        for s in list(self.candidates):
            prevalence += s.prevalence
        return prevalence
    
    def validate(self) -> None:
        if not diagnosable(self.candidates):
            raise DifferentialDiagnosisError("Candidate diagnoses must be diagnosable: can't differentiate {}.".format(str(undiagnosable(self.candidates))))
