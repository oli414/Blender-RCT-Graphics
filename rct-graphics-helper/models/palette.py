'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import subprocess
import os

from ..magick_command import MagickCommand
from ..res.res import res_path

palette_colors = [
    "black",
    "gray",
    "lavender_purple",
    "violet_purple",
    "blue",
    "teal",
    "yellow_green",
    "sea_green",
    "light_olive_green",
    "dark_olive_green",
    "lime_green",
    "yellow",
    "bright_yellow",
    "orange",
    "salmon",
    "sandy_brown",
    "tan_brown",
    "bordeaux_red",
    "bright_red",
    "magenta",
    "animated_water",
    "animated_water_sparkle",
    "animated_chain",
    "recolor_1",
    "transparent",
]


palette_colors_details = {
    "black": {
        "title": "Black",
        "Description": "Black to white tones",
        "default": True
    },
    "gray": {
        "title": "Gray",
        "Description": "4 extra gray tones",
        "default": True
    },
    "lavender_purple": {
        "title": "Lavender Purple",
        "Description": "Lavender purple",
        "default": True
    },
    "violet_purple": {
        "title": "Violet Purple",
        "Description": "Violet purple",
        "default": True
    },
    "blue": {
        "title": "Blue",
        "Description": "Blue",
        "default": True
    },
    "teal": {
        "title": "Teal",
        "Description": "Teal",
        "default": True
    },
    "yellow_green": {
        "title": "Yellow Green",
        "Description": "Yellow green",
        "default": True
    },
    "sea_green": {
        "title": "Sea Green",
        "Description": "Sea green",
        "default": True
    },
    "light_olive_green": {
        "title": "Light Olive Green",
        "Description": "Light olive green",
        "default": True
    },
    "dark_olive_green": {
        "title": "Dark Olive Green",
        "Description": "Dark olive green",
        "default": True
    },
    "lime_green": {
        "title": "Lime Green",
        "Description": "Lime green",
        "default": True
    },
    "yellow": {
        "title": "Yellow",
        "Description": "Yellow",
        "default": True
    },
    "bright_yellow": {
        "title": "Bright Yellow",
        "Description": "3 extra bright yellow colors",
        "default": True
    },
    "orange": {
        "title": "Orange",
        "Description": "Orange",
        "default": True
    },
    "salmon": {
        "title": "Salmon",
        "Description": "Salmon color used as the skin tone for peeps",
        "default": True
    },
    "sandy_brown": {
        "title": "Sandy Brown",
        "Description": "Sandy brown",
        "default": True
    },
    "tan_brown": {
        "title": "Tan Brown",
        "Description": "Less satured brown color",
        "default": True
    },
    "bordeaux_red": {
        "title": "Bordeaux Red",
        "Description": "Bordeaux red",
        "default": True
    },
    "bright_red": {
        "title": "Bright Red",
        "Description": "Bright red",
        "default": True
    },
    "magenta": {
        "title": "Magenta",
        "Description": "Magenta",
        "default": True
    },
    "transparent": {
        "title": "Transparent",
        "Description": "Transparent",
        "default": True
    },
    "animated_water": {
        "title": "Animated Water",
        "Description": "Colors used for the palette animated water",
        "default": False
    },
    "animated_water_sparkle": {
        "title": "Animated water Sparkle",
        "Description": "Colors used for the palette animated water sparkles",
        "default": False
    },
    "animated_chain": {
        "title": "Animated Chain",
        "Description": "Colors used for the palette animated chain lift",
        "default": False
    },
    "recolor_1": {
        "title": "Recolor 1 Orange",
        "Description": "Orange used by OpenRCT2 to import recolor 1",
        "default": False
    }
}

palette_base_path = os.path.join(res_path, "palettes")
palette_groups_path = os.path.join(palette_base_path, "groups")

# Collection of color groups to create a palette from


class Palette:
    def __init__(self, path=None, colors=[]):
        self.colors = colors
        self.generated = False
        self.invalidated = False
        self.path = ""

        if path != None:
            self.path = path
            self.generated = True
            self.invalidated = True

    # Adds a list of colors to the palette
    def add_colors(self, colors):
        for color in colors:
            if not color in self.colors:
                self.invalidated = True
                self.colors.append(color)

    # Excludes a color from the palette
    def exclude_color(self, color):
        if color in self.colors:
            self.invalidated = True
            self.colors.remove(color)

    def clear(self):
        self.colors = []
        self.invalidated = True

    # Creates a copy of the palette
    def copy(self):
        copied_palette = Palette()
        copied_palette.colors = self.colors.copy()
        copied_palette.invalidated = self.invalidated
        copied_palette.generated = self.generated
        copied_palette.path = self.path
        return copied_palette

    # Prepares the palette for use by the render process. The palette image file is regenerated if necessary
    def prepare(self, renderer):
        if (not self.generated) or self.invalidated:
            self.generate_output(renderer, self.path)

    # Generates a palette image file
    def generate_output(self, renderer, output_path):
        cmd = MagickCommand("")

        color_paths = []
        for color in self.colors:
            color_paths.append(os.path.join(
                palette_groups_path, color + ".png"))

        cmd.as_montage(color_paths)

        print(cmd.get_command_string(
            renderer.magick_path, output_path))
        subprocess.check_output(cmd.get_command_string(
            renderer.magick_path, output_path), shell=True)

        self.path = output_path
        self.generated = True
        self.invalidated = False
