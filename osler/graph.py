#!/usr/bin/env python3

import sys
import logging
log = logging.getLogger(__name__)

import anytree
from anytree.exporter import DotExporter
from ete3 import Tree
from graphviz import render, Source

sys.setrecursionlimit(1500)

class Node(object):

    def __init__(self, object, parent=None):
        self.object = object
        self.anynode = anytree.Node(object.name)
        self.parent = parent
        self.children = []
        self.leaf = True
        if parent:
            self.root = False
            self.parent.leaf = False
            self.parent.children.append(self)
            self.anynode.parent = parent.anynode
            self.etenode = parent.etenode.add_child(name=object.name)
        else:
            self.root = True
            self.anynode.parent = None
            self.etenode = Tree()
    
    def __eq__(self, other):
        if isinstance(self, Node) and isinstance(other, Node):
            return self.object == other.object
    
    def is_equal_to_subtree(self, other):
        if self.path_set() == other.path_set():
            return True
        else:
            return False
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return str(self.object)
    
    def __hash__(self):
        return hash(str(self))
    
    def find_subnodes(self, nodeset):
        nodeset.add(self)
        for c in self.children:
            c.find_subnodes(nodeset)
    
    def leaf_set(self):
        leafset = set()
        nodelist = list(self.node_set())
        for n in nodelist:
            if n.leaf:
                leafset.add(n)
        return leafset

    def node_set(self):
        nodeset = set()
        self.find_subnodes(nodeset)
        return nodeset
    
    def path_set(self):
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
        return pathset

    def render(self):
        print(anytree.RenderTree(self.anynode))

    def to_image(self, filename):
        DotExporter(self.anynode).to_dotfile(filename)
        Source.from_file(filename)
        render("dot", "png", filename)

    def to_png(self, filename):
        DotExporter(self.anynode).to_picture(filename)

    def to_svg(self, filename):
        t = self.etenode
        t.render(filename)

class OslerTree(Node):
    
    def __init__(self, name, root):
        self.name = name.replace(" ", "_")
        self.id = self.name
        self.root = root
        self.tree = {"node":self.root, "children":[]}