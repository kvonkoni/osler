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
        self.assertions = self.AssertionSet()
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
        for c in list(self.criteria):
            result.add(c.assertion)
        return result

    def CommonCriteria(self, other):
        if isinstance(other, Diagnosis):
            return self.criteria.intersection(other.criteria)
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def DifferentialCriteria(self, other):
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self.criteria):
                for criterionB in list(other.criteria):
                    if criterionA.Opposite(criterionB):
                        result.add(criterionA)
                        result.add(criterionB)
            return result
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def InconsequentialCriteria(self, other):
        if isinstance(other, Diagnosis):
            return self.criteria.union(other.criteria).difference(self.CommonCriteria(other).union(self.DifferentialCriteria(other)))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

def CompareDiagnoses(diagA, diagB):
    common_criteria = diagA.CommonCriteria(diagB)#diagA.criteria.intersection(diagB.criteria)
    differential_criteria = diagA.DifferentialCriteria(diagB)
    inconsequential_criteria = diagA.InconsequentialCriteria(diagB)
    print("{{Comparison of {} and {} criteria:".format(diagA.name, diagB.name))
    print("    Common Criteria:")
    for c in list(common_criteria):
        print("        "+c.name)
    print("    Differential Criteria:")
    for d in list(differential_criteria):
        print("        "+d.name)
    print("    Inconsequential Criteria")
    for i in list(inconsequential_criteria):
        print("        "+i.name)
    print("}")
