**RCT Graphics Helper is an add-on for Blender 2.79 that aids the creation of sprites that match the graphical style of Rollercoaster Tycoon.**

<p align="center">
  <img src="https://user-images.githubusercontent.com/2348094/163599017-243ab3a5-5567-4cd2-91d5-565b0cc86e63.png">
</p>

# Prerequisites

The following programs are necessary:

- [ImageMagick](https://imagemagick.org/script/download.php) (7.0.8-6 or higher) added to the Path variable as "Magick". For Windows install the "ImageMagick Q16 x64 static.exe" option.
- [Blender (2.79)](https://download.blender.org/release/Blender2.79/)

# Installing

1. Download the [latest release](https://github.com/oli414/Blender-RCT-Graphics/releases) of the RCT Graphics Helper Blender add-on.
2. In Blender, click on File > User Preferences > Add-ons > "Install Add-on from File..."
3. In the file explorer window, select the downloaded RCT Graphics Helper zip file.
4. Enable the add-on by clicking the checkbox to the left of "RendeR: RCT Graphics Helper"
5. Expand the RCT Graphics Helper add-on settings, and set the "OpenRCT2 Object Folder" path to the location of the /openrct2/object folder.
6. Click "Save User Settings".

# Usage

1. Open an existing file, or create a new file and make sure it's saved in its own folder.
2. Remove any global light sources.
3. In the render properties tab on the right, click "Initialize / Repair" in the "RCT Graphics Helper" section.
4. This will create the lighting rig, and set the correct render settings.
5. More options are now available in the RCT Graphics Helper section. Click the "Render" button to start rendering the scene.
6. In the folder where the Blend file is saved, an "output" folder has been created with the rendered image files.

Please check the [guidelines](https://github.com/oli414/Blender-RCT-Graphics/wiki/Guidelines) for the best results.

# Documentation

[Check out our wiki](https://github.com/oli414/Blender-RCT-Graphics/wiki/Documentation) for more in-depth details on all the available options.
