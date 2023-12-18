'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..builders.materials_builder import MaterialsBuilder

from ..builders.scene_builder import SceneBuilder
from ..builders.compositor_builder import CompositorBuilder
from ..res.res import res_path


class Init(bpy.types.Operator):
    bl_idname = "render.rct_init"
    bl_label = "Initialize RCT graphics helper"

    scene = None
    props = None

    def execute(self, context):
        # Setup render settings
        if context.scene.render.resolution_x == 1920 and context.scene.render.resolution_x == 1080:
            context.scene.render.resolution_x = 96
            context.scene.render.resolution_y = 96
        context.scene.render.resolution_percentage = 100

        # Output
        context.scene.render.image_settings.color_depth = "8"
        context.scene.render.image_settings.compression = 0
        context.scene.render.image_settings.color_mode = "RGBA"
        context.scene.render.alpha_mode = "TRANSPARENT"

        # Anti-aliasing
        context.scene.render.use_antialiasing = True
        context.scene.render.pixel_filter_type = "BOX"
        context.scene.render.antialiasing_samples = "5"
        context.scene.render.filter_size = 1.4

        # Create render layers
        editor_layer = self.create_render_layer(context, "Editor")
        editor_layer.layers = (True, False, False, True, True, True, True, True,
                               True, True, True, True, True, True, True, True, True, True, True, True)
        editor_layer.layers_zmask = (True, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False, False)
        editor_layer.use = True

        for i in range(8):
            riders_layer = self.create_render_layer(
                context, "Riders {}".format(i + 1))
            riders_layer.layers = (False, i == 0, i == 1, i == 2, i == 3, i == 4, i == 5, i == 6,
                                   i == 7, False, False, False, False, False, False, False, False, False, False, False)
            riders_layer.layers_zmask = (True, True, True, True, True, True, True, True, True,
                                         True, False, False, False, False, False, False, False, False, False, False)
            riders_layer.use = False

        # Track render layers
        track_layer = self.create_render_layer(context, "Track")
        track_layer.layers = (True, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False, False, False)
        track_layer.layers_zmask = (True, False, True, False, False, False, False, False,
                                    False, False, False, False, False, False, False, False, False, False, False, False)
        track_layer.use = False
        
        track_occluded_layer = self.create_render_layer(context, "Track Occluded")
        track_occluded_layer.layers = (False, True, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False, False, False)
        track_occluded_layer.layers_zmask = (True, False, True, False, False, False, False, False,
                                    False, False, False, False, False, False, False, False, False, False, False, False)
        track_occluded_layer.use = False

        self.delete_default_render_layer(context)

        # Create dependencies in the context
        sceneBuilder = SceneBuilder()
        sceneBuilder.build(context)
        
        bpy.data.cameras["Camera"].shift_x = -0.000345 * \
            96 / context.scene.render.resolution_x
        bpy.data.cameras["Camera"].ortho_scale = 169.72 / \
            (1920 / context.scene.render.resolution_x)

        compositorBuilder = CompositorBuilder()
        compositorBuilder.build(context)

        template_path = os.path.join(res_path, "templates/internal_template.blend")


        material_replacements = []

        with bpy.data.libraries.load(template_path) as (data_from, data_to):
            for material in data_from.materials:
                replacement = {
                    "new": material
                }
                if context.blend_data.materials.get(material) is not None:
                    material_data = context.blend_data.materials.get(material)
                    material_data.name = material + "__DELETE__"
                    replacement["old"] = material_data.name
                material_replacements.append(replacement)
            data_to.materials = data_from.materials

        for material in material_replacements:
            new_mat = context.blend_data.materials.get(material["new"])
            new_mat.use_fake_user = True
            
            if "old" in material:
                old_mat = context.blend_data.materials.get(material["old"])
                for o in bpy.data.objects:
                        for slot in o.material_slots:
                            if slot.material == old_mat:
                                slot.material = new_mat
                if old_mat:
                    context.blend_data.materials.remove(old_mat)
        
        return {'FINISHED'}

    def delete_default_render_layer(self, context):
        layer = context.scene.render.layers.get("RenderLayer")

        if layer != None:
            context.scene.render.layers.remove(layer)

    def create_render_layer(self, context, name):
        old_layer = context.scene.render.layers.get(name)

        if old_layer != None:
            context.scene.render.layers.remove(old_layer)

        layer = context.scene.render.layers.new(name)

        layer.use_pass_combined = True
        layer.use_pass_material_index = True
        layer.use_pass_object_index = True
        layer.use_zmask = True

        return layer
