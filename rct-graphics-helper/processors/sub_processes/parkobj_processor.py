'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import json
import os
from collections import OrderedDict
import shutil
import zipfile

from .sub_processor import SubProcessor

# Processor for creating a .parkobj file


class ParkobjProcessor(SubProcessor):
    def __init__(self, renderer):
        super().__init__()

        self.renderer = renderer

    def applicable(self, master_context):
        general_props = self.renderer.context.scene.rct_graphics_helper_general_properties
        return general_props.build_parkobj

    def process(self, master_context, callback=None):
        general_props = self.renderer.context.scene.rct_graphics_helper_general_properties
        task = master_context.task

        images = self._read_sprite_manifest(task)

        updated_object_file = self._inject_object_descriptor(
            task, images, general_props.build_gx)

        if updated_object_file == None:
            raise Exception(
                "Failed to inject image manifest into the object.json.")

        self._generate_parkobj(task, updated_object_file,
                               general_props.copy_parkobj_to_orct2, general_props.build_gx)

    def _read_sprite_manifest(self, task):
        sprite_manifest_file_path = os.path.join(
            task.get_output_folder(), "sprites.json")

        if not os.path.exists(sprite_manifest_file_path):
            raise Exception(
                "Failed to read the sprites.json sprite manifest for the .parkobj generation.")

        images = []

        with open(sprite_manifest_file_path, "r") as images_file:
            images = json.loads(images_file.read(),
                                object_pairs_hook=OrderedDict)
            images_file.close()

        return images

    def _inject_object_descriptor(self, task, images, has_gx):
        file_path = os.path.join(
            task.get_output_folder(), "object.json")

        if not os.path.exists(file_path):
            raise Exception(
                "Failed to read object.json. An object.json file is required in the output directory for the creation of a .parkobj file.")

        with open(file_path, mode="r+", encoding="utf-8") as object_file:
            data = json.loads(object_file.read(),
                              object_pairs_hook=OrderedDict)

            if has_gx:
                data["images"] = "$LGX:images.dat"
            else:
                data["images"] = images

            object_file.seek(0)
            object_file.truncate()

            object_file.write(json.dumps(data, indent=4, ensure_ascii=False))
            object_file.close()

            if data.get("id") == None:
                raise Exception(
                    "object.json file does not have an id field. The id field is required to determine the .parkobj file name.")

            print("Updated the images table in the object.json")

            return {
                "images": images,
                "object_id": data["id"]
            }

    def _generate_parkobj(self, task, info, copy_to_objects, has_gx):
        file_path = task.get_output_folder()
        parkobj_file_name = info.get("object_id") + ".parkobj"
        parkobj_file = os.path.join(file_path, parkobj_file_name)

        with zipfile.ZipFile(parkobj_file, 'w', zipfile.ZIP_DEFLATED) as parkobj:
            parkobj.write(os.path.join(
                file_path, "object.json"), "object.json")

            if has_gx:
                images_file = os.path.join(file_path, "images.dat")

                if not os.path.exists(images_file):
                    raise Exception(
                        images_file + " does not exist, but is expected to be there.")

                parkobj.write(os.path.join(
                    file_path, "images.dat"), "images.dat")
            else:
                for image in info.get("images"):

                    if isinstance(image, str):
                        continue

                    image_file = os.path.join(file_path, image.get("path"))

                    if not os.path.exists(image_file):
                        raise Exception(
                            image_file + " does not exist, but is expected to be there.")

                    parkobj.write(os.path.join(
                        file_path, image.get("path")), image.get("path"))

            parkobj.close()

            print("Finished generating the .parkobj file")

        if not copy_to_objects:
            return

        addon_prefs = task.context.user_preferences.addons["rct-graphics-helper"].preferences

        target_dir = os.path.abspath(bpy.path.abspath(
            os.path.join(addon_prefs.orct2_directory, "object")))

        if not os.path.exists(target_dir):
            raise Exception(
                "The OpenRCT2/objects directory set in the add-on preferences is not a valid directory. " + target_dir)

        shutil.copyfile(parkobj_file, os.path.join(
            target_dir, parkobj_file_name))

        print("Copied generated .parkobj file to " + target_dir)
