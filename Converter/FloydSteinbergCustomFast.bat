IF %1.==. GOTO NoFile
set file=%1
set magick=E:\Git\ImageMagick-Windows\VisualMagick\bin\magick.exe

%magick% %file% -fuzz 0 -fill none -opaque rgb(57,59,57)  -quantize RGB -dither FloydSteinberg -remap C:\Users\oli41\Desktop\OpenRCT2GFX\Converter\palette.gif -colorspace sRGB -bordercolor none -border 1 ( +clone -trim -set option:NTRIM %%[fx:min(page.x,page.width-w-page.x)]x%%[fx:min(page.y,page.height-h-page.y)] +delete ) -shave %%[NTRIM] %file%

GOTO End
:NoFile
    ECHO No file specified
    pause
GOTO End
:End