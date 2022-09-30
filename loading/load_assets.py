


import json
from typing import Callable, Optional

from vectormath.vector import Vector2 # type: ignore
from base_labels import Label
from base_sprite_animator import SpriteAnimator




def load_level(level: Label,
               resourse_path_funct: Callable = lambda x: x
               ) -> dict:
    
    filename = resourse_path_funct(f"data/{level.name}.json")
    
    with open(filename, "r", encoding='utf-8-sig') as f:
        level_assets: dict = json.load(f)
    
    print(f"loaded level '{level.name}' from {filename}.json")
    
    return level_assets






def load_tile_pack_sprites(level_assets: dict,
                           tile_pack_name: str,
                           scale: float, 
                           FPS: int,
                           resourse_path_funct: Callable = lambda x: x
                           ) -> tuple[Optional[SpriteAnimator], ...]:
    
    dictionary: dict = level_assets["tile packs"][tile_pack_name]
    
    filename: str = resourse_path_funct("images/" + dictionary["filename"] + ".png")
    
    tile_w = level_assets["tile width"]
    tile_h = level_assets["tile height"]
    
    colorkey = dictionary["colorkey"]
    
    tiles = tuple(
            (SpriteAnimator(
                label=Label(string),
                filename=filename, 
                rect=(level_assets["tiles"][string]["index"][0], 
                      level_assets["tiles"][string]["index"][1], 
                      tile_w, tile_h), 
                frame_count=level_assets["tiles"][string]["count"], 
                colorkey=colorkey, 
                loop=level_assets["tiles"][string]["loop"],
                frame_delay=(FPS // level_assets["tiles"][string]["frame_dividend"]),
                scale=scale)
            if (string is not None) else None)
        for string in dictionary["tiles"]
    )
    
    print(f"loaded tile sprites '{tile_pack_name}' "
          f"from {filename}")
    
    return tiles







def load_character_sprites(level_assets: dict, 
                           character: Label,
                           scale: float,
                           FPS: int,
                           resourse_path_funct: Callable = lambda x: x
                           ) -> tuple[SpriteAnimator, ...]:
    
    filename: str = resourse_path_funct("images/" + level_assets["characters"]["filename"] + ".png")
    
    character_dict: dict = level_assets["characters"]["entities"][character.name]
    
    crop_size = Vector2(character_dict["width"], character_dict["height"])
    
    dictionaries: list[dict] = level_assets["characters"]["entities"][character.name]["animations"]
    
    animations = tuple(
        SpriteAnimator(
            label=Label(dictionary["name"]),
            filename=filename, 
            rect=dictionary["rect"], 
            frame_count=dictionary["count"], 
            colorkey=dictionary["colorkey"], 
            loop=dictionary["loop"],
            frame_delay=(FPS // dictionary["frame_dividend"]),
            scale=scale,
            crop_size=crop_size
        )
        for dictionary in dictionaries
    )
    
    print(f"loaded character sprites of '{character.name}' "
          f"from {filename}")
    
    return animations




