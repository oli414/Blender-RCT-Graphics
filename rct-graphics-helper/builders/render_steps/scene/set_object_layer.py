'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
from ..render_step import RenderStep

class SetObjectLayer(RenderStep):
    def __init__(self, objects, enable_indices=[], disable_indices=[], overwrite=[]):
        self.objects = objects
        self.enable_indices = enable_indices
        self.disable_indices = disable_indices
        self.overwrite = overwrite

    def execute(self, context, callback):
        for object in self.objects:
            if len(self.overwrite)==20:
                object.layers = self.overwrite
            else:
                for i in self.enable_indices:
                    object.layers[i] = True
                for i in self.disable_indices:
                    object.layers[i] = False
        return True
