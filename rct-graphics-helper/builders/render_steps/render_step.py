'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

class RenderProps:
    def __init__(self):
        self.aa = False
        self.aa_with_background = False

    def from_general_props(self, general_props):
        self.aa_with_background = general_props.anti_alias_with_background

    def apply_to_renderer(self, renderer):
        renderer.set_aa(self.aa)
        renderer.set_aa_with_background(self.aa_with_background)

class RenderStep:
    def __init__(self):
        self.x = 0

    def create_output(self, output = ""):
        return {
            "value": output
        }

    def execute(self, context, callback):
        return True,None

