#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree

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

    def AssertionSet(self):
        result = set()
        for c in self.criteria:
            result.add(c.assertion)
        return result

    def Common(self, other):
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self.criteria):
                for criterionB in list(other.criteria):
                    if criterionA == criterionB:
                        result.add(criterionA.assertion)
            return result
        else:
            raise TypeError("Diagnosis.Common() expected Diagnosis, received {}".format(type(other)))

    def Differential(self, other):
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self.criteria):
                for criterionB in list(other.criteria):
                    if criterionA.Opposite(criterionB):
                        result.add(criterionA.assertion)
            return result
        else:
            raise TypeError("Diagnosis.Common() expected Diagnosis, received {}".format(type(other)))
