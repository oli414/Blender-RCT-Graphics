
# Prerequisites

The following programs are necessary:

- [ImageMagick](https://imagemagick.org/script/download.php) (7.0.8-6 or higher) added to the Path variable as "Magick". For Windows install the "ImageMagick Q16 x64 static.exe" option.
- [Blender (2.79)](https://download.blender.org/release/Blender2.79/)

# Installing

1. Download the [latest release](https://github.com/oli414/Blender-RCT-Graphics/releases) of the RCT Graphics Helper Blender add-on.
2. In Blender, click on File > User Preferences > Add-ons > "Install Add-on from File..."
3. In the file explorer window, select the downloaded RCT Graphics Helper zip file.
4. The plugin should now show up in the list of add-ons as "RCT Graphics Helper"
5. Expand the RCT Graphics Helper add-on settings, and set the "OpenRCT2 Object Folder" path to the location of the /openrct2/object folder.

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