

from random import randint
from base_labels import DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP, DirLabel, Label
from base_toggleable import Toggleable
from base_traits_entities import Entity, Trait
from combos import Combo
from controls import ControlInput, Controller
from utility_modules.utility_decor import has_implemented # type: ignore
from vectormath.vector import Vector2 # type: ignore




PUSH = Label("Push")
@has_implemented(Trait,
                 respond_to_input=True)
class Push(Toggleable, Trait):
    
    label: Label = PUSH
    
    pushed: bool
    
    dir_label: Label
    
    def __init__(self, 
                 /,
                 dir_label_name: str):
        super().__init__()
        self.pushed = False
        self.dir_label = DirLabel(dir_label_name)
        
    def respond_to_input(self, 
                         entity: Entity,
                         controller: Controller,
                         dt: int):
        # PRESS
        if (controller.get_key_state(self.dir_label, 
                                     ControlInput.PRESSED)):
            if (entity.animation_pack):
                entity.animation_pack.current_animation_label = Label("pushed")
                iter(entity.animation_pack.current_animation())
            
            
        # RELEASE
        elif (controller.get_key_state(self.dir_label, 
                                       ControlInput.RELEASED)):
            if (entity.animation_pack):
                entity.animation_pack.current_animation_label = Label("idle")
    
        
            
            

        
        
KICK = Label("Kick")
@has_implemented(Trait, 
                 respond_to_input=True,
                 update=True)
class Kick(Toggleable, Trait):
    
    label: Label = KICK
    
    combo: Combo
    
    @property
    def kicking(self) -> bool: return self._kicking > 0
    
    def __init__(self, /):
        super().__init__()
        
        def perform(dt: int):
            print("\nKICK!!!\n")
            self._kicking = 5
            
        def cancel():
            print("\n...oops...\n")
            
        self._kicking = 0
        
        self.combo = Combo( self.label,
                            (DIR_LEFT, DIR_RIGHT, DIR_UP), 
                            perform,
                            cancel
                            # excepted_keys=[DIR_UP]
                            )
    
    def respond_to_input(self, 
                         entity: Entity,
                         controller: Controller,
                         dt: int):
        self.combo.respond_to_input(controller=controller, dt=dt)
        
    def update(self, 
               entity: Entity,
               dt: int):
        
        if (self._kicking == 0):
            # randomly generate new combo
            dirs = (DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN)
            
            self.combo.sequence = ( dirs[randint(0, 3)], 
                                    dirs[randint(0, 3)], 
                                    dirs[randint(0, 3)] )
        
        self._kicking -= 1