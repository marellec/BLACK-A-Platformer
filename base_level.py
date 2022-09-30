
from abc import abstractmethod, ABC
from typing import Callable, Optional, Sequence
import pygame  # type: ignore

from pygame.surface import Surface  # type: ignore

from base_animation_pack import AnimationPack
from base_camera import Camera
from base_collision_observer import CollisionObserver
from base_entity_pack import EntityPack
from base_labels import Label
from base_tile_map_form import TileMapForm
from base_tile_maps import CollisionMap, TileMap
from base_tile_pack import TilePack, TilePackForm
from base_traits_entities import Entity
from controls import Controller
from loading.load_assets import (load_character_sprites,  # type: ignore
                                 load_level, 
                                 load_tile_pack_sprites)


from traits import trait_types

def retrieve_traits(trait_assets: Sequence[dict],
                    entity: Entity
                    ) -> Entity:
    for trait_info in trait_assets:
        entity.add_trait(trait_types[Label(trait_info["type_name"])](*trait_info["setup"]))
    return entity









class LevelForm:
    
    label: Label
    
    loaded: bool
    
    player: Optional[Entity]
    
    character_entity_pack: Optional[EntityPack]
    
    map_form: Optional[TileMapForm]
    
    tile_pack_form: Optional[TilePackForm]
    
    collision_observer: Optional[CollisionObserver]
    
    camera: Camera
    
    window: Surface
    
    def __init__(self,
                 label: Label):
        self.label = label
        self.loaded = False
        
    
    def load(self,
             scale: float,
             FPS: int,
             resourse_path_funct: Callable = lambda x: x):
        
        if (not self.loaded):
            
            # ASSETS
            self.assets = load_level(self.label, resourse_path_funct)
            
            # CHARACTER ENTITIES
            try: 
                self.character_entity_pack = EntityPack(
                    Label(self.label.name + "characters"),             
                    tuple( retrieve_traits(e_info["traits"], 
                                        Entity(
                        (label := Label(e_name)), 
                        self.assets["characters"]["entities"][e_name]["width"] * scale, 
                        self.assets["characters"]["entities"][e_name]["height"] * scale, 
                        self.assets["characters"]["entities"][e_name]["x"] * scale,
                        self.assets["characters"]["entities"][e_name]["y"] * scale,
                        AnimationPack(label, 
                                      load_character_sprites(self.assets, 
                                                             label,
                                                             scale, 
                                                             FPS,
                                                             resourse_path_funct))
                        )
                    )
                    for e_name, e_info in self.assets["characters"]["entities"].items() )
                )
                
                for entity in self.character_entity_pack.entities.values():
                    print(entity)
                
            except KeyError:
                self.character_entity_pack = None
                
                
            
            # PLAYER    
            try: 
                if (self.character_entity_pack is not None):
                    self.player = self.character_entity_pack[Label(self.assets["player"])]
                    print(self.player)
                else:
                    raise KeyError() # exit try: block
            except KeyError:
                self.player = None
            
            
            
            # MAP FORM
            try:
                self.map_form = TileMapForm(
                    tile_width= self.assets["tile width"] * scale,
                    tile_height= self.assets["tile height"] * scale,
                    tile_maps= tuple(
                        TileMap(Label(tile_map["name"]), 
                                tile_map["map"])
                        for tile_map in self.assets["tile maps"]
                    ),
                    collision_map= CollisionMap(Label("level 1 collision map"), 
                                                self.assets["collision map"])
                )
                
                print(self.map_form)
            except KeyError:
                self.map_form = None
            
            # TILE PACK FORM
            try:
                self.tile_pack_form = TilePackForm(
                    tuple( TilePack(Label(tile_pack_name), 
                                    load_tile_pack_sprites(self.assets,
                                                           tile_pack_name,
                                                           scale,
                                                           FPS,
                                                           resourse_path_funct))
                    for tile_pack_name in self.assets["tile packs"])
                )
            except KeyError:
                self.tile_pack_form = None
            
            # CAMERA
            
            if (self.map_form is not None):
                self.camera = Camera(self.map_form.w, self.map_form.h, 
                                     *(a * scale for a in self.assets["camera"]["setup"]))
            else:
                self.camera = Camera(0, 0, 
                                     *(a * scale for a in self.assets["camera"]["setup"]))
            
            print("camera size:", (self.camera.w, self.camera.h))
            
            # COLLISION OBSERVER
            
            if (self.map_form is not None):
                self.collision_observer = CollisionObserver(self.map_form.tile_width)
            else:
                self.collision_observer = None
            
            
            self.loaded = True
            
            
            
         
         
   
class Level(ABC):
    
    label: Label
    form: LevelForm
    
    
    def __init__(self, 
                 label: Label):
        self.label = label
        self.form = LevelForm(self.label)
        
    
    @abstractmethod
    def update(_, form: LevelForm, controller: Controller, dt: int):
        pass
    
    @abstractmethod
    def display(_, form: LevelForm, dt: int):
        pass
    
    @abstractmethod
    def setup(self, stuff___):
        """load level (if not loaded yet)
        
        \ngive extra progress information that persists across levels
        \nreturn self.form"""
        
        pass
    
    # @abstractmethod
    def start(self):
        
        
        self.paused = False
        pass
    
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    # @abstractmethod
    def end(self):
        
        
        self.paused = True
        pass