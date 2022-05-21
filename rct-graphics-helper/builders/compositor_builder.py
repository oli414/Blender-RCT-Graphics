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

        # Move to the final output column
        self.exit_branch_point()

        self.link(aa_mask, 0, combine_node, 3)

        # Main output node
        output_composite_node = self.create_node("CompositorNodeComposite")

        self.link(mixed_anti_aliased, 0, output_composite_node, 0)
        self.link(aa_mask, 0, output_composite_node, 1)

        # Metadata output node
        meta_output_node = self.create_node("CompositorNodeOutputFile")
        meta_output_node.label = "meta_output"
        meta_output_node.format.file_format = "OPEN_EXR"
        meta_output_node.format.color_mode = "RGBA"
        meta_output_node.format.color_depth = "16"
        meta_output_node.file_slots[0].path = "meta_mask"

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

        alpha_convert_node = self.create_node("CompositorNodePremulKey")
        alpha_convert_node.mapping = "PREMUL_TO_STRAIGHT"

        self.link(layers_node, 0, alpha_convert_node, 0)

        self.next_column()

        seperate_rgba_node = self.create_node("CompositorNodeSepRGBA")

        self.link(alpha_convert_node, 0, seperate_rgba_node, 0)

        self.start_branch_point()

        width_node, rounded_x_node = self.create_calculate_axis(
            "width", seperate_rgba_node, 1)

        self.next_process()

        height_node, rounded_y_node = self.create_calculate_axis(
            "length", seperate_rgba_node, 0)

        self.exit_branch_point()

        stride_node = self.create_node("CompositorNodeMath")
        stride_node.operation = "MULTIPLY"

        self.link(width_node, 0, stride_node, 0)
        self.link(rounded_y_node, 0, stride_node, 1)

        self.next_column()

        tile_index_node = self.create_node("CompositorNodeMath")
        tile_index_node.operation = "ADD"

        self.link(rounded_x_node, 0, tile_index_node, 0)
        self.link(stride_node, 0, tile_index_node, 1)

        self.next_column()

        map_range_node2 = self.create_node("CompositorNodeMapRange")
        map_range_node2.inputs[1].default_value = 0
        map_range_node2.inputs[2].default_value = 255
        map_range_node2.inputs[3].default_value = 0
        map_range_node2.inputs[4].default_value = 1

        self.link(tile_index_node, 0, map_range_node2, 0)

        self.next_column()

        combine_node = self.create_node("CompositorNodeCombRGBA")
        self.link(map_range_node, 0, combine_node, 0)
        self.link(map_range_node2, 0, combine_node, 1)
        self.link(map_range_node_blue, 0, combine_node, 2)

        self.next_process()

        return combine_node

    def create_calculate_axis(self, label, seperate_rgba, seperate_rgba_output_index):
        input_node = self.create_node("CompositorNodeValue")
        input_node.label = label
        input_node.outputs[0].default_value = 2

        self.next_column()

        half_node = self.create_node("CompositorNodeMath")
        half_node.operation = "MULTIPLY"
        half_node.inputs[1].default_value = 0.5

        self.link(input_node, 0, half_node, 0)

        self.next_column()

        min_node = self.create_node("CompositorNodeMath")
        min_node.operation = "SUBTRACT"
        min_node.inputs[0].default_value = 8

        max_node = self.create_node("CompositorNodeMath")
        max_node.operation = "ADD"
        max_node.inputs[0].default_value = 8

        size_plus_half_node = self.create_node("CompositorNodeMath")
        size_plus_half_node.operation = "SUBTRACT"
        size_plus_half_node.inputs[1].default_value = 0.50001

        self.link(half_node, 0, min_node, 1)
        self.link(half_node, 0, max_node, 1)
        self.link(input_node, 0, size_plus_half_node, 0)

        self.next_column()

        map_range_node = self.create_node("CompositorNodeMapRange")
        map_range_node.inputs[3].default_value = -0.49999
        map_range_node.use_clamp = True

        self.link(seperate_rgba, seperate_rgba_output_index, map_range_node, 0)
        self.link(min_node, 0, map_range_node, 1)
        self.link(max_node, 0, map_range_node, 2)
        self.link(size_plus_half_node, 0, map_range_node, 4)

        self.next_column()

        round_node = self.create_node("CompositorNodeMath")
        round_node.operation = "ROUND"

        self.link(map_range_node, 0, round_node, 0)

        return input_node, round_node
