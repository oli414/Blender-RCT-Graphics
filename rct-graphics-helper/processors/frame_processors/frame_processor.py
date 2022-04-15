'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

# Base processor for processing render frames


class FrameProcessor:
    def __init__(self):
        self.is_async = False

    def applicable(self, frame):
        return True

    def process(self, frame, callback=None):
        print("Invalid processor. Processor does not implement a process method.")
