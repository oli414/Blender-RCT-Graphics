'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''


import bpy
import os
import shutil
import json
import zipfile
from collections import OrderedDict

from .sub_processor import SubProcessor

from .frame_processors.post_processor import PostProcessor
from .frame_processors.merge_masks_processor import MergeMasksProcessor
from .frame_processors.render_processor import RenderProcessor
from .frame_processors.tile_indices_render_processor import TileIndicesRenderProcessor
from ...renderer import Renderer

# Context container for the render task process


class SpriteProcessContext:
    def __init__(self, master_context, final_callback):
        self.master_context = master_context
        self.task = master_context.task
        self.frame_index = 0
        self.sub_process_index = 0
        self.final_callback = final_callback

# Renders and post processes the sprites for a render task


class SpriteProcessor(SubProcessor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

        self.processes = [
            RenderProcessor(self.renderer),
            TileIndicesRenderProcessor(self.renderer, False),
            TileIndicesRenderProcessor(self.renderer, True),
            MergeMasksProcessor(self.renderer),
            PostProcessor(self.renderer)
        ]

        self.prioritize_final_output = True
        self.cleanup_afterwards = True

    def process(self, master_context, callback):
        def finalize(task_process_context):
            self._finalize(task_process_context)

            if callback != None:
                callback()

        if not os.path.exists(master_context.task.get_output_folder()):
            os.mkdir(master_context.task.get_output_folder())

        if not os.path.exists(os.path.join(master_context.task.get_output_folder(), "sprites")):
            os.mkdir(os.path.join(
                master_context.task.get_output_folder(), "sprites"))

        task_process_context = SpriteProcessContext(master_context, finalize)

        self._step(task_process_context)

    def _step(self, task_process_context):
        while task_process_context.sub_process_index < len(self.processes) and task_process_context.frame_index < len(task_process_context.task.frames):
            current_process = self.processes[task_process_context.sub_process_index]
            current_frame = task_process_context.task.frames[task_process_context.frame_index]

            is_async = current_process.is_async
            frame_process_callback = None

            # Set a callback to restart the task processor if the sub process is async
            if is_async:
                def continue_process():
                    self._step(task_process_context)
                frame_process_callback = continue_process

            print("Starting process: {}".format(
                type(current_process).__name__))
            current_process.process(current_frame, frame_process_callback)
            print("Finished process: {}".format(
                type(current_process).__name__))

            self._proceed_task_process_context(task_process_context)

            print("Progress: {}%".format(
                round(self._get_progress(task_process_context) * 100)))

            # Exit this function if the sub process is async, the callback restarts it when the subprocess is ready
            if is_async:
                return

        if task_process_context.final_callback != None:
            task_process_context.final_callback(task_process_context)

    def _cleanup(self, task_process_context):
        temp_folder = task_process_context.task.get_temporary_output_folder()
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)

    def _get_progress(self, task_process_context):
        total = len(task_process_context.task.frames) * len(self.processes)
        value = 0
        if self.prioritize_final_output:
            value = task_process_context.frame_index * \
                len(self.processes) + task_process_context.sub_process_index
        else:
            value = task_process_context.sub_process_index * \
                len(task_process_context.task.frames) + \
                task_process_context.frame_index
        return value / total

    def _proceed_task_process_context(self, task_process_context):
        while True:
            if self.prioritize_final_output:
                task_process_context.sub_process_index += 1

                if task_process_context.sub_process_index >= len(self.processes):
                    task_process_context.sub_process_index = 0
                    task_process_context.frame_index += 1

                    if task_process_context.frame_index >= len(task_process_context.task.frames):
                        return

            else:
                task_process_context.frame_index += 1

                if task_process_context.frame_index >= len(task_process_context.task.frames):
                    task_process_context.frame_index = 0
                    task_process_context.sub_process_index += 1

                    if task_process_context.sub_process_index >= len(self.processes):
                        return

            # Skip the sub process if it is not applicable to the current frame
            current_process = self.processes[task_process_context.sub_process_index]
            current_frame = task_process_context.task.frames[task_process_context.frame_index]

            if current_process.applicable(current_frame):
                break

    def _finalize(self, task_process_context):
        # Clean up
        if self.cleanup_afterwards:
            self._cleanup(task_process_context)
