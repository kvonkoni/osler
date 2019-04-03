#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
from osler.graph import Node

class Diagnosis(object):

    def __init__(self, name, description, remedy, criteria, prevalence=0.0, comorbidity=set()):
        self.name = name
        self.description = description
        self.remedy = remedy
        self.criteria = criteria
        self.assertions = self.assertion_set()
        self.prevalence = prevalence
        self.comorbidity = comorbidity

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Diagnosis):
            return self.criteria == other.criteria
        else:
            return False

    def __add__(self, other):
        name = self.name+"+"+other.name
        description = self.name+" intersect "+other.name
        remedy = self.name+" remedy and/or "+other.name+" remedy"
        criteria = self.common_criteria(other)
        prevalence = self.prevalence+other.prevalence
        comorbidity = self.comorbidity.union(other.comorbidity)
        return Diagnosis(name, description, remedy, criteria, prevalence, comorbidity)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def parent(self, parent_node):
        return Node(self, parent_node)

    def info(self):
        print("{{Diagnosis description: {}".format(self.description))
        print("  The criteria for this diagnosis are:")
        for c in list(self.criteria):
            print("    "+c.name)
        print("  The remedy for this diagnosis is: {}".format(self.remedy))
        print("}")

    def assertion_set(self):
        result = set()
        for c in list(self.criteria):
            result.add(c.assertion)
        return result

    def common_criteria(self, other):
        if isinstance(other, Diagnosis):
            return self.criteria.intersection(other.criteria)
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def common_criteria_assertions(self, other):
        if isinstance(other, Diagnosis):
            common_criteria = self.common_criteria(other)
            common_assertions = set()
            for c in list(common_criteria):
                common_assertions.add(c.assertion)
            return common_assertions
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def num_common_criteria_assertions(self, other):
        if isinstance(other, Diagnosis):
            return len(self.common_criteria_assertions(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def differential_criteria(self, other):
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self.criteria):
                for criterionB in list(other.criteria):
                    if criterionA.opposite(criterionB):
                        result.add(criterionA)
                        result.add(criterionB)
            return result
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def num_differential_criteria(self, other):
        if isinstance(other, Diagnosis):
            return len(self.differential_criteria(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def differential_assertions(self, other):
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self.criteria):
                for criterionB in list(other.criteria):
                    if criterionA.opposite(criterionB):
                        result.add(criterionA.assertion)
                        result.add(criterionB.assertion)
            return result
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def num_differential_assertions(self, other):
        if isinstance(other, Diagnosis):
            return len(self.differential_assertions(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def inconsequential_criteria(self, other):
        if isinstance(other, Diagnosis):
            return self.criteria.union(other.criteria).difference(self.common_criteria(other).union(self.differential_criteria(other)))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

def compare_diagnoses(diagA, diagB):
    common_criteria = diagA.common_criteria(diagB)
    differential_criteria = diagA.differential_criteria(diagB)
    inconsequential_criteria = diagA.inconsequential_criteria(diagB)
    print("{{Comparison of {} and {} criteria:".format(diagA.name, diagB.name))
    print("    Common Criteria:")
    for c in list(common_criteria):
        print("        "+c.name)
    print("    Differential Criteria:")
    for d in list(differential_criteria):
        print("        "+d.name)
    print("    Inconsequential Criteria:")
    for i in list(inconsequential_criteria):
        print("        "+i.name)
    print("}")
