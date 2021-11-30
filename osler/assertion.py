#!/usr/bin/env python3

from .common import EntityBase
from .graph import NodeMixin

class Assertion(EntityBase, NodeMixin):

    def __init__(self, proposition: str, test_difficulty: float=0.0, **kwargs) -> None:
        super().__init__(proposition.replace(" ", "_"))
        self._proposition = proposition
        self._test_difficulty = test_difficulty
        self._metadata = kwargs

    def __eq__(self, other: 'Assertion') -> bool:
        if isinstance(other, Assertion):
            return self._proposition == other._proposition
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self._name)
    
    @property
    def proposition(self) -> str:
        return self._proposition
    
    @property
    def test_difficulty(self) -> float:
        return self._test_difficulty