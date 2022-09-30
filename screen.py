

from vectormath.vector import Vector2 # type: ignore
from base_camera import Camera
from base_tile_map_form import TileMapForm


def position_from_screen(camera: Camera, 
                         vector: Vector2):
    """takes a TileMapForm and screen coordinate vector to translate,
    returns map coordinate vector"""
    return vector + Vector2(camera.x, camera.y)


def position_to_screen(camera: Camera, 
                       vector: Vector2):
    """takes a TileMapForm and map coordinate vector to translate,
    returns screen coordinate vector"""
    return vector - Vector2(camera.x, camera.y)

    

def on_screen(camera: Camera,
              *,
              pose: Vector2 = None,
              size: Vector2 = None,
              x: float = 0, y: float = 0, 
              w: float = 0, h: float = 0
              ) -> bool:
    
    if (pose is not None and size is not None):
        return ( ((pose.x   >= camera.x) and 
                  (pose.x   <= camera.x + camera.w) or 
                  (camera.x >= pose.x)   and
                  (camera.x <= pose.x + size.x))    and
                 ((pose.y   >= camera.y) and 
                  (pose.y   <= camera.y + camera.h) or 
                  (camera.y >= pose.y)   and
                  (camera.y <= pose.y + size.y)) )
    else:
        return ( ((x        >= camera.x) and 
                  (x        <= camera.x + camera.w) or 
                  (camera.x >= x)        and
                  (camera.x <= x + w))              and
                 ((y        >= camera.y) and 
                  (y        <= camera.y + camera.h) or 
                  (camera.y >= y)        and
                  (camera.y <= y + h)) )
