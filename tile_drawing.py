
from typing import Any, Callable, Optional
from pygame.surface import Surface # type: ignore
from base_camera import Camera 
from base_labels import Label
from base_tile_map_form import TileMapForm 
from base_tile_maps import TileMap
from base_tile_pack import TilePackForm
from vectormath.vector import Vector2 # type: ignore



def draw_tile_layer(surface: Surface, 
                    camera: Camera,
                    map_form: TileMapForm,
                    tile_pack_form: TilePackForm,
                    label: Label):
    """Draws a TileMap layer on given Surface,
     \nfrom given MapForm and TilePackForm,
     \nindexed by given label"""
    draw_tiles(surface,
               tuple(next(t) if (t) else None
                     for t in tile_pack_form[label].tiles),
               map_form[label],
               -camera.x, -camera.y,
               Vector2(camera.w, camera.h),
               map_form.tile_width,
               map_form.tile_height)


def draw_tiles(surface: Surface, 
               tiles: tuple,
               tile_map: TileMap,
               x: float, 
               y: float,
               window_size: Vector2,
               tile_width: float,
               tile_height: float, 
               draw_funct: Optional[Callable[[Any, 
                                              float, 
                                              float, 
                                              float,
                                              float], 
                                              None]] = None):
    """Draws a tile map on given Surface, from given
     \ndraw function (optional),
     \ntile pack tuple, TileMap, coordinates, and tile size
     \nDO NOT call next() on any animation inside here"""
    tops = (i * tile_height + y for i in range(tile_map.height()))
    
    for t, top in enumerate(tops):
        
        lefts = (i * tile_width + x for i in range(tile_map.width()))
        
        if (0 < top < window_size.y or 
            0 < top + tile_height < window_size.y):
        
            for l, left in enumerate(lefts):
                
                if (0 < left < window_size.x or 
                    0 < left + tile_width < window_size.x):
                    
                    if (draw_funct is not None):
                        draw_funct(tiles[tile_map[t][l]], 
                                   left, top, 
                                   tile_width, tile_height)
                    else:
                        tile = tiles[tile_map[t][l]]
                        
                        if (tile is not None):
                            surface.blit(tile, (left, top))
                    
