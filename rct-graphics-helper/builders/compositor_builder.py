'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math

from .nodes_builder import NodesBuilder


# Builder responsible for creating the compositor node graph necessary for the render process's post processing
class CompositorBuilder(NodesBuilder):

    def __init__(self):
        super().__init__()

        self.background_color = (0.041, 0.044, 0.041, 1)
        return

    # Clears the composite nodes and builds the necessary composite node graph for the render process
    def build(self, context):
        context.scene.use_nodes = True

        self.init(context.scene.node_tree)

        # Main input node
        input_layers_node = self.create_node("CompositorNodeRLayers")
        input_layers_node.scene = context.scene
        input_layers_node.layer = "Editor"
        input_layers_node.label = "input_layer"
        input_layers_node.update()
        self.start_branch_point()

        # Removes the transparancy from the anti-aliasing
        mixed_anti_aliased, aa_mask = self.create_background_anti_aliasing_process(
            input_layers_node)

        self.next_process()

        combine_node = self.create_metadata_image(input_layers_node)

        self.link(aa_mask, 0, combine_node, 3)
        
        # Metadata output node
        meta_output_node = self.create_node("CompositorNodeOutputFile")
        meta_output_node.label = "meta_output"
        meta_output_node.format.file_format = "OPEN_EXR"
        meta_output_node.format.color_mode = "RGBA"
        meta_output_node.format.color_depth = "16"
        meta_output_node.file_slots[0].path = "meta_mask"

        # Move to the final output column
        self.exit_branch_point()

        # Main output node
        output_composite_node = self.create_node("CompositorNodeComposite")

        self.link(mixed_anti_aliased, 0, output_composite_node, 0)
        self.link(aa_mask, 0, output_composite_node, 1)


        self.link(combine_node, 0, meta_output_node, 0)

        return

    def create_background_anti_aliasing_process(self, layers_node):
        alpha_remover_node = self.create_node("CompositorNodeAlphaOver")
        alpha_remover_node.use_premultiply = False
        alpha_remover_node.premul = 0
        alpha_remover_node.inputs[1].default_value = self.background_color

        self.link(layers_node, 0, alpha_remover_node, 2)

        alpha_convert_node = self.create_node("CompositorNodePremulKey")
        alpha_convert_node.mapping = "PREMUL_TO_STRAIGHT"

        self.link(layers_node, 0, alpha_convert_node, 0)

        alpha_masking_node = self.create_node("CompositorNodeMath")
        alpha_masking_node.operation = "GREATER_THAN"
        alpha_masking_node.inputs[1].default_value = 0.0

        self.link(layers_node, 1, alpha_masking_node, 0)

        self.next_column()

        alpha_mix_node = self.create_node("CompositorNodeMixRGB")
        alpha_mix_node.blend_type = "MIX"
        alpha_mix_node.inputs[1].default_value = self.background_color

        self.link(alpha_remover_node, 0, alpha_mix_node, 2)
        self.link(alpha_masking_node, 0, alpha_mix_node, 0)

        self.next_column()

        aa_w_bg_switch = self.create_node("CompositorNodeMixRGB")
        aa_w_bg_switch.label = "aa_with_backgound_switch"
        aa_w_bg_switch.blend_type = "MIX"

        self.link(alpha_convert_node, 0, aa_w_bg_switch, 1)
        self.link(alpha_mix_node, 0, aa_w_bg_switch, 2)

        return aa_w_bg_switch, alpha_masking_node

    def create_metadata_image(self, layers_node):
        map_range_node = self.create_node("CompositorNodeMapRange")
        map_range_node.inputs[1].default_value = 0
        map_range_node.inputs[2].default_value = 255
        map_range_node.inputs[3].default_value = 0
        map_range_node.inputs[4].default_value = 1

        self.link(layers_node, 15, map_range_node, 0)

        map_range_node_blue = self.create_node("CompositorNodeMapRange")
        map_range_node_blue.inputs[1].default_value = 0
        map_range_node_blue.inputs[2].default_value = 255
        map_range_node_blue.inputs[3].default_value = 0
        map_range_node_blue.inputs[4].default_value = 1

        self.link(layers_node, 14, map_range_node_blue, 0)

        self.next_column()

        combine_node = self.create_node("CompositorNodeCombRGBA")
        self.link(map_range_node, 0, combine_node, 0)
        self.link(map_range_node_blue, 0, combine_node, 2)

        self.next_column()

        return combine_node
