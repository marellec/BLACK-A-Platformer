
from base_labels import Label
from numpy import ndarray # type: ignore
import numpy as np  # type: ignore


# holds array of tile indices
class TileMap:
    
    label: Label
    _array: ndarray
    
    def __init__(self, label: Label, arr: tuple[tuple[int, ...], ...]):
        self.label = label
        self._array = np.array(arr, dtype=int)
        
    def width(self) -> int:
        return len(self._array[0])
    
    def height(self) -> int:
        return len(self._array)
    
    # get tile by index
    def __getitem__(self, key: int):
        return self._array[key]
    
    def __str__(self) -> str:
        return (f"tile map: {self.label.name} \n\n" + 
                "".join((" " if (ch == "[" or ch == "]") else ch) 
                        for ch in str(self._array)))



# holds array of collision function indices
# int[][] collision_map with #'s that each 
# route to a function from tile_collisions.COLLISIONS
class CollisionMap(TileMap):
    
    label: Label
    _array: ndarray
    
    def __init__(self, label: Label, arr: tuple[tuple[int, ...], ...]):
        super().__init__(label, arr)
        
    # if index out of bounds, return -1
    def get_tile(self, row: int, column: int) -> int:
        return (self[row][column] 
                if (0 <= row    < len(self._array) and
                    0 <= column < len(self._array[0]))
                else -1)
        


# print("\n")


# FOREGROUND = Label("foreground")

# t = TileMap( FOREGROUND,
#              (3, 0, 0, 3, 0, 0),
#              (0, 0, 2, 3, 0, 0),
#              (0, 5, 0, 3, 0, 0),
#              (1, 0, 4, 3, 0, 0) )

# print(t)
# print(t[0][5])

# t[0][0] = 7

# print(t)

# print("\n")