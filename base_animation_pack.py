
from typing import Optional

import pygame # type: ignore
from base_folder import Folder, abstract_Folder_method, special_implementation
from base_labels import Label
from loading.load_assets import load_character_sprites # type: ignore
from base_sprite_animator import SpriteAnimator


class AnimationPack(metaclass=Folder):
    
    folder_name = "animations"
    folder_key = Label
    folder_value = SpriteAnimator
    
    label: Label

    animations: dict[Label, SpriteAnimator]
    
    @property
    def current_animation_label(self) -> Label:
        return self._current_animation_label
    
    @current_animation_label.setter
    def current_animation_label(self, val: Label):
        if (val in self.animations or val == Label("None")): 
            self._current_animation_label = val
        else:
            raise ValueError(f"Animation {val} is not in animation pack '{self.label.name}'")
    
    def __init__(self, 
                 label: Label, 
                 animations: tuple[SpriteAnimator, ...],
                 *,
                 current_animation_index: int = 0):
        self.label = label
        self.animations = {a.label : a for a in animations}
        self._current_animation_label = (animations[current_animation_index].label 
                                         if (len(self.animations) > 0) else Label("None"))
    
    @special_implementation
    def add_animation(self, 
                      *,
                      # either just these to add all animations OR
                      level_assets: dict = None,
                      FPS: int = 60,
                      scale: float = 1,
                      # these to add 1 animation (same as SpriteAnimator())
                      label: Optional[Label] = None,
                      filename: str = "", 
                      rect: tuple[float, float, 
                                  float, float] = (0, 0, 0, 0),
                      colorkey: float = None, 
                      frame_count: int = 0, 
                      loop: bool = False, 
                      frame_delay: int = 1):
        
        if (level_assets is not None):
            animation = load_character_sprites(level_assets, 
                                               self.label,
                                               scale,
                                               FPS)
            self.animations[animation.label] = animation
            
        elif (label is not None):
            self.animations[label] = SpriteAnimator(label= label,
                                                         filename= filename,
                                                         rect= rect,
                                                         colorkey= colorkey,
                                                         frame_count= frame_count,
                                                         loop= loop,
                                                         frame_delay= frame_delay,
                                                         scale=scale)
        return self
    
    @abstract_Folder_method
    def remove_animation(self, label: Label):
        pass
    
    @abstract_Folder_method
    def __getitem__(self, label: Label) -> SpriteAnimator:
        pass
    
    def __bool__(self): 
        return (len(self.animations) > 0 and 
                self.current_animation_label != Label("None"))
    
    def current_animation(self) -> SpriteAnimator:
        return self.animations[self.current_animation_label]
    
    