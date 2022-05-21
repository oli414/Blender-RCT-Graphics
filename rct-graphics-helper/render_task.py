'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import os

# A collection of frames that are to be rendered and processed


class RenderTask:
    def __init__(self, context):
        self.context = context
        self.frames = []
        self.output_info = []

    def get_temporary_output_folder(self):
        return os.path.join(self.get_output_folder(), ".temp")

    def get_output_folder(self):
        return os.path.join(bpy.path.abspath(self.context.scene.rct_graphics_helper_general_properties.output_directory))

    def add_frame(self, frame):
        self.frames.append(frame)
