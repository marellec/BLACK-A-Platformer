





from dataclasses import dataclass
from typing import Callable, Union

from vectormath.vector import Vector2 # type: ignore

from base_labels import (SideLabel, TOP_SIDE, 
                                    BOTTOM_SIDE, 
                                    RIGHT_SIDE, 
                                    LEFT_SIDE,
                                    NONE_SIDE)


# class that stores info about a tile and
# how it was collided into
@dataclass
class TileInfo:
    
    reference: int
    row: int
    column: int
    tile_side: SideLabel







def hitTop   (obj_form: dict[str, Vector2],
              row: int, 
              pushback: float, 
              offset: float,
              c_tile_len: float, 
              c_offset: float):
  top = row * c_tile_len + (offset if (offset) else 0)
 
  if (obj_form["pose"].y + obj_form["size"].y >  top and
      obj_form["prev"].y + obj_form["size"].y <= top):
    
    if (pushback):
        obj_form["delta"].y = 0
        obj_form["pose"].y  = top - obj_form["size"].y - c_offset
    
    
    # print(TOP_SIDE)
    return True
  
  return False

def hitBottom(obj_form: dict[str, Vector2],
              row: int, 
              pushback: float, 
              offset: float,
              c_tile_len: float, 
              c_offset: float):
    bottom = (row + 1) * c_tile_len - (offset if (offset) else 0)
 
    if (obj_form["pose"].y <  bottom and
        obj_form["prev"].y >= bottom):
        
        if (pushback):
            obj_form["delta"].y = 0
            obj_form["pose"].y  = bottom + c_offset * 1.5
        
        # print("BOTTOM_SIDE")
        return True
    
    return False

def hitLeft  (obj_form: dict[str, Vector2],
              column: int, 
              pushback: float, 
              offset: float,
              c_tile_len: float, 
              c_offset: float):
    left = column * c_tile_len + (offset if (offset) else 0)

    if (obj_form["pose"].x + obj_form["size"].x >  left and
        obj_form["prev"].x + obj_form["size"].x <= left):
        
        if (pushback):
            obj_form["delta"].x = 0
            obj_form["pose"].x  = left - obj_form["size"].x - c_offset
        
        # print(LEFT_SIDE)
        return True
    
    return False

def hitRight (obj_form: dict[str, Vector2],
              column: int, 
              pushback: float, 
              offset: float,
              c_tile_len: float, 
              c_offset: float):
    right = (column + 1) * c_tile_len - (offset if (offset) else 0)

    if (obj_form["pose"].x <  right and
        obj_form["prev"].x >= right):
        
        if (pushback):
            obj_form["delta"].x = 0
            obj_form["pose"].x  = right + c_offset
        
        # print("real right")
        return True
    
    return False


def flatSides(obj_form: dict[str, Vector2],
              row: int,
              column: int,  
              collideable_sides: list[SideLabel], 
              checking_sides: list[SideLabel],
              pushbacks: list[bool], 
              offsets: list[float], 
              c_tile_len: float, 
              c_offset: float
              ) -> SideLabel:
    
    for collideable_side in collideable_sides:
        
            for checking_side, push_b, off_s in zip(checking_sides, 
                                           pushbacks,
                                           offsets):

                if   (checking_side == collideable_side == TOP_SIDE):
                        if (hitTop   (obj_form, row, 
                                      push_b, off_s, 
                                      c_tile_len, c_offset)): 
                            return TOP_SIDE
                
                elif (checking_side == collideable_side == LEFT_SIDE):
                        if (hitLeft  (obj_form, column, 
                                      push_b, off_s, 
                                      c_tile_len, c_offset)): 
                            return LEFT_SIDE
                
                elif (checking_side == collideable_side == BOTTOM_SIDE): 
                        if (hitBottom(obj_form, row, 
                                      push_b, off_s, 
                                      c_tile_len, c_offset)): 
                            return BOTTOM_SIDE
                
                elif (checking_side == collideable_side == RIGHT_SIDE):
                        if (hitRight (obj_form, column, 
                                      push_b, off_s, 
                                      c_tile_len, c_offset)): 
                            return RIGHT_SIDE
    return NONE_SIDE
    
    

