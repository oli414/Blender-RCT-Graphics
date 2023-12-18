'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from .render_step import RenderStep

class SetAnimationFrame(RenderStep):
    def __init__(self, animation_frame_index):
        self.animation_frame_index = animation_frame_index

    def execute(self, context, callback):
        context.renderer.set_animation_frame(self.animation_frame_index)
        return True

