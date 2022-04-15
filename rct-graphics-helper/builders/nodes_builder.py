'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math

# Builder for creating node graphs


class NodesBuilder:

    def __init__(self):
        self.init(None)

    def init(self, tree):
        self.horizontal_distance = 300

        self.phase_x = -self.horizontal_distance
        self.phase_y = 0

        self.max_x = 0
        self.max_y = 0

        self.start_x = 0
        self.start_y = 0

        self.reroute_y = 50

        self.branch_stack = []

        if tree != None:
            self.tree = tree
            self.links = tree.links

            # Remove existing nodes
            for node in self.tree.nodes:
                self.tree.nodes.remove(node)

    # Creates a node within the current column
    def create_node(self, type):
        node = self.tree.nodes.new(type=type)
        node.location = self.phase_x, -self.phase_y

        self.phase_y += 250

        if self.max_y < self.phase_y:
            self.max_y = self.phase_y

        return node

    # Moves the pointer to the next column
    def next_column(self):
        self.phase_x += self.horizontal_distance
        self.phase_y = self.start_y

        if self.max_x < self.phase_x:
            self.max_x = self.phase_x

    # Moves the pointer underneath the last branch point
    def next_process(self):
        self.start_y = self.max_y + 250
        self.phase_x = self.start_x
        self.phase_y = self.start_y

        if len(self.branch_stack) > 0 and self.branch_stack[-1][2] == -1:
            self.branch_stack[-1] = (self.branch_stack[-1]
                                     [0], self.branch_stack[-1][1], self.reroute_y)

        self.reroute_y = -self.start_y + 50

    # Starts a new branching point from which multiple processes can be started
    def start_branch_point(self):
        self.next_column()

        self.branch_stack.append(
            (self.start_x, self.start_y, -1))
        self.start_x = self.phase_x
        self.start_y = self.phase_y
        self.max_x = self.start_x
        self.max_y = self.start_y

    # Pops the previous branch point off the stack
    def exit_branch_point(self):
        x, y, rry = self.branch_stack.pop()
        self.start_x = x
        self.start_y = y

        if rry == -1:
            rry = -self.start_y + 50
        self.reroute_y = rry

        self.return_process()
        self.next_column()

    # Moves the pointer to the column behind all the current rows
    def return_process(self):
        self.phase_x = self.max_x
        self.phase_y = self.start_y

    # Links two nodes together, adds reroute nodes if necessary.
    def link(self, nodeA, outIndex, nodeB, inIndex):
        delta = nodeB.location[0] - nodeA.location[0]
        columns = int(delta / self.horizontal_distance)

        if columns <= 1:
            self.links.new(
                nodeA.outputs[outIndex], nodeB.inputs[inIndex])
        else:
            rerouteA = self.tree.nodes.new(type="NodeReroute")
            rerouteA.location = nodeA.location[0] + \
                self.horizontal_distance, self.reroute_y
            self.links.new(
                nodeA.outputs[outIndex], rerouteA.inputs[0])

            rerouteB = self.tree.nodes.new(type="NodeReroute")
            rerouteB.location = nodeB.location[0] - \
                self.horizontal_distance + 100, self.reroute_y

            self.links.new(
                rerouteA.outputs[0], rerouteB.inputs[0])
            self.links.new(
                rerouteB.outputs[0], nodeB.inputs[inIndex])
            self.reroute_y += 50
