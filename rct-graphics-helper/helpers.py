import math

def rotate_vec(x, y, view_angle):
    while view_angle < 0:
        view_angle += 4
    while view_angle > 3:
        view_angle -= 4
    if view_angle == 1:
        x, y = (-y,  x)
    if view_angle == 2:
        x, y = (-x, -y)
    if view_angle == 3:
        x, y = (y, -x)
    return (x, y)

def tile_index_to_tile_coord(tile_index, width):
    tile_y = math.floor(tile_index / width)
    tile_x = tile_index - (tile_y * width)
    return (tile_x, tile_y)

def tile_coord_to_tile_index(tile_x, tile_y, width):
    return tile_y * width + tile_x

def tile_coord_to_sprite_offset(tile_x, tile_y, width, length, view_angle):
    tile_x, tile_y = (tile_x - (width - 1) / 2, tile_y - (length - 1) / 2)
                    
    tile_x, tile_y = rotate_vec(tile_x, tile_y, view_angle)

    return (
        -int((tile_x * 32) - (tile_y * 32)),
        -int((tile_y * 16) + (tile_x * 16))
    )

def tile_index_to_sprite_offset(tile_index, width, length, view_angle):
    tile_x, tile_y = tile_index_to_tile_coord(tile_index, width)
    return tile_coord_to_sprite_offset(tile_x, tile_y, width, length, view_angle)
