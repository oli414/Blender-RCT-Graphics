'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math

# Builder for populating the scene with objects


class SceneBuilder:

    def __init__(self):
        self.prefix = ""
        self.suffix = ""
        return

    def build(self, context):
        scene = context.scene

        self.remove_scene_object(context, "Lamp")

        # Root rig object
        rig_obj = self.create_scene_object(context, "Rig", None)
        rig_obj.location = (0, 0, 0)
        rig_obj.rotation_euler = (0, 0, math.radians(-45))
        rig_obj.hide = True
        rig_obj.hide_select = True

        rig_obj.rotation_mode = "YXZ"

        scene.objects.link(rig_obj)

        # Vertical joint object
        vertical_joint_obj = self.create_scene_object(
            context, "VerticalJoint", None)
        vertical_joint_obj.location = (0, 0, 0)
        vertical_joint_obj.hide = True
        vertical_joint_obj.hide_select = True

        scene.objects.link(vertical_joint_obj)
        vertical_joint_obj.parent = rig_obj

        # Camera object
        camera_obj = self.create_camera(context)

        scene.objects.link(camera_obj)
        camera_obj.parent = vertical_joint_obj

        scene.camera = camera_obj

        # Main light
        main_light_obj = self.create_main_light(context)

        scene.objects.link(main_light_obj)
        main_light_obj.parent = vertical_joint_obj

        # Filler light
        filler_light_obj = self.create_filler_light(context)

        scene.objects.link(filler_light_obj)
        filler_light_obj.parent = vertical_joint_obj

        # Dome light
        dome_light_obj = self.create_light_dome(context)

        scene.objects.link(dome_light_obj)
        dome_light_obj.parent = vertical_joint_obj

        # Environment lighting
        bpy.data.worlds["World"].light_settings.use_environment_light = True
        bpy.data.worlds["World"].light_settings.environment_energy = 0.15
        bpy.data.worlds["World"].light_settings.gather_method = "RAYTRACE"
        bpy.data.worlds["World"].light_settings.distance = 0
        bpy.data.worlds["World"].light_settings.samples = 1

    def create_camera(self, context):
        name = self.prefix + "Camera" + self.suffix
        if name in bpy.data.cameras:
            bpy.data.cameras.remove(bpy.data.cameras[name])

        camera_data = bpy.data.cameras.new(name=name)

        camera_data.type = "ORTHO"
        camera_data.ortho_scale = 45.2587

        camera_data.clip_start = 220
        camera_data.clip_end = 340

        camera_data.sensor_fit = "HORIZONTAL"
        camera_data.sensor_width = 1

        camera_data.shift_y = 0.25

        camera_object = self.create_scene_object(
            context, "Camera", camera_data)

        camera_object.hide_select = True
        camera_object.location = (0, -241.947, 139.739)
        camera_object.rotation_euler = (math.radians(60), 0, 0)

        return camera_object

    def create_main_light(self, context):
        lamp_data = self.create_lamp_data(context, "MainLight", "SUN")

        lamp_data.energy = 1.3
        lamp_data.use_specular = True
        lamp_data.use_diffuse = True
        lamp_data.shadow_method = "RAY_SHADOW"
        lamp_data.shadow_ray_sample_method = "ADAPTIVE_QMC"
        lamp_data.shadow_ray_samples = 4
        lamp_data.shadow_soft_size = 0.5
        lamp_data.shadow_adaptive_threshold = 0.001

        lamp_object = self.create_scene_object(context, 'Mainlight', lamp_data)

        lamp_object.hide = True
        lamp_object.hide_select = True
        lamp_object.location = (0, 0, 0)
        lamp_object.rotation_euler = (math.radians(67.5), 0, math.radians(90))

        return lamp_object

    def create_filler_light(self, context):
        lamp_data = self.create_lamp_data(context, "FillerLight", "SUN")

        lamp_data.energy = 0.5
        lamp_data.use_specular = True
        lamp_data.use_diffuse = True
        lamp_data.shadow_method = "RAY_SHADOW"
        lamp_data.shadow_ray_sample_method = "ADAPTIVE_QMC"
        lamp_data.shadow_ray_samples = 4
        lamp_data.shadow_soft_size = 0.5
        lamp_data.shadow_adaptive_threshold = 0.001

        lamp_object = self.create_scene_object(
            context, 'FillerLight', lamp_data)

        lamp_object.hide = True
        lamp_object.hide_select = True
        lamp_object.location = (0, 0, 0)
        lamp_object.rotation_euler = (
            0, math.radians(-72.5), math.radians(115))

        return lamp_object

    def create_light_dome(self, context):
        lamp_data = self.create_lamp_data(context, "LightDome", "HEMI")
        lamp_data.energy = 0.1
        lamp_data.use_specular = False

        lamp_object = self.create_scene_object(context, 'LightDome', lamp_data)
        lamp_object.hide = True
        lamp_object.hide_select = True

        return lamp_object

    def create_scene_object(self, context, name, data=None):
        name = self.prefix + name + self.suffix
        if name in context.scene.objects:
            bpy.data.objects.remove(
                context.scene.objects[name], do_unlink=True)
        return bpy.data.objects.new(name, data)

    def remove_scene_object(self, context, name):
        if name in context.scene.objects:
            bpy.data.objects.remove(
                context.scene.objects[name], do_unlink=True)


    def create_lamp_data(self, context, name, type):
        name = self.prefix + name + self.suffix
        if name in bpy.data.lamps:
            bpy.data.lamps.remove(bpy.data.lamps[name])

        lamp_data = bpy.data.lamps.new(name=name, type=type)
        return lamp_data
