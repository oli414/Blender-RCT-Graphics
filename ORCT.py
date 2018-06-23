bl_info = {
    "name": "OpenRCT2 Graphics Helper",
    "category": "Render",
}

import bpy
import math
import os

angleSections = {
    "VEHICLE_SPRITE_FLAG_FLAT" : [
            [ False, 32, 0, 0, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES" : [
            [ False, 4, 11.1026, 0, 0 ],
            [ False, 4, -11.1026, 0, 0 ],
            [ False, 32, 22.2052, 0, 0 ],
            [ False, 32, -22.2052, 0, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_STEEP_SLOPES" : [
            [ False, 8, 40.36, 0, 0 ],
            [ False, 8, -40.36, 0, 0 ],
            [ False, 32, 58.5148, 0, 0 ],
            [ False, 32, -58.5148, 0, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES" : [
            [ False, 4, 75, 0, 0 ],
            [ False, 4, -75, 0, 0 ],
            [ False, 32, 90, 0, 0 ],
            [ False, 32, -90, 0, 0 ],
            [ False, 4, 105, 0, 0 ],
            [ False, 4, -105, 0, 0 ],
            [ False, 4, 120, 0, 0 ],
            [ False, 4, -120, 0, 0 ],
            [ False, 4, 135, 0, 0 ],
            [ False, 4, -135, 0, 0 ],
            [ False, 4, 150, 0, 0 ],
            [ False, 4, -150, 0, 0 ],
            [ False, 4, 165, 0, 0 ],
            [ False, 4, -165, 0, 0 ],
            [ False, 4, 180, 0, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES" : [
            [ True, 4, 8.0503, 0, 0 ],
            [ True, 4, -8.0503, 0, 0 ],
            [ True, 4, 16.1005, 0, 0 ],
            [ True, 4, -16.1005, 0, 0 ],
            [ True, 4, 49.1035, 0, 0 ],
            [ True, 4, -49.1035, 0, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_FLAT_BANKED" : [
            [ False, 8, 0, -22.5, 0 ],
            [ False, 8, 0, 22.5, 0 ],
            [ False, 32, 0, -45, 0 ],
            [ False, 32, 0, 45, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_INLINE_TWISTS" : [
            [ False, 4, 0, -15, 0 ],
            [ False, 4, 0, 15, 0 ],
            [ False, 4, 0, -30, 0 ],
            [ False, 4, 0, 30, 0 ],
            [ False, 4, 0, -45, 0 ],
            [ False, 4, 0, 45, 0 ],
            [ False, 4, 0, -60, 0 ],
            [ False, 4, 0, 60, 0 ],
            [ False, 4, 0, -75, 0 ],
            [ False, 4, 0, 75, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS" : [
        [ False, 32, 11.1026, -22.5, 0 ],
        [ False, 32, 11.1026, 22.5, 0 ],
        [ False, 32, -11.1026, -22.5, 0 ],
        [ False, 32, -11.1026, 22.5, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS" : [
        [ True, 4, 8.0503, -22.5, 0 ],
        [ True, 4, 8.0503, 22.5, 0 ],
        [ True, 4, -8.0503, -22.5, 0 ],
        [ True, 4, -8.0503, 22.5, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS" : [
        [ False, 4, 22.2052, -22.5, 0 ],
        [ False, 4, 22.2052, 22.5, 0 ],
        [ False, 4, -22.2052, -22.5, 0 ],
        [ False, 4, -22.2052, 22.5, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS" : [
        [ False, 32, 22.2052, -45, 0 ],
        [ False, 32, 22.2052, 45, 0 ],
        [ False, 32, -22.2052, -45, 0 ],
        [ False, 32, -22.2052, 45, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS" : [
        [ False, 4, 11.1026, -45, 0 ],
        [ False, 4, 11.1026, 45, 0 ],
        [ False, 4, -11.1026, -45, 0 ],
        [ False, 4, -11.1026, 45, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_CORKSCREWS" : [
        [ False, 4, 16.4, -15.8, 2.3 ],
        [ False, 4, 43.3, -34.4, 14 ],
        [ False, 4, 90, -45, 45 ],
        [ False, 4, 136.7, -34.4, 76 ],
        [ False, 4, 163.6, -15.8, 87.7 ],
        [ False, 4, -16.4, 15.8, 2.3 ],
        [ False, 4, -43.3, 34.4, 14 ],
        [ False, 4, -90, 45, 45 ],
        [ False, 4, -136.7, 34.4, 76 ],
        [ False, 4, -163.6, 15.8, 87.7 ],
        [ False, 4, 16.4, 15.8, -2.3 ],
        [ False, 4, 43.3, 34.4, -14 ],
        [ False, 4, 90, 45, -45 ],
        [ False, 4, 136.7, 34.4, -76 ],
        [ False, 4, 163.6, 15.8, -87.7 ],
        [ False, 4, -16.4, -15.8, -2.3 ],
        [ False, 4, -43.3, -34.4, -14 ],
        [ False, 4, -90, -45, -45 ],
        [ False, 4, -136.7, -34.4, -76 ],
        [ False, 4, -163.6, -15.8, -87.7 ]
    ],
    "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION" : [
        [ False, 4, 0, 0, 0 ],
        [ False, 4, 0, 0, 0 ],
        [ False, 4, 0, 0, 0 ]
    ],
    "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL" : [
        [ False, 32, 98.287, 0, 0 ]
    ]
}

toRenderSections = [
    "VEHICLE_SPRITE_FLAG_FLAT",
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES",
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES",
    "VEHICLE_SPRITE_FLAG_CORKSCREWS"
]

class RenderTask(object):
    sections = None
    sectionIndex = 0
    status = "CREATED"
    sectionInfo = None
    outIndex = 0
    def __init__(self, sections, outIndexStart):
        self.sections = sections
        self.outIndex = outIndexStart

    def step(self):

        if self.sectionInfo is None:
            section = self.sections[self.sectionIndex]
            self.sectionInfo = AngleSectionInfo(section, self.outIndex)

        result = self.sectionInfo.step()
        self.outIndex = self.sectionInfo.outIndex

        if result == "FINISHED":
            self.sectionInfo = None
            self.sectionIndex += 1

            if self.sectionIndex == len(self.sections):
                self.status = "FINISHED"
                return "FINISHED"

class AngleSectionInfo(object):
    section = None
    frame = None
    frameIndex = 0
    subIndex = 0
    outIndex = None
    status = "CREATED"
    def __init__(self, sectionIn, outIndexStart):
        self.section = sectionIn
        self.outIndex = outIndexStart

    def step(self):
        if self.frameIndex == len(self.section):
            self.status = "FINISHED"
        self.frame = self.section[self.frameIndex]

        frame = self.frame
        angle = 0
        if frame[0]:
            angle = 45
        angle += 360 / frame[1] * self.subIndex
        rotateRig(angle, frame[2], frame[3], frame[4])
        render(self.outIndex)
        postRender(self.outIndex)

        self.outIndex += 1
        self.subIndex += 1
        if self.subIndex == self.frame[1]:
            self.subIndex = 0
            self.frameIndex += 1
        if self.frameIndex == len(self.section):
            self.status = "FINISHED"
            return "FINISHED"
        self.status = "RUNNING"
        return "RUNNING"

def render(index):
    bpy.data.scenes['Scene'].render.filepath = bpy.path.abspath("//output/"+str(index)+".png")
    bpy.ops.render.render( write_still=True ) 
    

def rotateRig(angle, verAngle=0, bankedAngle=0, midAngle=0):
        object = bpy.data.objects['Rig']
        if object is None:
            return False
        object.rotation_euler = (math.radians(bankedAngle),math.radians(verAngle),math.radians(midAngle))
        vJoint = object.children[0] 
        vJoint.rotation_euler = (0,0,math.radians(angle))
        return True
    
def postRender(index):
    os.chdir("C:\\Users\\oli41\\Desktop\\OpenRCT2GFX\\Converter")
    os.system("FloydSteinbergCustomFast.bat " + bpy.path.abspath("//output/"+str(index)+".png"))
    

class RotateRenderRig(bpy.types.Operator):
    """Rotates the render rig"""
    bl_idname = "object.rotate_render_rig"
    bl_label = "Rotate Render Rig"
    
    _timer = None
    index = 0
    rendering = False
    stop = False
    renderTask = None
    
    @classmethod
    def poll(cls, context):
        return bpy.data.objects['Rig'] is not None
    
    def pre(self, dummy):
        self.rendering = True
        
    def post(self, dummy):
        self.index += 1
        self.rendering = False
        
    def cancelled(self, dummy):
        self.stop = True
    
    def execute(self, context):
        scene = context.scene
        properties = scene.orct2gh_properties
        
        angleSectionsToRender = []
        if properties.sprite_flag_flat:
            angleSectionsToRender.append(angleSections["VEHICLE_SPRITE_FLAG_FLAT"])
        if properties.sprite_flag_gentle_slopes:
            angleSectionsToRender.append(angleSections["VEHICLE_SPRITE_FLAG_GENTLE_SLOPES"])
        if properties.sprite_flag_steep_slopes:
            angleSectionsToRender.append(angleSections["VEHICLE_SPRITE_FLAG_STEEP_SLOPES"])
        if properties.sprite_flag_vertical_slopes:
            angleSectionsToRender.append(angleSections["VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES"])
        if properties.sprite_flag_vertical_diagonal_slopes:
            angleSectionsToRender.append(angleSections["VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES"])
        
        self.renderTask = RenderTask(angleSectionsToRender, 0)
        
        rotateRig(0, 0, 0, 0)
        
        bpy.data.cameras["Camera"].ortho_scale = 169.72 / (100 / bpy.data.scenes['Scene'].render.resolution_percentage)
        
        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        context.window_manager.modal_handler_add(self)
        
        return {"RUNNING_MODAL"}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            
            if self.stop or self.renderTask.status == "FINISHED":
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)
                
                rotateRig(0, 0, 0, 0)
                bpy.data.cameras["Camera"].ortho_scale = 169.72
                self.report({'INFO'}, 'Render finished.')
                
                return {"FINISHED"}
            
            elif not self.rendering:
                # render next frame
                self.renderTask.step()
                
        return {"PASS_THROUGH"}
    
class MyProperties(bpy.types.PropertyGroup):
    angles_num = bpy.props.IntProperty(
        name = "Horizontal Angles",
        description="Number of horizontal angles that have to be rendered",
        default = 4,
        min = 1,
        max = 100
        )
        
    sprite_flag_flat = bpy.props.BoolProperty(
        name = "Flat",
        description="Render sprites for flat track",
        default = True,
        )
    sprite_flag_gentle_slopes = bpy.props.BoolProperty(
        name = "Gentle Slopes",
        description="Render sprites for gentle sloped track",
        default = True,
        )
    sprite_flag_steep_slopes = bpy.props.BoolProperty(
        name = "Steep Slopes",
        description="Render sprites for steep sloped track",
        default = False,
        )
    sprite_flag_vertical_slopes = bpy.props.BoolProperty(
        name = "Vertical Slopes And Invert",
        description="Render sprites for vertically sloped track and inverts",
        default = False,
        )
    sprite_flag_vertical_diagonal_slopes = bpy.props.BoolProperty(
        name = "Diagonal Slopes",
        description="Render sprites for diagonal slopes",
        default = True,
        )


class OpenRCT2GraphicsHelperPanel(bpy.types.Panel):
    bl_label = "OpenRCT2 Graphics Helper"
    bl_idname = "RENDER_PT_orct_graphics_helper"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.orct2gh_properties
        
        row = layout.row()
        row.label("Ride Vehicle Track Properties:")
        
        row = layout.row()
        row.prop(properties, "sprite_flag_flat")
        row = layout.row()
        row.prop(properties, "sprite_flag_gentle_slopes")
        row = layout.row()
        row.prop(properties, "sprite_flag_steep_slopes")
        row = layout.row()
        row.prop(properties, "sprite_flag_vertical_slopes")
        row = layout.row()
        row.prop(properties, "sprite_flag_vertical_diagonal_slopes")
        
        row = layout.row()
        row.operator("object.rotate_render_rig", text = "Render")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.orct2gh_properties = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.orct2gh_properties


if __name__ == "__main__":
    register()
