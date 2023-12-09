'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
from ..render_step import RenderStep

class SetVisibility(RenderStep):
    def __init__(self, objects, hide_render):
        self.objects = objects
        self.hide_render = hide_render

    def execute(self, context, callback):
        for object in self.objects:
            object.hide_render = self.hide_render
        return True
