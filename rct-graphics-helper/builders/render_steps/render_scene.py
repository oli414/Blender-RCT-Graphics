'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import os
from .render_step import RenderStep

class RenderScene(RenderStep):
    def __init__(self, output, render_props, output_meta=False):
        self.output = self.create_output(output)
        self.render_props = render_props
        self.output_meta = output_meta
        if self.output_meta:
            self.meta_output = self.create_output("")

    def execute(self, context, callback):
        self.render_props.apply_to_renderer(context.renderer)

        output_name = self.output["value"]
        output_path = os.path.join(context.temp_path, output_name)
        self.output["value"] = output_path + ".png"
        context.renderer.set_output_path(output_path)
        
        print("Writing scene render to {}".format(self.output["value"]))

        meta_output_name = output_name + "_meta"
        if self.output_meta:
            self.meta_output["value"] = os.path.join(context.temp_path, meta_output_name + "0000.exr")
            print("Writing meta render to {}".format(self.meta_output["value"]))
        context.renderer.set_meta_output_path(context.temp_path, meta_output_name)

        context.renderer.render(True, callback)

        return False

