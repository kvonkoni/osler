#!/usr/bin/env python

class Pando:
    ID = {}

    @classmethod
    def AddToGlobal(cls, id, instance):
        cls.ID[id] = instance
