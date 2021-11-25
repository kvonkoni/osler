#!/usr/bin/env python3

from .graph import Node

class NodeMixin:

    def parent(self, parent_node):
        return Node(self, parent_node)

class EntityBase:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))