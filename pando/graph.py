#!/usr/bin/env python

import anytree
import ete3
from anytree.exporter import DotExporter
import itertools
from ete3 import TreeStyle, TextFace, add_face_to_node

from pando.common import Pando

class Node(Pando):
    id_iter = itertools.count()
    ID = {}

    def __init__(self, object, parent=None):
        self.id = "n"+str(next(self.id_iter))
        self.object = object.id
        self.node = anytree.Node(object.name)
        if parent:
            self.node.parent = parent.node
            self.etenode = parent.etenode.add_child(name=object.name)
        else:
            self.node.parent = None
            self.etenode = None
        self.parent = parent
        Node.ID[self.id] = self
        Pando.ID[self.id] = self

    def Child(self, child):
        new_node = Node(child, )

    def Render(self):
        print(anytree.RenderTree(self.node))

    def To_image(self, filename):
        DotExporter(self.node).to_dotfile(filename)
        Source.from_file(filename)
        render("dot", "png", filename)

    def To_png(self, filename):
        DotExporter(self.node).to_picture(filename)

    def To_svg(self, filename):
        t = self.etenode
        ts = TreeStyle()
        ts.show_leaf_name = False
        def my_layout(node):
                F = TextFace(node.name, tight_text=True)
                add_face_to_node(F, node, column=0, position="branch-right")
        ts.layout_fn = my_layout
        ts.mode = "c"
        ts.arc_start = 45 # 0 degrees = 3 o'clock
        ts.arc_span = 135
        t.render(filename, tree_style=ts)
