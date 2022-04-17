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

from .frame_processors.post_processor import PostProcessor
from .frame_processors.merge_masks_processor import MergeMasksProcessor
from .frame_processors.render_processor import RenderProcessor
from .frame_processors.tile_indices_render_processor import TileIndicesRenderProcessor
from ..renderer import Renderer

# Context container for the render task process


class RenderTaskProcessContext:
    def __init__(self, task, final_callback):
        self.task = task
        self.frame_index = 0
        self.sub_process_index = 0
        self.final_callback = final_callback

# Processes a render task


class RenderTaskProcessor:
    def __init__(self, context, palette_manager):
        self.context = context
        self.renderer = Renderer(context, palette_manager)

        self.processes = [
            RenderProcessor(self.renderer),
            TileIndicesRenderProcessor(self.renderer, False),
            TileIndicesRenderProcessor(self.renderer, True),
            MergeMasksProcessor(self.renderer),
            PostProcessor(self.renderer)
        ]

        self.prioritize_final_output = True
        self.cleanup_afterwards = True

    def process(self, task, callback):
        def finalize():
            self._finalize(task)

            if callback != None:
                callback()

        task_process_context = RenderTaskProcessContext(task, finalize)
        self._step(task_process_context)

    def _step(self, task_process_context):
        general_props = self.context.scene.rct_graphics_helper_general_properties

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

        # Clean up
        if self.cleanup_afterwards:
            self._cleanup(task_process_context)

        if task_process_context.final_callback != None:
            task_process_context.final_callback()

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

    def _finalize(self, task):
        general_props = self.context.scene.rct_graphics_helper_general_properties

        images = self._append_images_manifest(task)

        if not general_props.write_to_object_descriptor:
            return

        updated_object_file = self._inject_object_descriptor(task, images)

        if not general_props.build_parkobj or updated_object_file == None:
            return

        self._generate_parkobj(task, updated_object_file,
                               general_props.copy_parkobj_to_orct2)

    def _append_images_manifest(self, task):
        file_path = os.path.join(
            task.get_output_folder(), "images.json")

        output_info_list = task.output_info

        def get_index(output_info):
            return output_info.index

        output_info_list.sort(key=get_index)

        images = []
        if os.path.exists(file_path):
            with open(file_path, "r") as images_file:
                images = json.loads(images_file.read(),
                                    object_pairs_hook=OrderedDict)
                images_file.close()

        with open(file_path, "w") as images_file:
            def_entry = None
            if len(images) > 0:
                def_entry = images[len(images) - 1]

            for output_info in output_info_list:
                while len(images) <= output_info.index:
                    images.append(def_entry)

                image_dict = OrderedDict()
                image_dict["path"] = os.path.basename(output_info.path)
                image_dict["x"] = output_info.offset_x
                image_dict["y"] = output_info.offset_y
                image_dict["format"] = "keep"

                images[output_info.index] = image_dict

            images_file.write(json.dumps(images, indent=4))
            images_file.close()

        return images

    def _inject_object_descriptor(self, task, images):
        file_path = os.path.join(
            task.get_output_folder(), "object.json")

        if not os.path.exists(file_path):
            return None

        with open(file_path, mode="r+", encoding="utf-8") as object_file:
            data = json.loads(object_file.read(),
                              object_pairs_hook=OrderedDict)

            data["images"] = images

            object_file.seek(0)
            object_file.truncate()

            object_file.write(json.dumps(data, indent=4, ensure_ascii=False))
            object_file.close()

            if data.get("id") == None:
                print("object.json does not contain an object id field")
                return None

            print("Updated the images table in the object.json")

            return {
                "images": images,
                "object_id": data["id"]
            }

    def _generate_parkobj(self, task, info, copy_to_objects):
        general_props = self.context.scene.rct_graphics_helper_general_properties

        file_path = task.get_output_folder()
        parkobj_file_name = info.get("object_id") + ".parkobj"
        parkobj_file = os.path.join(file_path, parkobj_file_name)

        with zipfile.ZipFile(parkobj_file, 'w', zipfile.ZIP_DEFLATED) as parkobj:
            parkobj.write(os.path.join(
                file_path, "object.json"), "object.json")

            for image in info.get("images"):

                if isinstance(image, str):
                    continue

                image_file = os.path.join(file_path, image.get("path"))

                if not os.path.exists(image_file):
                    print(
                        image_file + " does not exist. Creation of the .parkobj has been aborted")
                    return

                parkobj.write(os.path.join(
                    file_path, image.get("path")), image.get("path"))

            parkobj.close()

            print("Finished generating the .parkobj file")

        if not copy_to_objects:
            return

        addon_prefs = task.context.user_preferences.addons["rct-graphics-helper"].preferences

        target_dir = os.path.abspath(bpy.path.abspath(
            addon_prefs.orct2_object_directory))
        if not os.path.exists(target_dir):
            print(target_dir + " is not an existing directory.")
            return

        shutil.copyfile(parkobj_file, os.path.join(
            target_dir, parkobj_file_name))

        print("Copied generated .parkobj file to " + target_dir)
