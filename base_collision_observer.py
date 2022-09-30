
import math

from vectormath.vector import Vector2 # type: ignore
from base_labels import (SideLabel,
                         TOP_SIDE, 
                         BOTTOM_SIDE, 
                         LEFT_SIDE, 
                         RIGHT_SIDE,
                         NONE_SIDE)

from base_tile_maps import CollisionMap
from base_traits_entities import Entity
from tile_collisions import COLLISIONS, NO_RES, TileInfo, checking_order




def step_range(start, step, length):
    return (i * step + start for i in range(length))




# class that holds 
# tile_length and collision offset and
# takes an Entity and a CollisionMap and
# checks for collisions
class CollisionObserver:

    tile_length: float
    offset: float = 0.5
    
    
    def __init__(self, 
                 tile_length: float, 
                 offset: float = 0.5):
        self.tile_length = tile_length
        self.offset = offset
    
    
    # checks a rectangular Entity obj_form against 
    # the surrounding tiles in the CollisionMap
    #
    # returns: 
    #       new_form = dict with Vector2 
    #           { 'prev', 'delta', 'pose', and 'size' }
    #       collisions = list of TileInfo 
    #           for each collision
    def check_collision(self, 
                        obj_form: Entity, 
                        collision_map: CollisionMap, 
                        tile_length: float) -> tuple[dict[str, Vector2],
                                                     list[TileInfo]]:
        
        new_form: dict[str, Vector2] = { 
            "prev":  obj_form.prev.copy(),
            "pose":  obj_form.pose.copy(),
            "size":  obj_form.size.copy(),
            "delta": obj_form.delta.copy()
        }
        
        collisions: list[TileInfo] = []
        
        self.tile_length = tile_length

        self.handle_side(collision_map, new_form, collisions, TOP_SIDE)
        self.handle_side(collision_map, new_form, collisions, LEFT_SIDE)
        self.handle_side(collision_map, new_form, collisions, RIGHT_SIDE)
        self.handle_side(collision_map, new_form, collisions, BOTTOM_SIDE)

        return (new_form, collisions)
    
    # NOT USING ANYMORE
    # def handleSide(self, 
    #                collision_map: CollisionMap, 
    #                obj_form: dict[str, Vector2],
    #                collisions: list[TileInfo],
    #                obj_side: SideLabel):
        
    #     getLane = lambda tile_length, val: math.floor(val / tile_length)
    #     valid_tile = lambda t : ((t > 0) and 
    #                              (COLLISIONS[t] is not None))
        
    #     x: float = 0 
    #     y: float = 0
    #     sides: list[SideLabel] = [] # sides of environment tile to check against
    #     constant_row = False # True if we're looking at 
    #                          # top or bottom side of object,
    #                          # or False for left/right sides
        
    #     if   (obj_side == TOP_SIDE):
    #         x = obj_form["pose"].x
    #         y = obj_form["pose"].y
    #         sides = [BOTTOM_SIDE, RIGHT_SIDE]
    #         constant_row = True
            
    #     elif (obj_side == BOTTOM_SIDE):
    #         x = obj_form["pose"].x
    #         y = obj_form["pose"].y + obj_form["size"].y
    #         sides = [TOP_SIDE, RIGHT_SIDE]
    #         constant_row = True
            
    #     elif (obj_side == LEFT_SIDE):
    #         x = obj_form["pose"].x
    #         y = obj_form["pose"].y
    #         sides = [RIGHT_SIDE, BOTTOM_SIDE]
    #         constant_row = False
            
    #     elif (obj_side == RIGHT_SIDE):
    #         x = obj_form["pose"].x + obj_form["size"].x
    #         y = obj_form["pose"].y
    #         sides = [LEFT_SIDE, BOTTOM_SIDE]
    #         constant_row = False
        
        
    #     next_tile_side = LEFT_SIDE if (constant_row) else TOP_SIDE
        
    #     # x or y of the corner of the object we're looking at
    #     pos = x if (constant_row) else y
        
    #     # width or height of the object
    #     obj_size = (obj_form["size"].x if (constant_row) else 
    #                 obj_form["size"].y)
        
        
    #     # row or column of the side of the object we're looking at
    #     lane = getLane(self.tile_length, 
    #                    y if (constant_row) else x)
        
    #     # points on the side of the object we're looking at
    #     points_on_obj = tuple(step_range(getLane(self.tile_length, pos), # first corner
    #                                      1, 
    #                                      math.ceil(obj_size / self.tile_length)))
        
    #     points_on_obj += (getLane(self.tile_length, pos + obj_size),) # last corner
        
        
        
        
    #     del sides[-1] # testing
        
        
        
        
    #     # the opposite: column or row of the 
    #     # point on the object we're looking at
    #     for index, cross_lane in enumerate(points_on_obj):
            
    #         # if (index == len(points_on_obj)): # last point
    #         #     sides.append(next_tile_side)
            
    #         row    = lane if (constant_row) else cross_lane
    #         column = cross_lane if (constant_row) else lane
            
    #         tile: int = collision_map.get_tile(row, column)
            
    #         if valid_tile(tile): # call collision function, 
    #                              # if tile routes to one
                                 
                
    #             tile_info = TileInfo(reference=tile, 
    #                                  row=row, 
    #                                  column=column, 
    #                                  tile_side=NONE_SIDE)
                
    #             # if collided, add tile_info to collisions list
    #             if ( tile_side := COLLISIONS[tile]( obj_form,
    #                                                 tile_info,
    #                                                 row, column,
    #                                                 sides,
    #                                                 self.tile_length, 
    #                                                 self.offset) ):
    #                 tile_info.tile_side = tile_side
                
    #             collisions.append(tile_info)
            
    #         # if (index == 0): # first point
    #         #     del sides[-1]
    
    # USING NOW
    def handle_side(self, 
                    collision_map: CollisionMap, 
                    obj_form: dict[str, Vector2],
                    collisions: list[TileInfo],
                    obj_side: SideLabel):
        
        # returns row or column
        getLane = lambda tile_length, val: math.floor(val / tile_length)
        
        # checks if tile routes to collision function
        valid_collision = lambda c : ((c > 0) and 
                                      (COLLISIONS[c] is not NO_RES))
        
        x: float = 0 
        y: float = 0
        ALL_POINTS_SIDE = NONE_SIDE
        POINT_1_SIDE    = NONE_SIDE
        POINT_2_SIDE    = NONE_SIDE
        constant_row = False # True if we're looking at 
                             # top or bottom side of object,
                             # or False for left/right sides
        
        if   (obj_side == TOP_SIDE):
            x = obj_form["pose"].x
            y = obj_form["pose"].y
            ALL_POINTS_SIDE = BOTTOM_SIDE 
            POINT_1_SIDE    = RIGHT_SIDE
            POINT_2_SIDE    = LEFT_SIDE
            constant_row = True
            
        elif (obj_side == BOTTOM_SIDE):
            x = obj_form["pose"].x
            y = obj_form["pose"].y + obj_form["size"].y
            ALL_POINTS_SIDE = TOP_SIDE
            POINT_1_SIDE    = RIGHT_SIDE
            POINT_2_SIDE    = LEFT_SIDE
            constant_row = True
            
        elif (obj_side == LEFT_SIDE):
            x = obj_form["pose"].x
            y = obj_form["pose"].y
            ALL_POINTS_SIDE = RIGHT_SIDE 
            POINT_1_SIDE    = BOTTOM_SIDE
            POINT_2_SIDE    = TOP_SIDE
            constant_row = False
            
        elif (obj_side == RIGHT_SIDE):
            x = obj_form["pose"].x + obj_form["size"].x
            y = obj_form["pose"].y
            ALL_POINTS_SIDE = LEFT_SIDE
            POINT_1_SIDE    = BOTTOM_SIDE
            POINT_2_SIDE    = TOP_SIDE
            constant_row = False
        
        
        # x or y of the corner of the object we're looking at
        pos = x if (constant_row) else y
        
        # width or height of the object
        obj_size = (obj_form["size"].x if (constant_row) else 
                    obj_form["size"].y)
        
        
        # row or column of the side of the object we're looking at
        lane = getLane(self.tile_length, 
                       y if (constant_row) else x)
        
        # points on the side of the object we're looking at
        points_on_obj = tuple(step_range(getLane(self.tile_length, pos), # first corner
                                         1, 
                                         math.ceil(obj_size / self.tile_length)))
        
        points_on_obj += (getLane(self.tile_length, pos + obj_size),) # last corner
        
        
        # CHECKING:  ALL_POINTS_SIDE
        
        # has (tile_info, collision_index)
        all_collisions: list[ TileInfo ] = []
        
        # the opposite: column or row of the 
        # point on the object we're looking at
        for cross_lane in points_on_obj:
            
            row    = lane if (constant_row) else cross_lane
            column = cross_lane if (constant_row) else lane
            
            collision_index: int = collision_map.get_tile(row, column)
            
            if valid_collision(collision_index): # if tile routes to 
                                                 # collision function

                # save tile_info to all_collisions list
                all_collisions.append( 
                    TileInfo(reference=collision_index, 
                             row=row, 
                             column=column, 
                             tile_side=ALL_POINTS_SIDE )
                )
                
        
        ordered_collisions = checking_order(all_collisions, ALL_POINTS_SIDE)
        
        # print("[")
        # for same_offset_tile_infos in ordered_collisions:
        #     print("  [ ", *same_offset_tile_infos, sep="\n   ") 
        #     print("  ]")
        # print("]")
        # print()
        
        for same_offset_tile_infos in ordered_collisions:
            
            collided_with_offset = False
            
            for tile_info in same_offset_tile_infos:
                
                # if collided with tile, 
                # add tile_info for every 
                # collision with same offset 
                # to collisions list,
                # then stop checking ALL_POINTS_SIDE
                if ((COLLISIONS[tile_info.reference]( 
                                    obj_form,
                                    row, column,
                                    [tile_info.tile_side],
                                    self.tile_length, 
                                    self.offset
                     )
                    ) != NONE_SIDE):
                    
                    collided_with_offset = True
                    collisions.extend(same_offset_tile_infos)
                    break
            
            # if collision found,
            # stop checking ALL_POINTS_SIDE
            if (collided_with_offset): 
                break
                
        # for tile_info in all_collisions:
                
        #     # if collided with tile, 
        #     # add tile_info to collisions
        #     if ((COLLISIONS[tile_info.reference]( 
        #                         obj_form,
        #                         row, column,
        #                         [tile_info.tile_side],
        #                         self.tile_length, 
        #                         self.offset
        #          )
        #         ) != NONE_SIDE):
                  
        #         collisions.append(tile_info)
        
        
        
        # # CHECKING:  POINT_1_SIDE
        
        # cross_lane = points_on_obj[0]
        # row    = lane if (constant_row) else cross_lane
        # column = cross_lane if (constant_row) else lane
        # collision_index = collision_map.get_tile(row, column)
        # tile_info = TileInfo(reference=collision_index, 
        #                      row=row, 
        #                      column=column, 
        #                      tile_side=POINT_1_SIDE )
        
        # if valid_collision(collision_index):
            
        #     # if collided with tile, 
        #     # add tile_info to collisions
        #     if ((COLLISIONS[tile_info.reference]( 
        #                         obj_form,
        #                         row, column,
        #                         [tile_info.tile_side],
        #                         self.tile_length, 
        #                         self.offset
        #          )
        #         ) != NONE_SIDE):
                
        #         collisions.append(tile_info)
        
        
        # # CHECKING:  POINT_2_SIDE
        
        # cross_lane = points_on_obj[-1]
        # row    = lane if (constant_row) else cross_lane
        # column = cross_lane if (constant_row) else lane
        # collision_index = collision_map.get_tile(row, column)
        # tile_info = TileInfo(reference=collision_index, 
        #                      row=row, 
        #                      column=column, 
        #                      tile_side=POINT_2_SIDE )
        
        # if valid_collision(collision_index):
            
        #     # if collided with tile, 
        #     # add tile_info to collisions
        #     if ((tile_side := COLLISIONS[tile_info.reference]( 
        #                         obj_form,
        #                         row, column,
        #                         [tile_info.tile_side],
        #                         self.tile_length, 
        #                         self.offset
        #                         )
        #         ) != NONE_SIDE):
                
        #         collisions.append(tile_info)
        
        
        
        
        

  
# (done)
# we REALLY want the collisions list to have 
# every non-None tile that the entity is touching


# saves all valid collision functions for each obj_side
# then checks them in order of 
# least offset to most offset (on that tile_side)

# finds if at least one tile on that 
# tile_side was collided with,
# and then all other tiles on that 
# tile_side (with the same offset) should be counted

# NO LONGER checks multiple tile_sides on corners

# (not anymore)
# DOING multiple checks of each tile_side for each corner of obj_form




# could send offsets directly to collision functions
# and then check if each offset is -1 and other stuff 
# (using indexing with side_indices)

# hitTop(), hitBottom(), ... could all be in a dictionary and 
# accessed by their DirLabels



