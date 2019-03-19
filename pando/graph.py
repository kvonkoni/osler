#!/usr/bin/env python

import anytree
import ete3
from anytree.exporter import DotExporter
from ete3 import Tree, TreeStyle, TextFace, add_face_to_node

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

    def Child(self, child):
        new_node = Node(child, )

    def Render(self):
        print(anytree.RenderTree(self.anynode))

    def To_image(self, filename):
        DotExporter(self.anynode).to_dotfile(filename)
        Source.from_file(filename)
        render("dot", "png", filename)

    def To_png(self, filename):
        DotExporter(self.anynode).to_picture(filename)

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
