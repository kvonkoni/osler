#!/usr/bin/env python3

from typing import List, Set

from .assertion import Assertion
from .common import EntityBase
from .graph import NodeMixin

class Criterion(EntityBase, NodeMixin):

    @classmethod
    def search(cls, assertion: Assertion, truth_value: bool, criterialist: List['Criterion']) -> 'Criterion':
        criterion = Criterion(assertion, truth_value)
        for c in criterialist:
            if c == criterion:
                return c

    def __init__(self, assertion: Assertion, truth_value: bool, **kwargs) -> None:
        super().__init__(assertion.name + '_is_' + str(truth_value))
        self._assertion = assertion
        self._truth_value = truth_value
        self._metadata = kwargs

    def __eq__(self, other) -> bool:
        if isinstance(other, Criterion):
            return self.assertion == other.assertion and (self.truth_value == other.truth_value)
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self._name)
    
    @property
    def assertion(self) -> Assertion:
        return self._assertion
    
    @property
    def truth_value(self) -> bool:
        return self._truth_value

    def opposite(self, other) -> bool:
        return (self.assertion == other.assertion) and (self.truth_value != other.truth_value)

def assertion_set_from_criterion_set(criterion_set: Set[Criterion]) -> Set[Assertion]:
    result = set()
    for c in list(criterion_set):
        result.add(c.assertion)
    return result
