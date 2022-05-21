'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..palette_manager import PaletteManager

from ..builders.task_builder import TaskBuilder

from ..processors.render_task_processor import RenderTaskProcessor

from ..renderer import Renderer

from ..models.palette import palette_colors


def rotate_rig(angle, verAngle=0, bankedAngle=0, midAngle=0):
    object = bpy.data.objects['Rig']
    if object is None:
        return
    object.rotation_euler = (math.radians(bankedAngle),
                             math.radians(verAngle), math.radians(midAngle - 45))
    vJoint = object.children[0]
    vJoint.rotation_euler = (0, 0, math.radians(angle))


class RCTRender(object):
    def __init__(self):
        self.context = None

        self.task_builder = TaskBuilder()

        self.palette_manager = PaletteManager()

    @classmethod
    def poll(cls, context):
        return 'Rig' in bpy.data.objects is not None

    def create_task(self, context):
        print("This render operator does not setup a task")
        return None

    def execute(self, context):
        general_props = context.scene.rct_graphics_helper_general_properties

        rotate_rig(0, 0, 0, 0)
        bpy.data.cameras["Camera"].ortho_scale = 169.72 / \
            (1920 / context.scene.render.resolution_x)

        bpy.data.cameras["Camera"].shift_x = -0.000345 * \
            96 / context.scene.render.resolution_x

        def finish():
            general_props.rendering = False
            rotate_rig(0, 0, 0, 0)
            print("RCT render has been completed")

        general_props.rendering = True

        if general_props.palette == "CUSTOM":
            colors = []

            i = 0
            for value in general_props.custom_palette_colors:
                if value:
                    colors.append(palette_colors[i])
                i += 1
            self.palette_manager.set_custom_palette(colors)

        render_task_processor = RenderTaskProcessor(
            context, self.palette_manager)

        task = self.create_task(context)

        render_task_processor.process(task, finish)

        return {'FINISHED'}
