
from typing import Optional
from base_folder import Folder, abstract_Folder_method
from base_labels import Label
from base_sprite_animator import SpriteAnimator



class TilePack():
    
    label: Label
    tiles: tuple[Optional[SpriteAnimator], ...]
    
    def __init__(self, 
                 label: Label,
                 tiles: tuple[Optional[SpriteAnimator], ...]):
        self.label = label
        self.tiles = tuple(t for t in tiles)
        
    def __getitem__(self, tile_index: int
                    ) -> Optional[SpriteAnimator]:
        return self.tiles[tile_index]



class TilePackForm(metaclass=Folder):
    
    folder_name = "tile_packs"
    
    tile_packs: dict[Label, TilePack]
    
    def __init__(self, 
                 tile_packs: tuple[TilePack, ...] = tuple()):
        self.tile_packs = {t.label : t for t in tile_packs}

    def add_tile_pack(self, tile_pack_label: Label, tile: TilePack):
        self.tile_packs[tile_pack_label] = tile
        return self
    
    @abstract_Folder_method
    def remove_tile_pack(self, tile_pack_label: Label):
        pass
    
    @abstract_Folder_method
    def __getitem__(self, tile_pack_label: Label
                    ) -> TilePack:
        pass