'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

track_angle_sections_names = [
    "VEHICLE_SPRITE_FLAG_FLAT",
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES",
    "VEHICLE_SPRITE_FLAG_STEEP_SLOPES",
    "VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES",
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES",
    "VEHICLE_SPRITE_FLAG_FLAT_BANKED",
    "VEHICLE_SPRITE_FLAG_INLINE_TWISTS",
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS",
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_CORKSCREWS",
    "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION",
    "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL"
]

track_angle_sections = {
    "VEHICLE_SPRITE_FLAG_FLAT": [
        [False, 32, 0, 0, 0]
    ],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES": [
        [False, 4, 11.1026, 0, 0],
        [False, 4, -11.1026, 0, 0],
        [False, 32, 22.2052, 0, 0],
        [False, 32, -22.2052, 0, 0]
    ],
    "VEHICLE_SPRITE_FLAG_STEEP_SLOPES": [
        [False, 8, 40.36, 0, 0],
        [False, 8, -40.36, 0, 0],
        [False, 32, 58.5148, 0, 0],
        [False, 32, -58.5148, 0, 0]
    ],
    "VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES": [
        [False, 4, 75, 0, 0],
        [False, 4, -75, 0, 0],
        [False, 32, 90, 0, 0],
        [False, 32, -90, 0, 0],
        [False, 4, 105, 0, 0],
        [False, 4, -105, 0, 0],
        [False, 4, 120, 0, 0],
        [False, 4, -120, 0, 0],
        [False, 4, 135, 0, 0],
        [False, 4, -135, 0, 0],
        [False, 4, 150, 0, 0],
        [False, 4, -150, 0, 0],
        [False, 4, 165, 0, 0],
        [False, 4, -165, 0, 0],
        [False, 4, 180, 0, 0]
    ],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES": [
        [True, 4, 8.0503, 0, 0],
        [True, 4, -8.0503, 0, 0],
        [True, 4, 16.1005, 0, 0],
        [True, 4, -16.1005, 0, 0],
        [True, 4, 49.1035, 0, 0],
        [True, 4, -49.1035, 0, 0]
    ],
    "VEHICLE_SPRITE_FLAG_FLAT_BANKED": [
        [False, 8, 0, -22.5, 0],
        [False, 8, 0, 22.5, 0],
        [False, 32, 0, -45, 0],
        [False, 32, 0, 45, 0]
    ],
    "VEHICLE_SPRITE_FLAG_INLINE_TWISTS": [
        # The banking sprites are used at the start of a twist ((180-MAX_BANK)/6*FRAME)+MAX_BANK
        [False, 4, 0, -67.5, 0],
        [False, 4, 0, 67.5, 0],
        [False, 4, 0, -90, 0],
        [False, 4, 0, 90, 0],
        [False, 4, 0, -112.5, 0],
        [False, 4, 0, 112.5, 0],
        [False, 4, 0, -135, 0],
        [False, 4, 0, 135, 0],
        [False, 4, 0, -157.5, 0],
        [False, 4, 0, 157.5, 0]
    ],
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS": [
        [False, 32, 11.1026, -22.5, 0],
        [False, 32, 11.1026, 22.5, 0],
        [False, 32, -11.1026, -22.5, 0],
        [False, 32, -11.1026, 22.5, 0]
    ],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS": [
        [True, 4, 8.0503, -22.5, 0],
        [True, 4, 8.0503, 22.5, 0],
        [True, 4, -8.0503, -22.5, 0],
        [True, 4, -8.0503, 22.5, 0]
    ],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS": [
        [False, 4, 22.2052, -22.5, 0],
        [False, 4, 22.2052, 22.5, 0],
        [False, 4, -22.2052, -22.5, 0],
        [False, 4, -22.2052, 22.5, 0]
    ],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS": [
        [False, 32, 22.2052, -45, 0],
        [False, 32, 22.2052, 45, 0],
        [False, 32, -22.2052, -45, 0],
        [False, 32, -22.2052, 45, 0]
    ],
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS": [
        [False, 4, 11.1026, -45, 0],
        [False, 4, 11.1026, 45, 0],
        [False, 4, -11.1026, -45, 0],
        [False, 4, -11.1026, 45, 0]
    ],
    "VEHICLE_SPRITE_FLAG_CORKSCREWS": [
        [False, 4, 22.21,   20.7,   4.11],
        [False, 4, 50.77,   37.76,  18.43],
        [False, 4, 90,      45,     45],
        [False, 4, 129.23,  37.76,  71.57],
        [False, 4, 157.79,  20.7,   85.89],

        [False, 4, -22.21,  -20.7,   4.11],
        [False, 4, -50.77,  -37.76,  18.43],
        [False, 4, -90,     -45,     45],
        [False, 4, -129.23, -37.76,  71.57],
        [False, 4, -157.79, -20.7,   85.89],

        [False, 4, 22.21,   -20.7,   -4.11],
        [False, 4, 50.77,   -37.76,  -18.43],
        [False, 4, 90,      -45,     -45],
        [False, 4, 129.23,  -37.76,  -71.57],
        [False, 4, 157.79,  -20.7,   -85.89],

        [False, 4, -22.21,   20.7,   -4.11],
        [False, 4, -50.77,   37.76,  -18.43],
        [False, 4, -90,      45,     -45],
        [False, 4, -129.23,  37.76,  -71.57],
        [False, 4, -157.79,  20.7,   -85.89],
    ],
    "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION": [
        [False, 4, 0, 0, 0]
    ],
    "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL": [
        [False, 32, 9.8287, 0, 0]
    ]
}