def flatVerticalExtPartialSides(obj_form: dict[str, Vector2],
                                row: int,
                                column: int,  
                                collideable_sides: list[SideLabel], 
                                checking_sides: list[SideLabel],
                                pushbacks: list[bool], 
                                body_on_top: bool,
                                offset: float, 
                                checking_side_offset: float,
                                c_tile_len: float, 
                                c_offset: float
                                ) -> SideLabel:
    
    for collideable_side, push_b in zip(collideable_sides, 
                                        pushbacks):
        for checking_side in checking_sides:
            
            if (collideable_side == checking_side == TOP_SIDE):
                if (hitTop    (obj_form, row,  
                               push_b, 
                               0 if (body_on_top) else offset, 
                               c_tile_len, c_offset)): 
                    return TOP_SIDE
            
            edge_of_tile = row * c_tile_len + offset
            
            horizontal = ( (obj_form["pose"].y  < edge_of_tile)
                          
                          if (body_on_top) else 
                          
                          ((obj_form["pose"].y + 
                            obj_form["size"].y) > edge_of_tile) )
            
            if (horizontal):
                
                if (collideable_side == checking_side == LEFT_SIDE):
                    if (hitLeft  (obj_form, column,  
                                  push_b, checking_side_offset, 
                                  c_tile_len, c_offset)): 
                        return LEFT_SIDE
                
                if (collideable_side == checking_side == RIGHT_SIDE):
                    if (hitRight (obj_form, column,  
                                  push_b, checking_side_offset, 
                                  c_tile_len, c_offset)): 
                        return RIGHT_SIDE
            
            if (collideable_side == checking_side == BOTTOM_SIDE):
                if (hitBottom (obj_form, row,  
                               push_b, 
                               offset if (body_on_top) else 0, 
                               c_tile_len, c_offset)): 
                    return BOTTOM_SIDE
    return NONE_SIDE
            



def  NO_RES(obj_form: dict[str, Vector2],
            row: int,
            column: int, 
            checking_sides: list[SideLabel], 
            c_tile_len: float, 
            c_offset: float
            ) -> SideLabel:
    pass



def flatAll(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE, BOTTOM_SIDE, RIGHT_SIDE], checking_sides, [True,True,True,True], [0,0,0,0], c_tile_len, c_offset)
def flatT(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE   ], checking_sides, [True], [0], c_tile_len, c_offset)
def flatB(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [BOTTOM_SIDE], checking_sides, [True], [0], c_tile_len, c_offset)
def flatL(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [LEFT_SIDE  ], checking_sides, [True], [0], c_tile_len, c_offset)
def flatR(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [RIGHT_SIDE ], checking_sides, [True], [0], c_tile_len, c_offset)
def flatTB(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, BOTTOM_SIDE], checking_sides, [True,True], [0,0], c_tile_len, c_offset)
def flatLR(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [LEFT_SIDE, RIGHT_SIDE], checking_sides, [True,True], [0,0], c_tile_len, c_offset)
def flatT_L(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE], checking_sides,     [True,True], [0,0], c_tile_len, c_offset)
def flatT_R(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, RIGHT_SIDE], checking_sides,    [True,True], [0,0], c_tile_len, c_offset)
def flatB_L(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [LEFT_SIDE, BOTTOM_SIDE], checking_sides,  [True,True], [0,0], c_tile_len, c_offset)
def flatB_R(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [BOTTOM_SIDE, RIGHT_SIDE], checking_sides, [True,True], [0,0], c_tile_len, c_offset)
def flatTB_L(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE, BOTTOM_SIDE], checking_sides,   [True,True,True], [0,0,0], c_tile_len, c_offset)
def flatTB_R(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, BOTTOM_SIDE, RIGHT_SIDE], checking_sides,  [True,True,True], [0,0,0], c_tile_len, c_offset)
def flatLR_T(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE, RIGHT_SIDE], checking_sides,    [True,True,True], [0,0,0], c_tile_len, c_offset)
def flatLR_B(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [LEFT_SIDE, BOTTOM_SIDE, RIGHT_SIDE], checking_sides, [True,True,True], [0,0,0], c_tile_len, c_offset)
def noResFlatAll(obj_form, row, column, checking_sides, c_tile_len, c_offset) -> SideLabel: return  flatSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE, BOTTOM_SIDE, RIGHT_SIDE], checking_sides, [False,False,False,False], [0,0,0,0], c_tile_len, c_offset)


def flatTB_TopHalf(obj_form, row, column, checking_sides, c_tile_len, c_offset): return flatVerticalExtPartialSides(obj_form, row, column, [TOP_SIDE, BOTTOM_SIDE], checking_sides, [True,True], True, c_tile_len/2, 0, c_tile_len, c_offset)
def flatTB_L_TopHalf(obj_form, row, column, checking_sides, c_tile_len, c_offset): return flatVerticalExtPartialSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE, BOTTOM_SIDE ], checking_sides, [True,True,True], True, c_tile_len/2, 0, c_tile_len, c_offset)
def flatTB_R_TopHalf(obj_form, row, column, checking_sides, c_tile_len, c_offset): return flatVerticalExtPartialSides(obj_form, row, column, [TOP_SIDE, BOTTOM_SIDE, RIGHT_SIDE], checking_sides, [True,True,True], True, c_tile_len/2, 0, c_tile_len, c_offset)

def noResFlatLR_T_BottomHalf(obj_form, row, column, checking_sides, c_tile_len, c_offset): return flatVerticalExtPartialSides(obj_form, row, column, [TOP_SIDE, LEFT_SIDE, RIGHT_SIDE], checking_sides, [False,False,False], False, c_tile_len/2, c_tile_len/6, c_tile_len, c_offset)

def noResFlatT_Bottom3_4ths(obj_form, row, column, checking_sides, c_tile_len, c_offset): return flatVerticalExtPartialSides(obj_form, row, column, [TOP_SIDE], checking_sides, [False], False, c_tile_len/4, 0, c_tile_len, c_offset)








