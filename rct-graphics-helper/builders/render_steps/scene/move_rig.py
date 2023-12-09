'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
from ..render_step import RenderStep

class MoveRig(RenderStep):
    def __init__(self, view_angle, x, y, z):
        self.view_angle = view_angle
        self.x = x
        self.y = y
        self.z = z
    
    def execute(self, context, callback):
        rig = bpy.data.objects["Rig"]
        if rig is None:
            return True
        rig.location = (self.x, self.y, self.z)
        rig.rotation_euler = (math.radians(0),
                             math.radians(0), math.radians(0))
        vJoint = rig.children[0]
        vJoint.rotation_euler = (0, 0, math.radians(self.view_angle - 45))
        return True

