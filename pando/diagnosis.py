#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from pando.assertion import IsEquivalent

class Diagnosis:
    list = []

    def __init__(self, name, description, remedy, criteria, prevalence=0.0, comorbidity=[], parent=None):
        Diagnosis.list.append(self)
        self.name = name
        self.description = description
        self.remedy = remedy
        self.criteria = criteria
        self.prevalence = prevalence
        self.comorbidity = comorbidity
        self.node = anytree.Node(self.name)
        self.parent = parent

    def info(self):
        print("{{Diagnosis description: {}".format(self.description))
        print("  The criteria for this diagnosis are:")
        for c in list(self.criteria):
            print("    "+c.name)
        print("  The remedy for this diagnosis is: {}".format(self.remedy))
        print("}")

def AssertionSet(diagnosis):
    result = set()
    for c in diagnosis.criteria:
        result.add(c.assertion)
    return result

def DifferentialCriteria(diagnosisA, diagnosisB):
    result = set()
    for criterionA in list(diagnosisA.criteria):
        for criterionB in list(diagnosisB.criteria):
            if IsEquivalent(criterionA.assertion, criterionB.assertion) and (criterionA.truth_value != criterionB.truth_value):
                result.add(criterionA)
                result.add(criterionB)
    return result
