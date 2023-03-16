'''
Copyright (c) 2023 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

# This is the order sprite groups are rendered in
sprite_group_names = [
    "slopeFlat",         "slopes12",         "slopes25",           "slopes42",
    "slopes60",          "slopes75",         "slopes90",           "slopesLoop",
    "slopeInverted",     "slopes8",          "slopes16",           "slopes50",
    "flatBanked22",      "flatBanked45",     "flatBanked67",       "flatBanked90",
    "inlineTwists",      "slopes12Banked22", "slopes8Banked22",    "slopes25Banked22",
    "slopes8Banked45",   "slopes16Banked22", "slopes16Banked45",   "slopes25Banked45",
    "slopes12Banked45",  "slopes25Banked67", "slopes25Banked90",   "slopes25InlineTwists",
    "slopes42Banked22",  "slopes42Banked45", "slopes42Banked67",   "slopes42Banked90",
    "slopes60Banked22",  "corkscrews",       "restraintAnimation", "curvedLiftHillUp",
    "curvedLiftHillDown"
]

# The sprites to render in each sprite group. The given rotation values are unused
sprite_group_manifest = {
    'slopeFlat': [
        [False, 32, 0, 0, 0]
    ],
    'slopes12': [
        [False, 4, 11.1026, 0, 0],
        [False, 4, -11.1026, 0, 0]
    ],
    'slopes25': [
        [False, 32, 22.2052, 0, 0],
        [False, 32, -22.2052, 0, 0]
    ],
    'slopes42': [
        [False, 8, 40.36, 0, 0],
        [False, 8, -40.36, 0, 0]
    ],
    'slopes60': [
        [False, 32, 58.5148, 0, 0],
        [False, 32, -58.5148, 0, 0]
    ],
    'slopes75': [
        [False, 4, 75, 0, 0],
        [False, 4, -75, 0, 0]
    ],
    'slopes90': [
        [False, 32, 90, 0, 0],
        [False, 32, -90, 0, 0]
    ],
    'slopesLoop': [
        [False, 4, 105, 0, 0],
        [False, 4, -105, 0, 0],
        [False, 4, 120, 0, 0],
        [False, 4, -120, 0, 0],
        [False, 4, 135, 0, 0],
        [False, 4, -135, 0, 0],
        [False, 4, 150, 0, 0],
        [False, 4, -150, 0, 0],
        [False, 4, 165, 0, 0],
        [False, 4, -165, 0, 0]
    ],
    'slopeInverted': [
        [False, 4, 180, 0, 0]
    ],
    'slopes8': [
        [True, 4, 8.0503, 0, 0],
        [True, 4, -8.0503, 0, 0]
    ],
    'slopes16': [
        [True, 4, 16.1005, 0, 0],
        [True, 4, -16.1005, 0, 0]
    ],
    'slopes50': [
        [True, 4, 49.1035, 0, 0],
        [True, 4, -49.1035, 0, 0]
    ],
    'flatBanked22': [
        [False, 8, 0, -22.5, 0],
        [False, 8, 0, 22.5, 0]
    ],
    'flatBanked45': [
        [False, 32, 0, -45, 0],
        [False, 32, 0, 45, 0]
    ],
    'flatBanked67': [
        [False, 4, 0, -67.5, 0],
        [False, 4, 0, 67.5, 0]
    ],
    'flatBanked90': [
        [False, 4, 0, -90, 0],
        [False, 4, 0, 90, 0]
    ],
    'inlineTwists': [
        [False, 4, 0, -112.5, 0],
        [False, 4, 0, 112.5, 0],
        [False, 4, 0, -135, 0],
        [False, 4, 0, 135, 0],
        [False, 4, 0, -157.5, 0],
        [False, 4, 0, 157.5, 0]
    ],
    'slopes12Banked22': [
        [False, 32, 11.1026, -22.5, 0],
        [False, 32, 11.1026, 22.5, 0],
        [False, 32, -11.1026, -22.5, 0],
        [False, 32, -11.1026, 22.5, 0]
    ],
    'slopes8Banked22': [
        [True, 4, 8.0503, -22.5, 0],
        [True, 4, 8.0503, 22.5, 0],
        [True, 4, -8.0503, -22.5, 0],
        [True, 4, -8.0503, 22.5, 0]
    ],
    'slopes25Banked22': [
        [False, 4, 22.2052, -22.5, 0],
        [False, 4, 22.2052, 22.5, 0],
        [False, 4, -22.2052, -22.5, 0],
        [False, 4, -22.2052, 22.5, 0]
    ],
    'slopes8Banked45': [
        [True, 4, 8.0503, -45, 0],
        [True, 4, 8.0503, 45, 0],
        [True, 4, -8.0503, -45, 0],
        [True, 4, -8.0503, 45, 0]
    ],
    'slopes16Banked22': [
        [True, 4, 16.1005, -22.5, 0],
        [True, 4, 16.1005, 22.5, 0],
        [True, 4, -16.1005, -22.5, 0],
        [True, 4, -16.1005, 22.5, 0]
    ],
    'slopes16Banked45': [
        [True, 4, 16.1005, -45, 0],
        [True, 4, 16.1005, 45, 0],
        [True, 4, -16.1005, -45, 0],
        [True, 4, -16.1005, 45, 0]
    ],
    'slopes25Banked45': [
        [False, 32, 22.2052, -45, 0],
        [False, 32, 22.2052, 45, 0],
        [False, 32, -22.2052, -45, 0],
        [False, 32, -22.2052, 45, 0]
    ],
    'slopes12Banked45': [
        [False, 4, 11.1026, -45, 0],
        [False, 4, 11.1026, 45, 0],
        [False, 4, -11.1026, -45, 0],
        [False, 4, -11.1026, 45, 0]
    ],
    'slopes25Banked67': [
        [False, 4, 22.2052, -67.5, 0],
        [False, 4, 22.2052, 67.5, 0],
        [False, 4, -22.2052, -67.5, 0],
        [False, 4, -22.2052, 67.5, 0]
    ],
    'slopes25Banked90': [
        [False, 4, 22.2052, -90, 0],
        [False, 4, 22.2052, 90, 0],
        [False, 4, -22.2052, -90, 0],
        [False, 4, -22.2052, 90, 0]
    ],
    'slopes25InlineTwists': [
        [False, 4, 22.2052, -112.5, 0],
        [False, 4, 22.2052, 112.5, 0],
        [False, 4, 22.2052, -135, 0],
        [False, 4, 22.2052, 135, 0],
        [False, 4, 22.2052, -157.5, 0],
        [False, 4, 22.2052, 157.5, 0],
        [False, 4, -22.2052, -112.5, 0],
        [False, 4, -22.2052, 112.5, 0],
        [False, 4, -22.2052, -135, 0],
        [False, 4, -22.2052, 135, 0],
        [False, 4, -22.2052, -157.5, 0],
        [False, 4, -22.2052, 157.5, 0]
    ],
    'slopes42Banked22': [
        [False, 8, 40.36, -22.5, 0],
        [False, 8, 40.36, 22.5, 0],
        [False, 8, -40.36, -22.5, 0],
        [False, 8, -40.36, 22.5, 0]
    ],
    'slopes42Banked45': [
        [False, 8, 40.36, -45, 0],
        [False, 8, 40.36, 45, 0],
        [False, 8, -40.36, -45, 0],
        [False, 8, -40.36, 45, 0]
    ],
    'slopes42Banked67': [
        [False, 8, 40.36, -67.5, 0],
        [False, 8, 40.36, 67.5, 0],
        [False, 8, -40.36,-67.5, 0],
        [False, 8, -40.36, 67.5, 0]
    ],
    'slopes42Banked90': [
        [False, 8, 40.36, -90, 0],
        [False, 8, 40.36, 90, 0],
        [False, 8, -40.36, -90, 0],
        [False, 8, -40.36, 90, 0]
    ],
    'slopes60Banked22': [
        [False, 32, 58.5148, -22.5, 0],
        [False, 32, 58.5148, 22.5, 0],
        [False, 32, -58.5148, -22.5, 0],
        [False, 32, -58.5148, 22.5, 0]
    ],
    'corkscrews': [
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
    'restraintAnimation': [
        [False, 4, 0, 0, 0]
    ],
    'curvedLiftHillUp': [
        [False, 32, 9.8287, 0, 0]
    ],
    'curvedLiftHillDown': [
        [False, 32, 9.8287, 0, 0]
    ]
}

# Default sprite precision for full mode, the tooltip for the sprite group, and if the sprite group should be hidden from the list of sprite groups
sprite_group_metadata = {
    "slopeFlat": [32, "Flat track"],
    "slopes12": [4, "Orthogonal flat-to-gentle slope track"],
    "slopes25": [32, "Orthogonal gentle slope track"],
    "slopes42": [8, "Gentle-to-steep slope track"],
    "slopes60": [32, "Orthogonal steep slope track"],
    "slopes75": [4, "Steep-to-vertical slope track"],
    "slopes90": [4, "Vertical track"],
    "slopesLoop": [4,"Loop track"],
    "slopeInverted": [4, "Fully inverted track"],
    "slopes8": [4, "Diagonal flat-to-gentle slope track"],
    "slopes16": [4, "Diagonal gentle slope track"],
    "slopes50": [4, "Diagonal steep track"],
    "flatBanked22": [8, "Flat-to-bank transition track"],
    "flatBanked45": [32, "Flat banked track"],
    "flatBanked67": [4, "Flat steep banked track"],
    "flatBanked90": [4, "Flat vertically-banked track"],
    "inlineTwists": [4, "Flat inline twists"],
    "slopes12Banked22": [32, "Orthogonal flat-to-gentle-and-flat-to-banked transition track"],
    "slopes8Banked22": [4, "Diagonal flat-to-gentle-and-flat-to-banked transition track"],
    "slopes25Banked22": [4, "Orthogonal gentle slope flat-to-bank transition track"],
    "slopes25Banked45": [32, "Gentle sloped banked turns"],
    "slopes8Banked45": [4, "Diagonal flat-to-gentle slope banked transition track"],
    "slopes16Banked22": [4, "Diagonal gentle slope flat-to-banked transition track"],
    "slopes16Banked45": [4, "Diagonal gentle slope banked track"],
    "slopes12Banked45": [4, "Orthogonal flat-to-gentle-slope banked transition track"],
    "slopes25Banked67": [4, "Part of small zero-G rolls"],
    "slopes25Banked90": [4, "Part of small zero-G rolls"],
    "slopes25InlineTwists": [4, "Part of large zero-G roll"],
    "slopes42Banked22": [4, "Part of large zero-G roll"],
    "slopes42Banked45": [4, "Part of large zero-G roll"],
    "slopes42Banked67": [4, "Part of large zero-G roll"],
    "slopes42Banked90": [4, "Part of large zero-G roll"],
    "slopes60Banked22": [4, "Part of large zero-G roll"],
    "corkscrews": [4, "Corkscrew track"],
    "restraintAnimation": [4, "Animated restraints"],
    "curvedLiftHillUp": [32, "Sprial lifthill up track"],
    "curvedLiftHillDown": [32, "Spiral lifthill down track"]
}

# All legacy groups. See list in rct_graphics_helper_panel.py for which ones are displayed
legacy_group_names = [
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
    "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL",
    "VEHICLE_SPRITE_FLAG_ZERO_G_ROLLS",
    "VEHICLE_SPRITE_FLAG_INVERTED",
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPE_BANKED"
]

# Legacy sprite groups that are reset every time the user makes a selection
legacy_groups_implied = [
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS",
    "VEHICLE_SPRITE_FLAG_INVERTED"
]

# Display name of each sprite group, tooltip for each sprite group, default state of each sprite group
legacy_group_metadata = {
    "VEHICLE_SPRITE_FLAG_FLAT": ["Flat", "Render sprites for flat track", True],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES": ["Gentle Slopes", "Render sprites for gentle sloped track", True],
    "VEHICLE_SPRITE_FLAG_STEEP_SLOPES": ["Steep Slopes", "Render sprites for steep sloped track", False],
    "VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES": ["Vertical Loops", "Render sprites for vertical slopes and loops", False],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES": ["Diagonal Slopes", "Render sprites for diagonal slopes", True],
    "VEHICLE_SPRITE_FLAG_FLAT_BANKED": ["Flat Banked","Render sprites for flat banked track", False],
    "VEHICLE_SPRITE_FLAG_INLINE_TWISTS": ["Inline Twist", "Render sprites for the inline twist element", False],
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS": ["", "", False],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS": ["", "", False],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS": ["", "", False],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS": ["", "", False],
    "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS": ["Sloped Banked Turns","Render sprites for sloped banked turns", False],
    "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS": ["", "", False],
    "VEHICLE_SPRITE_FLAG_CORKSCREWS": ["Corkscrew", "Render sprites for corkscrews", False],
    "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION": ["Animated Restraints", "Render animated restraints", False],
    "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL": ["Spiral Lifthill", "Render sprites for spiral lifthills", False],
    "VEHICLE_SPRITE_FLAG_ZERO_G_ROLLS": ["Zero-G Rolls", "Render sprites for zero-G rolls", False],
    "VEHICLE_SPRITE_FLAG_INVERTED": ["", "", False],
    "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPE_BANKED": ["Diagonal Sloped Banked", "Render sprites for diagonal sloped banked track", False],
}

# What full sprite groups each legacy group maps to
legacy_group_map = {
    'VEHICLE_SPRITE_FLAG_FLAT': [ 'slopeFlat' ],
    'VEHICLE_SPRITE_FLAG_GENTLE_SLOPES': ['slopes12', 'slopes25'],
    'VEHICLE_SPRITE_FLAG_STEEP_SLOPES': ['slopes42', 'slopes60'],
    'VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES': ['slopes75', 'slopes90', 'slopesLoop'],
    'VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES': ['slopes8', 'slopes16','slopes50'],
    'VEHICLE_SPRITE_FLAG_FLAT_BANKED': ['flatBanked22','flatBanked45'],
    'VEHICLE_SPRITE_FLAG_INLINE_TWISTS': ['flatBanked67', 'flatBanked90', 'inlineTwists'],
    'VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS': ['slopes12Banked22'],
    'VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS': ['slopes8Banked22'],
    'VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS': ['slopes25Banked22'],
    'VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS': ['slopes25Banked45'],
    'VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS': ['slopes12Banked45'],
    'VEHICLE_SPRITE_FLAG_CORKSCREWS': ['corkscrews'],
    'VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION': ['restraintAnimation'],
    'VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL': ['curvedLiftHillUp', 'curvedLiftHillDown'],
    'VEHICLE_SPRITE_FLAG_ZERO_G_ROLLS': ["slopes60Banked22", "slopes42Banked22","slopes42Banked45","slopes42Banked67","slopes42Banked90", "slopes25InlineTwists", "slopes25Banked67","slopes25Banked90"],
    'VEHICLE_SPRITE_FLAG_INVERTED': ['slopeInverted'],
    'VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPE_BANKED': ['slopes8Banked45', 'slopes16Banked22', 'slopes16Banked45']
}

# What legacy groups are implied by combinations of other legacy sprite groups
legacy_group_dependencies = {
    frozenset({'VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS'}): frozenset({'VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS','VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS','VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS'}),
    frozenset({'VEHICLE_SPRITE_FLAG_FLAT_BANKED','VEHICLE_SPRITE_FLAG_GENTLE_SLOPES'}): frozenset({'VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS'}),
    frozenset({'VEHICLE_SPRITE_FLAG_FLAT_BANKED','VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES'}): frozenset({'VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS'}),
    frozenset({'VEHICLE_SPRITE_FLAG_INLINE_TWISTS'}): frozenset({'VEHICLE_SPRITE_FLAG_FLAT_BANKED', 'VEHICLE_SPRITE_FLAG_INVERTED'}),
    frozenset({'VEHICLE_SPRITE_FLAG_CORKSCREWS'}): frozenset({'VEHICLE_SPRITE_FLAG_INVERTED'}),
    frozenset({'VEHICLE_SPRITE_FLAG_ZERO_G_ROLLS'}): frozenset({'VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS', 'VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS', 'VEHICLE_SPRITE_FLAG_GENTLE_SLOPES', 'VEHICLE_SPRITE_FLAG_INVERTED'}),
    frozenset({'VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPE_BANKED'}): frozenset({'VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS'})
}