side_indices: dict[SideLabel, int] = {
    TOP_SIDE:    0,
    LEFT_SIDE:   1,
    BOTTOM_SIDE: 2,
    RIGHT_SIDE:  3
}

no_res_offset: list[float] = [  -1,  -1,  -1,  -1]

# [top, left, bottom, right]
OFFSETS: list[list[float]] = [
    no_res_offset,  # 0
    [   0,   0,   0,   0],  # 1
    [   0,  -1,  -1,  -1],  # 2
    [  -1,  -1,   0,  -1],  # 3
    [  -1,   0,  -1,  -1],  # 4
    [  -1,  -1,  -1,   0],  # 5
    [   0,  -1,   0,  -1],  # 6
    [  -1,   0,  -1,   0],  # 7
    [   0,   0,  -1,  -1],  # 8
    [   0,  -1,  -1,   0],  # 9
    [  -1,   0,   0,  -1],  # 10
    [  -1,  -1,   0,   0],  # 11
    [   0,   0,   0,  -1],  # 12
    [   0,  -1,   0,   0],  # 13
    [   0,   0,  -1,   0],  # 14
    [  -1,   0,   0,   0],  # 15
    [   0,   0,   0,   0],  # 16
    no_res_offset, # flatAllTopHalf, # 17
    no_res_offset, # flatB_TopHalf,  # 18
    no_res_offset, # flatL_TopHalf,  # 19
    no_res_offset, # flatR_TopHalf,  # 20
    [   0,  -1, 1/2,  -1],         # 21
    no_res_offset, # flatLRTopHalf,  # 22
    no_res_offset, # flatT_LTopHalf, # 23
    no_res_offset, # flatT_RTopHalf, # 24
    no_res_offset, # flatB_LTopHalf, # 25
    no_res_offset, # flatB_RTopHalf, # 26
    [   0,   0, 1/2,  -1],       # 27
    [   0,  -1, 1/2,   0],       # 28
    no_res_offset, # flatLR_TTopHalf, # 29
    no_res_offset, # flatLR_BTopHalf, # 30
    [ 1/4,  -1,  -1,  -1],     # 31
    [ 1/2,   0,  -1,   0]     # 32
]




COLLISIONS: list[Callable[ [dict[str, Vector2],
                            int,
                            int, 
                            list[SideLabel],
                            float, 
                            float], SideLabel] ] = [
    NO_RES,   # 0
    flatAll,  # 1
    flatT,    # 2
    flatB,    # 3
    flatL,    # 4
    flatR,    # 5
    flatTB,   # 6
    flatLR,   # 7
    flatT_L,  # 8
    flatT_R,  # 9
    flatB_L,  # 10
    flatB_R,  # 11
    flatTB_L, # 12
    flatTB_R, # 13
    flatLR_T, # 14
    flatLR_B, # 15
    noResFlatAll, # 16
    NO_RES, # flatAllTopHalf, # 17
    NO_RES, # flatB_TopHalf,  # 18
    NO_RES, # flatL_TopHalf,  # 19
    NO_RES, # flatR_TopHalf,  # 20
    flatTB_TopHalf,           # 21
    NO_RES, # flatLRTopHalf,  # 22
    NO_RES, # flatT_LTopHalf, # 23
    NO_RES, # flatT_RTopHalf, # 24
    NO_RES, # flatB_LTopHalf, # 25
    NO_RES, # flatB_RTopHalf, # 26
    flatTB_L_TopHalf,         # 27
    flatTB_R_TopHalf,         # 28
    NO_RES, # flatLR_TTopHalf, # 29
    NO_RES, # flatLR_BTopHalf, # 30
    noResFlatLR_T_BottomHalf,     # 31 # NOT WORKING for L/R
    noResFlatT_Bottom3_4ths     # 32
]


def collision_offset(collision_index: int, 
                     checking_side: SideLabel
                     ) -> float:
    side_index = side_indices[checking_side]
    
    return OFFSETS[collision_index][side_index]


# order collision functions from least to greatest offset
# ex:

# [ [0,   ...], 
#   [1/4, ...], 
#   [1/2, ...], 
#   ...        ]
def checking_order(collisions: list[TileInfo], 
                   checking_side: SideLabel
                   ) -> list[list[ TileInfo ]]:
    """Orders (tile_info.reference = collision function) from least to greatest offset
        
       list[ tile_info, ... ]
        
       ex: [ [0,   ...],  [1/4, ...], [1/2, ...], ... ]"""
    
    collision_offset__indices: dict[float, list[TileInfo]] = {}
    
    for tile_info in collisions:
        offset = collision_offset(tile_info.reference, checking_side)
        
        if (offset >= 0):
            collision_offset__indices.setdefault(offset,
                                                [])
            collision_offset__indices[offset].append((tile_info))
    
    collision_offsets: list[float] = sorted(collision_offset__indices.keys())
    
    return [collision_offset__indices[offset] # [tile_info, ...] with same offset
            for offset in collision_offsets]