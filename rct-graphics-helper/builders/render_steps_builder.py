'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from ..builders.render_steps.scene.set_object_layer import SetObjectLayer
from ..builders.render_steps.scene.set_visibility import SetVisibility
from ..builders.render_steps.scene.move_rig import MoveRig
from ..builders.render_steps.cache_output import CacheOutput
from ..builders.render_steps.render_tile_indices import RenderTileIndices
from ..builders.render_steps.select_tiles import SelectTiles
from ..builders.render_steps.copy_alpha import CopyAlpha
from ..builders.render_steps.set_layer import SetLayer
from ..builders.render_steps.reset_renderer import ResetRenderer
from ..builders.render_steps.quantize import Quantize
from ..builders.render_steps.render_scene import RenderScene
from ..builders.render_steps.output import Output
from ..render_task import RenderTask

# Builder for creating render tasks procedurally

class RenderStepsBuilder:
    def __init__(self):
        self.steps = []

        self.previous_output = None

        self.i = 0

    def _gen_index(self):
        self.i += 1
        return "{}".format(self.i)
    
    def move_rig(self, view_angle, x=0, y=0, z=0):
        step = MoveRig(view_angle, x, y, z)
        self.steps.append(step)
        return self
    
    def set_visibility(self, objects, hide_render):
        step = SetVisibility(objects, hide_render)
        self.steps.append(step)
        return self
    
    def overwrite_object_layers(self, objects, overwrite):
        step = SetObjectLayer(objects, [], [], overwrite)
        self.steps.append(step)
        return self
    
    def set_object_layers(self, objects, enable_indices, disable_indices):
        step = SetObjectLayer(objects, enable_indices, disable_indices)
        self.steps.append(step)
        return self
    
    def get_output(self):
        return self.previous_output

    def set_input(self, input):
        self.previous_output = input
        return self

    def reset_renderer(self):
        self.steps.append(ResetRenderer())
        return self
    
    def set_layer(self, layer):
        self.steps.append(SetLayer(layer))
        return self
    
    def cache_output(self, exr):
        step = CacheOutput(self.previous_output, self._gen_index(), exr)
        self.steps.append(step)
        self.previous_output = step.output
        return self
    
    def render_scene_with_meta(self, render_props):
        step = RenderScene(self._gen_index(), render_props, True)
        self.steps.append(step)
        self.previous_output = step.output
        return step.meta_output

    def render_scene(self, render_props):
        step = RenderScene(self._gen_index(), render_props)
        self.steps.append(step)
        self.previous_output = step.output
        return self
    
    def copy_alpha(self, mask_input, inverted=False):
        step = CopyAlpha(self.previous_output, mask_input, inverted)
        self.steps.append(step)
        self.previous_output = step.output
        return self
    
    def quantize(self, palette, meta_input=None, recolorables=0):
        step = Quantize(self.previous_output, palette, meta_input, recolorables)
        self.steps.append(step)
        self.previous_output = step.output
        return self
    
    def render_tile_indices(self, render_props, width, length, offset_x=0, offset_y=0):
        step = RenderTileIndices(self._gen_index(), render_props, width, length, offset_x, offset_y)
        self.steps.append(step)
        self.previous_output = step.output
        return self
    
    def select_tiles(self, tile_meta_input, tiles):
        step = SelectTiles(self.previous_output, tile_meta_input, tiles)
        self.steps.append(step)
        self.previous_output = step.output
        return self

    def output(self, index=-1, offset_x=0, offset_y=0):
        self.steps.append(Output(self.previous_output, index, offset_x, offset_y))
        return self

    def create_task(self, context):
        task = RenderTask(context)
        task.steps = self.steps
        self.steps = []
        return task



