#!/usr/bin/env python

#import PyLog
#import PyKnow
#import kanren
import nltk
import anytree
import itertools
from pando.common import Pando
from pando.graph import Node

class Diagnosis(Pando):
    id_iter = itertools.count()
    ID = {}

    @classmethod
    def AddToClass(cls, id, instance):
        cls.ID[id] = instance

    def __init__(self, name, description, remedy, criteria, prevalence=0.0, comorbidity=set(), parent=None):
        self.id = "d"+str(next(self.id_iter))
        self.name = name
        self.description = description
        self.remedy = remedy
        self.criteria = criteria
        self.assertions = self.AssertionSet()
        self.prevalence = prevalence
        self.comorbidity = comorbidity
        self.AddToClass(self.id, self)
        self.AddToGlobal(self.id, self)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Criterion):
            return self.criteria == other.criteria
        else:
            return False

    def __add__(self, other):
        name = self.name+"+"+other.name
        description = self.name+" intersect "+other.name
        remedy = self.name+" remedy and/or "+other.name+" remedy"
        criteria = self.CommonCriteria(other)
        prevalence = self.prevalence+other.prevalence
        comorbidity = self.comorbidity.union(other.comorbidity)
        return Diagnosis(name, description, remedy, criteria, prevalence, comorbidity)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def Parent(self, parent_node):
        return Node(self, parent_node)

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

    def CommonCriteriaAssertions(self, other):
        if isinstance(other, Diagnosis):
            common_criteria = self.CommonCriteria(other)
            common_assertions = set()
            for c in list(common_criteria):
                common_assertions.add(c.assertion)
            return common_assertions
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def NumCommonCriteriaAssertions(self, other):
        if isinstance(other, Diagnosis):
            return len(self.CommonCriteriaAssertions(other))
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

    def NumDifferentialCriteria(self, other):
        if isinstance(other, Diagnosis):
            return len(self.DifferentialCriteria(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def DifferentialAssertions(self, other):
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self.criteria):
                for criterionB in list(other.criteria):
                    if criterionA.Opposite(criterionB):
                        result.add(criterionA.assertion)
                        result.add(criterionB.assertion)
            return result
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def NumDifferentialAssertions(self, other):
        if isinstance(other, Diagnosis):
            return len(self.DifferentialAssertions(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def InconsequentialCriteria(self, other):
        if isinstance(other, Diagnosis):
            return self.criteria.union(other.criteria).difference(self.CommonCriteria(other).union(self.DifferentialCriteria(other)))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

def CompareDiagnoses(diagA, diagB):
    common_criteria = diagA.CommonCriteria(diagB)
    differential_criteria = diagA.DifferentialCriteria(diagB)
    inconsequential_criteria = diagA.InconsequentialCriteria(diagB)
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
