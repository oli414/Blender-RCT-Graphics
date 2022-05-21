'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''


import bpy
from collections import OrderedDict

from .sub_processes.sub_processor import SubProcessor

from ..renderer import Renderer

# Context container for a process


class BaseProcessorContext:
    def __init__(self, final_callback):
        self.sub_process_index = 0
        self.final_callback = final_callback

# Processesor for performing a set of subtasks


class BaseProcessor(SubProcessor):
    def __init__(self, context):
        super().__init__()
        self.context = context

        self.processes = []

    def create_context(finalize_callback):
        return BaseProcessorContext(finalize_callback)

    def process(self, callback):
        def finalize():
            if callback != None:
                callback()

        process_context = self.create_context(finalize)
        self._step(process_context)

    def _step(self, process_context):
        while process_context.sub_process_index < len(self.processes):
            current_process = self.processes[process_context.sub_process_index]

            if not current_process.applicable(process_context):
                self._proceed_process_context(process_context)
                continue

            is_async = current_process.is_async
            sub_process_callback = None

            # Set a callback to restart the task processor if the sub process is async
            if is_async:
                def continue_process():
                    self._step(process_context)
                sub_process_callback = continue_process

            print("Starting subprocess: {}".format(
                type(current_process).__name__))
            current_process.process(process_context, sub_process_callback)
            print("Finished subprocess: {}".format(
                type(current_process).__name__))

            self._proceed_process_context(process_context)

            # Exit this function if the sub process is async, the callback restarts it when the subprocess is ready
            if is_async:
                return

        if process_context.final_callback != None:
            process_context.final_callback()

    def _proceed_process_context(self, process_context):
        process_context.sub_process_index += 1
