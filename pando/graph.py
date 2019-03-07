#!/usr/bin/env python

import anytree
import itertools
from pando.common import Pando

class Node(Pando):
    id_iter = itertools.count()
    ID = {}

    def __init__(self, object, parent=None):
        self.id = "n"+str(next(self.id_iter))
        self.object = object.id
        self.node = anytree.Node(object.name)
        self.parent = parent
        Node.ID[self.id] = self
        Pando.ID[self.id] = self

    def Parent(self, parent):
        new_node = Node(parent, )

    def Render(self):
        print(anytree.RenderTree(self.node))

    def To_image(self, filename):
        DotExporter(self.node).to_dotfile(filename)
        Source.from_file(filename)
        render("dot", "png", filename)

    def To_png(self, filename):
        DotExporter(self.node).to_picture(filename)
