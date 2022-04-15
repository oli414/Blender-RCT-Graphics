# Class for building magick commands
class MagickCommand(object):
    full_command = ""

    def __init__(self, input):
        self.full_command = self.__stringify_input(input)
        self.use_repage = False

    # Replaces the command with a montage command for generating spritesheets
    def as_montage(self, inputs):
        self.use_repage = False
        self.full_command = "montage \"" + \
            "\" \"".join(inputs) + \
            "\" -tile x1 -geometry +0+0 -background none"

    # Writes the current result to the MPR for reuse in the same command. The cached result can be referenced using mpr:{id}
    def write_to_cache(self, id, delete_previous=False, next_file=""):
        delete_addition = ""
        post = " "
        if delete_previous:
            delete_addition = "+delete "
            post = " " + self.__stringify_input(next_file)
        self.full_command = "( " + self.full_command + \
            " -write mpr:" + id + " " + delete_addition + ")" + post

    # Quantizes the image using a palette
    def quantize(self, palette, amount):
        self.full_command += " -dither FloydSteinberg -define dither:diffusion-amount=" + str(amount) + "% -remap " + \
            self.__stringify_input(palette) + " -depth 16"

    # Trims the image to the smallest possible size and outputs the offset difference
    def trim(self):
        self.use_repage = True
        self.full_command += \
            " -bordercolor none -compose Copy -border 1 -trim  -format \"%[fx:page.x - page.width/2] %[fx:page.y - page.height/2]\" -write info:"

    # Sets a number of channels (Red, Green, Blue) to 0
    def nullify_channels(self, channels_to_nullify):
        if not isinstance(channels_to_nullify, list):
            channels_to_nullify = [channels_to_nullify]
        self.full_command += " -channel " + \
            ",".join(channels_to_nullify) + " -evaluate set 0 +channel"

    # Masks out a specific color
    def id_mask(self, r, g, b):
        color = "rgb(" + ",".join([str(r), str(g), str(b)]) + ")"
        self.full_command += " -fill \"#00000000\" +opaque \"" + \
            color + "\" -fill \"#ffffffff\" -opaque \"" + color + "\""

    # Mixes between the current source, and source B given a mask
    def mask_mix(self, sourceB, mask):
        self.full_command = "( " + self.full_command + " ) " + \
            self.__stringify_input(sourceB) + " " + \
            self.__stringify_input(mask) + " -composite"

    # Mixes between the current source, alpha given a mask
    def mask_mix_self(self, mask):
        self.full_command = "( " + self.full_command + " ) " + \
            "-alpha on ( +clone -channel a -fx 0 ) +swap " + \
            self.__stringify_input(mask) + " -composite"

    # Combines the current source with sourceB
    def combine(self, sourceB):
        self.full_command = "( " + self.full_command + " ) " + \
            self.__stringify_input(sourceB) + " -composite"

    # Adds the current source and sourceB together using addition
    def additive(self, sourceB):
        self.full_command = "( " + self.full_command + " ) " + \
            self.__stringify_input(sourceB) + " -compose plus -composite"

    # Copies the alpha channel from the alpha_source and applies it to the current source
    def copy_alpha(self, alpha_source):
        mask = self.__stringify_input(
            alpha_source)
        self.full_command = "( " + self.full_command + \
            " ) ( " + \
            mask + " ) -compose CopyOpacity -composite"

    def set_bit_depth(self, depth):
        self.full_command += " -depth " + str(depth)

    # Gets the cli command to perform the ImageMagick operation

    def get_command_string(self, magick_path, output):
        if self.use_repage:
            self.full_command = self.full_command + " +repage"
        return magick_path + " " + self.full_command + " \"" + output + "\""

    def __stringify_input(self, input):
        if type(input) is str:
            if input.startswith("mpr:"):
                return input
            return "\"" + input + "\""
        self.use_repage = self.use_repage or input.use_repage
        return "( " + input.full_command + " )"
