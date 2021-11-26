#!/usr/bin/env python3

import sys
from typing import FrozenSet, Set, Tuple

import anytree
from anytree.exporter import DotExporter
from ete3 import Tree
from graphviz import render, Source

from .common import EntityBase

sys.setrecursionlimit(1500)

class Node:

    def __init__(self, object: EntityBase, parent: 'Node'=None) -> None:
        self._object = object
        self._anynode = anytree.Node(object.name)
        self._parent = parent
        self._children = []
        self._leaf = True
        if parent:
            self._root = False
            self._parent._leaf = False
            self._parent._children.append(self)
            self._anynode.parent = parent._anynode
            self._etenode = parent._etenode.add_child(name=object.name)
        else:
            self._root = True
            self._anynode.parent = None
            self._etenode = Tree()
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.object == other.object
        else:
            return self.object == other
    
    def is_equal_to_subtree(self, other: 'Node'):
        return self.path_set() == other.path_set()
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return str(self._object)
    
    def __hash__(self) -> int:
        return hash(self._object)
    
    @property
    def object(self) -> EntityBase:
        return self._object
    
    @property
    def root(self) -> 'Node':
        return self._root
    
    @property
    def parent(self) -> 'Node':
        return self._parent
    
    @property
    def children(self) -> Tuple['Node']:
        return tuple(self._children)
    
    @property
    def leaf(self) -> bool:
        return self._leaf
    
    def find_subnodes(self, nodeset: Set['Node']) -> None:
        nodeset.add(self)
        for c in self._children:
            c.find_subnodes(nodeset)
    
    def leaf_set(self) -> FrozenSet['Node']:
        leafset = set()
        nodelist = list(self.node_set())
        for n in nodelist:
            if n.leaf:
                leafset.add(n)
        return frozenset(leafset)

    def node_set(self) -> FrozenSet['Node']:
        nodeset = set()
        self.find_subnodes(nodeset)
        return frozenset(nodeset)
    
    def path_set(self) -> Tuple['Node']:
        pathset = set()
        leaflist = list(self.leaf_set())
        for l in leaflist:
            path = []
            current = l
            while not current.root:
                path.append(current.object)
                current = current.parent
            pathtuple = tuple(path)
            pathset.add(pathtuple)
        return tuple(pathset)

    def render(self) -> None:
        print(anytree.RenderTree(self._anynode))

    def to_image(self, filename: str) -> None:
        DotExporter(self._anynode).to_dotfile(filename)
        Source.from_file(filename)
        render("dot", "png", filename)

    def to_png(self, filename: str) -> None:
        DotExporter(self._anynode).to_picture(filename)

    def to_svg(self, filename: str) -> None:
        t = self._etenode
        t.render(filename)

class NodeMixin:

    def parent(self, parent_node: Node) -> Node:
        return Node(self, parent_node)