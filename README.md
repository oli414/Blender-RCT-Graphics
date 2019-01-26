
# Prerequisites

The following programs are necessary:

- ImageMagick (7.0.8-6 or higher)
- Blender (recent version)

# Installing

1. Copy the rct_graphics_helper folder (RCT Graphics Helper Addon/rct_graphics_helper) into the Blender addon folder.
2. Open the sample scene (lighting_rig.blend).
3. Enable RCT Graphics Helper in Blender's addon menu. 

The Render tab should now contain 3 new panels.

# Usage

1. Use the sample scene from the lighting_rig.blend file.
2. Import or create your model centered on the world's origin.
3. Go into to render tab.

Please check the [guidelines](https://github.com/oli414/Blender-RCT-Graphics/wiki/Guidelines) for the best results.

## Static Objects and Rides

4. Set the number of viewing angles in the "RCT Static" panel, for a standard scenery object this would be 4.
5. Click Render Static Object and wait until a message appears stating that the render is finished.

## Tracked Ride Vehicles

4. Select for which track pieces you want to render sprites in the "RCT Vehicles" panel.
5. Check the Restraint Animation checkbox if your vehicle has a restraint animation (Not yet implemented).
6. Check the Inverted Set checkbox for rides which can go upside-down for an extended amount of time, like the flying and lay-down coaster.
7. Set the number of rider sets (Sets of peeps, peeps usually enter rides in sets of 2). The different sets of peeps should have their layers set to a unique one after the first. So for the first set of peeps set their layers to only have the seconds one enabled.
8. Click Render Vehicle and wait until a message appears stating that the render is finished.

## Output

The images will be outputted to (by default) the output folder which is relative to the blender file. Offset files will be created along with the images.
The output can then be used in a tool like [Krutonium's ObjectBuilderGUI](https://github.com/Krutonium/ObjectBuilderGUI).

# Note

The textures distributed with the sample models are licensed under public domain and were taken from: https://opengameart.org/
