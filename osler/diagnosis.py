#!/usr/bin/env python3

from typing import Set, FrozenSet

from .assertion import Assertion
from .common import EntityBase, NodeMixin
from .criterion import Criterion

class Diagnosis(EntityBase, NodeMixin):

    def __init__(self, name: str, criteria: Set[Criterion], prevalence: float=0.0, **kwargs) -> None:
        super().__init__(name.replace(" ", "_"))
        self._criteria = frozenset(criteria)
        self._assertions = frozenset(self.assertion_set())
        self._prevalence = prevalence
        self._metadata = kwargs

    def __eq__(self, other: 'Diagnosis') -> bool:
        if isinstance(other, Diagnosis):
            return self._criteria == other._criteria
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self._criteria)

    def __add__(self, other: 'Diagnosis') -> 'Diagnosis':
        name = self._name + "+" + other._name
        criteria = self.common_criteria(other)
        prevalence = self._prevalence + other._prevalence
        return Diagnosis(name, criteria, prevalence)

    def __radd__(self, other: 'Diagnosis') -> 'Diagnosis':
        return self.__add__(other)
    
    @property
    def criteria(self) -> FrozenSet[Criterion]:
        return self._criteria
    
    @property
    def assertions(self) -> FrozenSet[Assertion]:
        return self._assertions
    
    @property
    def prevalence(self) -> float:
        return self._prevalence

    def info(self) -> None:
        print("{{Diagnosis name: {}".format(self._name))
        print("  The criteria for this diagnosis are:")
        for c in list(self._criteria):
            print("    " + c.name)
        print("}")

    def assertion_set(self) -> Set[Assertion]:
        result = set()
        for c in list(self._criteria):
            result.add(c.assertion)
        return result

    def common_criteria(self, other: 'Diagnosis') -> Set[Criterion]:
        if isinstance(other, Diagnosis):
            return self._criteria.intersection(other.criteria)
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def common_criteria_assertions(self, other: 'Diagnosis') -> Set[Assertion]:
        if isinstance(other, Diagnosis):
            common_criteria = self.common_criteria(other)
            common_assertions = set()
            for c in list(common_criteria):
                common_assertions.add(c.assertion)
            return common_assertions
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def num_common_criteria_assertions(self, other: 'Diagnosis') -> int:
        if isinstance(other, Diagnosis):
            return len(self.common_criteria_assertions(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def differential_criteria(self, other: 'Diagnosis') -> Set[Criterion]:
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self._criteria):
                for criterionB in list(other.criteria):
                    if criterionA.opposite(criterionB):
                        result.add(criterionA)
                        result.add(criterionB)
            return result
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def num_differential_criteria(self, other: 'Diagnosis') -> int:
        if isinstance(other, Diagnosis):
            return len(self.differential_criteria(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def differential_assertions(self, other: 'Diagnosis') -> Set[Assertion]:
        if isinstance(other, Diagnosis):
            result = set()
            for criterionA in list(self._criteria):
                for criterionB in list(other.criteria):
                    if criterionA.opposite(criterionB):
                        result.add(criterionA.assertion)
                        result.add(criterionB.assertion)
            return result
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def num_differential_assertions(self, other: 'Diagnosis') -> int:
        if isinstance(other, Diagnosis):
            return len(self.differential_assertions(other))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

    def inconsequential_criteria(self, other: 'Diagnosis') -> Set[Criterion]:
        if isinstance(other, Diagnosis):
            return self.criteria.union(other.criteria).difference(self.common_criteria(other).union(self.differential_criteria(other)))
        else:
            raise TypeError("expected Diagnosis object, received {}".format(type(other)))

def compare_diagnoses(diagA: 'Diagnosis', diagB: 'Diagnosis') -> None:
    common_criteria = diagA.common_criteria(diagB)
    differential_criteria = diagA.differential_criteria(diagB)
    inconsequential_criteria = diagA.inconsequential_criteria(diagB)
    print("{{Comparison of {} and {} criteria:".format(diagA.name, diagB.name))
    print("    Common Criteria:")
    for c in list(common_criteria):
        print("        " + c.name)
    print("    Differential Criteria:")
    for d in list(differential_criteria):
        print("        " + d.name)
    print("    Inconsequential Criteria:")
    for i in list(inconsequential_criteria):
        print("        " + i.name)
    print("}")

def diagnosable(diagnosis_set: Set['Diagnosis']) -> bool:
    if len(diagnosis_set) < 2:
        return False
    diagnosis_list = list(diagnosis_set)
    num_diagnoses = len(diagnosis_set)
    for i in range(num_diagnoses):
        for j in range(i+1, num_diagnoses):
            if not diagnosis_list[i].differential_assertions(diagnosis_list[j]):
                return False
    return True

def undiagnosable(diagnosis_set: Set['Diagnosis']) -> Set['str']:
    if len(diagnosis_set) < 2:
        return diagnosis_set
    undiagnosable = set()
    diagnosis_list = list(diagnosis_set)
    num_diagnoses = len(diagnosis_set)
    for i in range(num_diagnoses):
        for j in range(i+1, num_diagnoses):
            if not diagnosis_list[i].differential_assertions(diagnosis_list[j]):
                undiagnosable.add(diagnosis_list[i])
                undiagnosable.add(diagnosis_list[j])
    print(undiagnosable)
    return undiagnosable