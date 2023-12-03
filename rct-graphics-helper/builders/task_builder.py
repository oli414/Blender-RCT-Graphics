'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from operator import length_hint
from ..frame import Frame
from ..render_task import RenderTask

# Builder for creating render tasks procedurally


class TaskBuilder:

    # Builder class for creating render tasks
    def __init__(self):
        self.angles = []

        self.view_angle = 0
        self.bank_angle = 0
        self.vertical_angle = 0
        self.mid_angle = 0

        self.width = 1
        self.length = 1

        self.invert_tile_positions = False

        self.use_anti_aliasing = True
        self.anti_alias_with_background = False
        self.maintain_aliased_silhouette = True

        self.output_index = 0

        self.recolorables = 0

        self.layer = "Editor"

        self.palette = None

        self.offset_x = 0
        self.offset_y = 0

        self.occlusion_layers = 0

        self.task = RenderTask(None)

    def set_output_index(self, output_index):
        self.output_index = output_index

    def set_offset(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

    # Adds render angles for the given number of viewing angles relative to the currently configured rotation
    def add_viewing_angles(self, number_of_viewing_angles, animation_frame_index=0, animation_frames=1):

        start_output_index = self.output_index
        for i in range(number_of_viewing_angles):
            for j in range(animation_frames):
                angle = 360 / number_of_viewing_angles * i

                frame_index = start_output_index + i * animation_frames + j
                frame = Frame(frame_index, self.task, angle + self.view_angle,
                              self.bank_angle, self.vertical_angle, self.mid_angle)
                frame.set_multi_tile_size(self.width, self.length, self.invert_tile_positions)

                frame.set_offset(self.offset_x, self.offset_y)

                frame.set_recolorables(self.recolorables)

                frame.set_layer(self.layer)

                frame.set_base_palette(self.palette)

                frame.set_anti_aliasing_with_background(
                    self.use_anti_aliasing, self.anti_alias_with_background, self.maintain_aliased_silhouette)

                frame.animation_frame_index = animation_frame_index + j

                frame.set_occlusion_layers(self.occlusion_layers)

                if self.occlusion_layers > 0:
                    output_indices = []
                    for k in range(self.occlusion_layers):
                        output_indices.append(
                            start_output_index + k * animation_frames * number_of_viewing_angles + j * number_of_viewing_angles + i)
                    frame.set_output_indices(output_indices)

                if frame.oversized:
                    output_indices = []
                    for k in range(frame.width * frame.length):
                        tile_index = k
                        if frame.invert_tile_positions:
                            tile_index = (frame.width * frame.length - k - 1)
                        output_indices.append(
                            start_output_index + tile_index * animation_frames * number_of_viewing_angles + j * number_of_viewing_angles + i)
                        
                    frame.set_output_indices(output_indices)

                self.angles.append(frame)

        frames = number_of_viewing_angles * \
            animation_frames * self.width * self.length
        if self.occlusion_layers > 0:
            frames *= self.occlusion_layers
            
        self.output_index += frames

    # Sets the number of recolorable materials
    def set_recolorables(self, number_of_recolorables):
        self.recolorables = number_of_recolorables

    # Sets the base palette to use
    def set_palette(self, palette):
        self.palette = palette

    # Sets the layer to render
    def set_layer(self, layer_name):
        self.layer = layer_name

    # Sets the anti-aliasing parameters
    def set_anti_aliasing_with_background(self, use_anti_aliasing, anti_alias_with_background, maintain_aliased_silhouette):
        self.use_anti_aliasing = use_anti_aliasing

        # No need to anti-alias with background if anti-aliasing is disabled
        self.anti_alias_with_background = anti_alias_with_background and use_anti_aliasing

        # Always maintain aliased silhouttes when anti-aliasing with the background is disabled
        self.maintain_aliased_silhouette = ((
            not anti_alias_with_background) or maintain_aliased_silhouette) and use_anti_aliasing

    # Sets the size of the render in tiles
    def set_size(self, width, length, invert_tile_positions):
        self.width = width
        self.length = length
        self.invert_tile_positions = invert_tile_positions

    # Sets the rotation applied to future render angles
    def set_rotation(self, view_angle, bank_angle=0, vertical_angle=0, mid_angle=0):
        self.view_angle = view_angle
        self.bank_angle = bank_angle
        self.vertical_angle = vertical_angle
        self.mid_angle = mid_angle

    # Resets the rotation applied to future render angles
    def reset_rotation(self):
        self.view_angle = 0
        self.bank_angle = 0
        self.vertical_angle = 0
        self.mid_angle = 0

    # Sets the number of occlusion layers
    def set_occlusion_layers(self, layers):
        self.occlusion_layers = layers

    # Creates a render task with the supplied angles. Clears the buffer for reuse of the task builder
    def create_task(self, context):
        task = self.task
        task.context = context
        task.frames = self.angles
        self.clear()
        return task

    def clear(self):
        self.angles = []

        self.width = 1
        self.length = 1

        self.set_offset(0, 0)

        self.set_occlusion_layers(0)

        self.recolorables = 0

        self.task = RenderTask(None)

        self.reset_rotation()
