
from typing import Optional
from base_animation_pack import AnimationPack
from base_folder import Folder, abstract_Folder_method
from base_labels import Label
from base_toggleable import Toggleable
from controls import Controller
from tile_collisions import TileInfo
import utility_modules.utility_decor as ud # type: ignore
from utility_modules.utility_decor import not_implemented # type: ignore
from utility_modules.pretty_printing import str_Vector2 # type: ignore
from vectormath.vector import Vector2 # type: ignore




class Trait:
    
    """Base for every trait an entity can have, comes with:
    
      -    a Label
      -    non-implemented optional methods
      
      goes together with:
      -    bool functions to check whether a trait has an optional method"""
    
    label: Label
    
    def __init__(self):
        pass
    
    @not_implemented
    def restart(self, entity: "Entity"):
        raise NotImplementedError("This trait doesn't restart")
    
    @not_implemented
    def respond_to_input(self, 
                         entity: "Entity",
                         controller: Controller,
                         dt: int):
        """Responds to controller input"""
        raise NotImplementedError("This trait doesn't respond to input")
    
    @not_implemented
    def update(self, 
               entity: "Entity",
               dt: int):
        """Updates"""
        raise NotImplementedError("This trait doesn't update")
    
    @not_implemented
    def handle_collision(self, 
                         entity: "Entity",
                         tile_infos: tuple[TileInfo, ...],
                         tiles: tuple[tuple[tuple[Label, Label], 
                                            ...],
                                      ...]):
        """Handles tile collision"""
        raise NotImplementedError("This trait doesn't handle collision")
    






def is_toggleable(trait: Trait) -> bool:
    return isinstance(trait, Toggleable)
    
def is_restartable(trait: Trait) -> bool:
    return ud.is_implemented(Trait, trait.restart)

def is_respond_to_input_able(trait: Trait) -> bool:
    return ud.is_implemented(Trait, trait.respond_to_input)

def is_updateable(trait: Trait) -> bool:
    return ud.is_implemented(Trait, trait.update)
    
def is_handle_collision_able(trait: Trait) -> bool:
    return ud.is_implemented(Trait, trait.handle_collision)














class Entity(metaclass=Folder):
    """Every game entity (not background or text) comes with:
    
    -    a Label
    -    size, pose, prev, delta, & accl (Vector2)
    
    -    Trait dictionary { }
    -    add/remove_trait( ) methods
    -    get trait by indexing ( __getitem__( ) )
    
    -    delegates these methods to its traits:
    
    -    respond_to_input( )
    -    update( )
    -    restart( )
    -    handle_collision( )"""
    
    folder_name = "traits"
    
    label: Label
    traits: dict[Label, Trait] # folder
    
    @property
    def size(self) -> Vector2: return self._size.copy()
    @size.setter
    def size(self, v: Vector2): self._size = v.copy()
    
    @property
    def pose(self) -> Vector2: return self._pose.copy()
    @pose.setter
    def pose(self, v: Vector2): self._pose = v.copy()
    
    @property
    def prev(self) -> Vector2: return self._prev.copy()
    @prev.setter
    def prev(self, v: Vector2): self._prev = v.copy()
    
    @property
    def delta(self) -> Vector2: return self._delta.copy()
    @delta.setter
    def delta(self, v: Vector2): self._delta = v.copy()
    
    @property
    def accl(self) -> Vector2: return self._accl.copy()
    @accl.setter
    def accl(self, v: Vector2): self._accl = v.copy()
    
    animation_pack: Optional[AnimationPack]
    
    def __init__(self,
                 label: Label,
                 w: float, h: float, 
                 x: float = 0, y: float = 0,
                 animation_pack: Optional[AnimationPack] = None):
        self.label = label
        self.traits = {}
        
        self.size = Vector2(w, h)
        
        self.pose = Vector2(x, y)
        self.prev = self.pose
        self.delta = Vector2(0, 0)
        self.accl = Vector2(0, 0)
        
        self.animation_pack = animation_pack
        
    
    def add_trait(self, trait: Trait):
        self.traits[trait.label] = trait
        return self
        
    @abstract_Folder_method
    def remove_trait(self, trait_label: Label):
        pass
        
    @abstract_Folder_method
    def __getitem__(self, trait_label: Label) -> Trait:
        pass
    
    def restart(self):
        for trait in self.traits.values():
            if (is_toggleable(trait)): 
                trait.enable()
            if (is_restartable(trait)): 
                trait.restart()
    
    def respond_to_input(self,
                         controller: Controller,
                         dt: int):
        for trait in self.traits.values():
            if (is_respond_to_input_able(trait)): 
                trait.respond_to_input(self, controller, dt)
    
    def update(self,
               dt: int):
        for trait in self.traits.values():
            if (is_updateable(trait)): 
                trait.update(self, dt)
       
    def handle_collision(self, 
                         tile_infos: tuple[TileInfo, ...],
                         tiles: tuple[tuple[tuple[Label, Label], 
                                            ...],
                                      ...]):
        """Each tile in tiles should be (tile label, TilePack.label)"""
        for trait in self.traits.values():
            if (is_handle_collision_able(trait)): 
                trait.handle_collision(self, tile_infos, tiles)
                
    def __str__(self) -> str:
        return ( (f"'{self.label.name}': Entity\n"
                  f"\n    size:  {str_Vector2(self.size)}\n"
                  f"\n    pose:  {str_Vector2(self.pose)}"
                  f"\n    prev:  {str_Vector2(self.prev)}"
                  f"\n    delta: {str_Vector2(self.delta)}"
                  f"\n    accl:  {str_Vector2(self.accl)}\n") +
                "".join(f"\n    {t}" for t in self.traits.values()))
                

                
# print("\n")

# e = Entity(Label("e"), 50, 50)
# print(e)

# print("\n")