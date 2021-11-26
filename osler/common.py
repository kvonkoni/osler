#!/usr/bin/env python3

class EntityBase:

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

    def __repr__(self):
        return self.__str__()
    
    @property
    def name(self) -> str:
        return self._name

class DifferentialDiagnosisError(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)