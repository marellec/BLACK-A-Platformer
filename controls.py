

from enum import Enum, auto
from typing import Optional, Sequence, Union
import pygame # type: ignore
from base_labels import DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP, Label


class ControlInput(Enum):
    
    PRESSED = auto()
    DOWN = auto()
    RELEASED = auto()


class ControlPreset:
    
    AWSD = ((DIR_LEFT,  pygame.K_a),
            (DIR_UP,    pygame.K_w),
            (DIR_DOWN,  pygame.K_s),
            (DIR_RIGHT, pygame.K_d))

    UP_DOWN_LEFT_RIGHT = ((DIR_UP,    pygame.K_UP),
                          (DIR_DOWN,  pygame.K_DOWN),
                          (DIR_LEFT,  pygame.K_LEFT),
                          (DIR_RIGHT, pygame.K_RIGHT))



class Key:
    
    label: Label
    
    @property
    def code(self) -> int: return self._code
    
    @property
    def pressed(self) -> bool: return self._pressed
    @pressed.setter
    def pressed(self, val: bool): self._pressed = val
    
    @property
    def prev_down(self) -> int: return self._prev_down
    @prev_down.setter
    def prev_down(self, val: int): self._prev_down = val
    
    @property
    def down(self) -> int: return self._down
    @down.setter
    def down(self, val: int): self._down = val
    
    @property
    def released(self) -> bool: return self._released
    @released.setter
    def released(self, val: bool): self._released = val
    
    def __init__(self, label: Label, code: int):
        self.label = label
        self._code = code
        
        self.pressed = False
        self.prev_down = 0
        self.down = 0
        self.released = False
    
    def get_state(self, 
                  input_type: ControlInput
                  ) -> bool:
        state = True
        
        if   (input_type == ControlInput.PRESSED): 
            state =  self.pressed
        elif (input_type == ControlInput.DOWN): 
            state =  self.down > 0
        elif (input_type == ControlInput.RELEASED): 
            state =  self.released
        
        return state




class Controller():
    
    keys: dict[int, Key]
    
    name_map: dict[Label, int]
    
    pushed_keys: Sequence[bool]
    
    def __init__(self,
                 *, # presets optional
                 presets: Optional[tuple[tuple[tuple[Label, 
                                                     int], ...]]] = None,
                 key_mappings: Optional[tuple[tuple[Label, 
                                                    int], ...]] = None):
        
        self.keys = {}
        self.name_map = {}
        
        if (presets is not None):
            
            for preset in presets:
                self.keys = {code : Key(label, code) for label, code in preset}
                self.name_map = {label : code for label, code in preset}
        if (key_mappings is not None):
            
            for label, code in key_mappings:
                self.add_key(label, code)
    
    
    def update(self, keydown_states: Sequence[bool]):
        """At the start of each frame"""
        
        for key_code, key in self.keys.items():
            
            if (keydown_states[key_code] == True):
                key.down += 1
                
                if (key.down == 1): key.pressed = True
                else              : key.pressed = False
        
        
    
    def press(self, key_code: int):
        if (key_code in self.keys):
            self.keys[key_code].pressed = True
            self.keys[key_code].released = False
            
    def release(self, key_code: int):
        if (key_code in self.keys):
            self.keys[key_code].pressed = False
            self.keys[key_code].prev_down = self.keys[key_code].down
            self.keys[key_code].down = 0
            self.keys[key_code].released = True
    
            
    def convert_to_code(self, 
                        key_nameORcode: Union[Label, int]
                        ) -> int:
        key_code = 0
        if (isinstance(key_nameORcode, Label)):
            key_code = self.name_map[key_nameORcode]
        return key_code
    
            
    def get_key_state(self, 
                      key_nameORcode: Union[Label, int], 
                      input_type: ControlInput) -> bool:
        return (self.keys[self.convert_to_code(key_nameORcode)]
                    .get_state(input_type))
        
    def get_prev_down(self, key_nameORcode: Union[Label, int]) -> int:
        return self.keys[self.convert_to_code(key_nameORcode)].prev_down
        
    def get_down(self, key_nameORcode: Union[Label, int]) -> int:
        return self.keys[self.convert_to_code(key_nameORcode)].down
    
    
    def add_key(self, label: Label, code: int):
        key = Key(label, code)
        self.keys[code] = key
        self.name_map[label] = code
        return self
        
    def remove_key(self, 
                   key_nameORcode: Union[Label, int]):
        del self.keys[self.convert_to_code(key_nameORcode)]
        return self
    