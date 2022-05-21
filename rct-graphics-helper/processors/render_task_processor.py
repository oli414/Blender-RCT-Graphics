'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''


import bpy
from .sub_processes.parkobj_processor import ParkobjProcessor
from .sub_processes.gx_processor import GXProcessor
from .sub_processes.sprites_manifest_processor import SpritesManifestProcessor
from .base_processor import BaseProcessor, BaseProcessorContext

from .sub_processes.sprite_processor import SpriteProcessor
from ..renderer import Renderer

# Context container for the render task process


class RenderTaskProcessContext(BaseProcessorContext):
    def __init__(self, task, final_callback):
        super().__init__(final_callback)
        self.task = task

# Processes a render task


class RenderTaskProcessor(BaseProcessor):
    def __init__(self, context, palette_manager):
        super().__init__(context)
        self.renderer = Renderer(context, palette_manager)

        self.processes = [
            SpriteProcessor(self.renderer),
            SpritesManifestProcessor(self.renderer),
            GXProcessor(self.renderer),
            ParkobjProcessor(self.renderer)
        ]

    def create_context(self, finalize_callback, task):
        return RenderTaskProcessContext(task, finalize_callback)

    def process(self, task, callback):
        def finalize():
            if callback != None:
                callback()

        task_process_context = self.create_context(finalize, task)
        self._step(task_process_context)
