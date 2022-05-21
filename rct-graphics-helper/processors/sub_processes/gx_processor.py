'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import shutil
import bpy
import os
import subprocess

from .sub_processor import SubProcessor

# Processor for creating the GX image .dat file


class GXProcessor(SubProcessor):
    def __init__(self, renderer):
        super().__init__()

        self.renderer = renderer

    def applicable(self, master_context):
        general_props = self.renderer.context.scene.rct_graphics_helper_general_properties
        return general_props.build_gx

    def process(self, master_context, callback=None):
        general_props = self.renderer.context.scene.rct_graphics_helper_general_properties
        task = master_context.task
        manifest_file_path = os.path.join(
            task.get_output_folder(), "sprites.json")
        gx_file_path = os.path.join(
            task.get_output_folder(), "images.dat")

        result = str(subprocess.check_output(
            "gxc build \"" + gx_file_path + "\" \"" + manifest_file_path + "\"", shell=True))

        if not os.path.exists(gx_file_path):
            raise Exception(
                "GXC command did not return a GX file. Did you add the GXC (sprite compiler) to the path variable?")

        if not general_props.build_assetpack:
            return

        addon_prefs = task.context.user_preferences.addons["rct-graphics-helper"].preferences

        if addon_prefs.opengraphics_directory == "":
            raise Exception(
                "OpenGraphics repository path is not set in the add-on preferences.")

        opengraphics_repo_path = os.path.abspath(
            addon_prefs.opengraphics_directory)

        result = str(subprocess.check_output(
            "node build.mjs", shell=True, cwd=opengraphics_repo_path))

        parkap_file_name = "openrct2.graphics.opengraphics.parkap"
        parkap_file = os.path.abspath(os.path.join(
            opengraphics_repo_path, "out", parkap_file_name))

        if not os.path.exists(parkap_file):
            raise Exception(
                ".parkap file could not be found. Node.js is required for this process.")

        if not general_props.copy_assetpack_to_orct2:
            return

        target_dir = os.path.abspath(bpy.path.abspath(os.path.join(
            addon_prefs.orct2_directory, "assetpack")))

        shutil.copyfile(parkap_file, os.path.join(
            target_dir, parkap_file_name))

        print("Copied generated .parkap file to " + target_dir)
