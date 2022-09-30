
from base_folder import Folder, abstract_Folder_method
from base_labels import Label
from base_tile_maps import TileMap, CollisionMap


class TileMapForm(metaclass=Folder):
    
    
    folder_name = "tile_maps"
        
    tile_maps: dict[Label, TileMap] # folder
    
    
    collision_map: CollisionMap
    
    @property
    def w(self) -> float: return self._w
    @property
    def h(self) -> float: return self._h
    
    @property
    def tile_width(self) -> float: return self._tile_width
    @property
    def tile_height(self) -> float: return self._tile_height
    
    def __init__(self,
                 *,
                 tile_width: float, 
                 tile_height: float, 
                 tile_maps: tuple[TileMap, ...], 
                 collision_map: CollisionMap):
        self._x: float = 0
        self._y: float = 0
        self._w = collision_map.width() * tile_width
        self._h = collision_map.height() * tile_height
        self._tile_width = tile_width
        self._tile_height = tile_height
        self.tile_maps = {m.label : m for m in tile_maps}
        self.collision_map = collision_map
        
    def add_tile_map(self,  tile_map: TileMap):
        self.tile_maps[tile_map.label] = tile_map
        return self             
        
    abstract_Folder_method
    def remove_tile_map(self, tile_map_label: Label):
        pass
       
    @abstract_Folder_method 
    def __getitem__(self, tile_map_label: Label) -> TileMap:
        pass
    
    def __str__(self) -> str:
        return ("TileMapForm:" + f"\n< {self.tile_width}, {self.tile_height} >" +
                "".join("\n\n " + str(m) for m in self.tile_maps.values()) +
                "\n\n " + str(self.collision_map) )
