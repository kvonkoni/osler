#!/usr/bin/env python

import anytree
import ete3
from anytree.exporter import DotExporter, JsonExporter
#from ete3 import Tree, TreeStyle, TextFace, add_face_to_node
from ete3 import Tree
from graphviz import render, Source
import sys

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
        if self.path_set() == other.path_set():
            return True
        else:
            return False
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if self.parent:
            return str(self.object)# +"_childof_" + str(self.parent)
        else:
            return str(self.object)# +"_root"
    
    def __hash__(self):
        return hash(str(self))
    
    def find_subnodes(self, nodeset):
        nodeset.add(self)
        #print("node: "+str(self)+"; leaf: "+str(self.leaf)+"; root: "+str(self.root))
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
                path.append(current)
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
        #ts = TreeStyle()
        #ts.show_leaf_name = False
        #def my_layout(node):
        #        F = TextFace(node.name, tight_text=True)
        #        add_face_to_node(F, node, column=0, position="branch-right")
        #ts.layout_fn = my_layout
        #ts.mode = "c"
        #ts.arc_start = 45 # 0 degrees = 3 o'clock
        #ts.arc_span = 135
        #t.render(filename, tree_style=ts)
        t.render(filename)

class OslerTree(object):
    
    def __init__(self, name, root):
        self.name = name.replace(" ", "_")
        self.id = self.name
        self.root = root
        self.tree = {"node":self.root, "children":[]}