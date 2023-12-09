'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math

from .nodes_builder import NodesBuilder


# Builder responsible for creating materials necessary for the rendering process
class MaterialsBuilder(NodesBuilder):

    def __init__(self):
        super().__init__()
        self.prefix = ""
        self.suffix = ""
        return

    def build(self, context):
        self.create_world_position_material(context)

        self.create_recolorable_material("Recolorable 1", (0.1, 0.9, 0.3), 1)
        self.create_recolorable_material("Recolorable 2", (0.9, 0.1, 0.4), 2)
        self.create_recolorable_material("Recolorable 3", (0.9, 0.6, 0), 3)

    def create_recolorable_material(self, name, color, pass_index):
        material = self.create_material(name)

        material.diffuse_color = color
        material.diffuse_intensity = 1

        material.specular_color = (1, 1, 1)
        material.specular_intensity = 1
        material.specular_hardness = 25
        material.specular_shader = "PHONG"
        material.use_fake_user = True

        material.pass_index = pass_index

        return material

    def create_world_position_material(self, context, x_offset=0, y_offset=0):
        material = self.create_material("WorldPosition")

        material.use_nodes = True

        self.init(material.node_tree)

        input_node = self.create_node("ShaderNodeGeometry")

        self.next_column()

        mapping_node = self.create_node("ShaderNodeMapping")
        mapping_node.translation = (8 - x_offset / 4, 8 - y_offset / 4, 0)
        mapping_node.scale = (0.25, 0.25, 0.25)
        mapping_node.use_min = True
        mapping_node.use_max = True
        mapping_node.min = (0, 0, 0)
        mapping_node.max = (16, 16, 16)

        self.link(input_node, 0, mapping_node, 0)

        self.next_column()

        output_node = self.create_node("ShaderNodeOutput")

        self.link(mapping_node, 0, output_node, 0)

        return

    def create_material(self, name):
        name = self.prefix + name + self.suffix

        old_material = bpy.data.materials.get(name)
        if old_material != None:
            old_material.name = "__material_to_replace"

        material = bpy.data.materials.new(name)

        if old_material != None:
            # Replace existing materials with the new one
            for obj in (o for o in bpy.data.objects if hasattr(o, "material_slots")):
                for slot in obj.material_slots:
                    if slot.material.name == old_material.name:
                        slot.material = material

            bpy.data.materials.remove(old_material, do_unlink=True)

        return material
