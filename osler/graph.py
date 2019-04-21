#!/usr/bin/env python

import anytree
import ete3
from anytree.exporter import DotExporter, JsonExporter
#from ete3 import Tree, TreeStyle, TextFace, add_face_to_node
from ete3 import Tree
from graphviz import render, Source

class Node(object):

    def __init__(self, object, parent=None):
        self.object = object
        self.anynode = anytree.Node(object.name)
        if parent:
            self.anynode.parent = parent.anynode
            self.etenode = parent.etenode.add_child(name=object.name)
        else:
            self.anynode.parent = None
            self.etenode = Tree()
        self.parent = parent

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
    
    def __init__(self, name):
        self.name = name.replace(" ", "_")
        self.id = self.name
        self.tree = {"id":self.id, "children":[]}
    
    def add_child(self, child):
        dict = {"id":child.id, "children":[]}
        self.tree["children"].append(dict)