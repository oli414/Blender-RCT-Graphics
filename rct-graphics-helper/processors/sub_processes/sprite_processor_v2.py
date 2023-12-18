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

from ...renderer import Renderer

# Context container for the render task process
class SpriteProcessContext:
    def __init__(self, master_context, final_callback, renderer, output, temp):
        self.master_context = master_context
        self.task = master_context.task
        self.step_index = 0
        self.final_callback = final_callback
        
        self.renderer = renderer
        self.output_path = output
        self.temp_path = temp

class SpriteProcessorV2(SubProcessor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self, master_context, callback):
        def finalize(task_process_context):
            self._finalize(task_process_context)

            if callback != None:
                callback()

        if not os.path.exists(master_context.task.get_output_folder()):
            os.mkdir(master_context.task.get_output_folder())

        output_path = os.path.join(master_context.task.get_output_folder(), "sprites")
        if not os.path.exists(output_path):
            os.mkdir(output_path)

            
        temp_path = os.path.join(master_context.task.get_output_folder(), ".temp")
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        task_process_context = SpriteProcessContext(master_context, finalize, self.renderer, output_path, temp_path)

        self._step(task_process_context)

    def _step(self, task_process_context):
        while task_process_context.step_index < len(task_process_context.task.steps):
            current_step = task_process_context.task.steps[task_process_context.step_index]

            def step_finished():
                print("Finished step: {}".format(
                    type(current_step).__name__))
                self._proceed_task_process_context(task_process_context)
                print("Progress: {}%".format(
                    round(self._get_progress(task_process_context) * 100)))
            
            def async_step_finished():
                step_finished()
                self._step(task_process_context)

            print("Starting step: {}".format(
                type(current_step).__name__))
            is_finished = current_step.execute(task_process_context, async_step_finished)

            # Exit this function if the sub process is async, the callback restarts it when the subprocess is ready
            if not is_finished:
                return
            
            step_finished()
            
        if task_process_context.final_callback != None:
            task_process_context.final_callback(task_process_context)

    def _cleanup(self, task_process_context):
        x = 0
        #if os.path.exists(task_process_context.temp_path):
        #    shutil.rmtree(task_process_context.temp_path)

    def _get_progress(self, task_process_context):
        total = len(task_process_context.task.steps)
        value = task_process_context.step_index
        return value / total

    def _proceed_task_process_context(self, task_process_context):
        task_process_context.step_index += 1
        print("Next step is {}".format(task_process_context.step_index))

    def _finalize(self, task_process_context):
        # Clean up
        self._cleanup(task_process_context)
