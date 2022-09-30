
from abc import ABC, abstractmethod
from base_traits_entities import *

from base_labels import BOTTOM_SIDE, Label, DIR_UP, TOP_SIDE, DIR_LEFT, DIR_RIGHT
from base_toggleable import Toggleable
from button_traits import KICK, PUSH, Kick, Push
from combos import Combo1Key
from controls import Controller, ControlInput
from utility_modules.utility_decor import has_implemented # type: ignore

from vectormath.vector import Vector2 # type: ignore



TILE_COLLISION = Label("TileCollision")
class TileCollision(Toggleable, Trait):

    label: Label = TILE_COLLISION
    
    def __init__(self):
        super().__init__()


ACCELERATION = Label("Acceleration")
@has_implemented(Trait, 
                 update=True)
class Acceleration(Trait):
    
    label: Label = ACCELERATION
    
    def __init__(self):
        super().__init__()
    
    def update(self, 
               entity: Entity,
               dt: int):
        entity.delta += entity.accl


TRANSPORTATION = Label("Transportation")
@has_implemented(Trait, 
                 update=True)
class Transportation(Trait):
    
    label: Label = TRANSPORTATION
    
    def __init__(self):
        super().__init__()
    
    def update(self, 
               entity: Entity,
               dt: int):
        entity.prev = entity.pose.copy()
        entity.pose += entity.delta


GRAVITY = Label("Gravity")
@has_implemented(Trait, 
                 update=True)
class Gravity(Toggleable, Trait):
    
    label: Label = GRAVITY
    
    g_force: float
    
    def __init__(self, 
                 /,
                 g_force: float):
        super().__init__()
        self.g_force = g_force
    
    def update(self, 
               entity: Entity,
               dt: int):
        entity.delta += Vector2(0, self.g_force)


XMOTION = Label("XMotion")

@has_implemented(Trait, 
                 respond_to_input=True,
                 update=True)
class XMotion(ABC, Toggleable, Trait):
    
    label: Label = XMOTION

    direction: int = 0
    heading: int = 1
    distance: float = 0
    
    speed: float
    accl: float = 0
    decl: float = 0
    drag_factor: float = 0
    
    def __init__(self, 
                 /,
                 speed: float, 
                 accl: float = 0,
                 decl: float = 0,
                 drag_factor: float = 0):
        super().__init__()
        
        self.direction = XMotion.direction
        self.heading = XMotion.heading
        self.distance = XMotion.distance
        
        self.speed = speed
        self.accl = accl
        self.decl = decl
        self.drag_factor = drag_factor
        
        
        
    def respond_to_input(self, 
                         entity: Entity,
                         controller: Controller,
                         dt: int):
        """Get player X-motion direction from controller input"""
        if   (controller.get_key_state(DIR_LEFT, 
                                       ControlInput.DOWN)):
            self.direction = -1
        elif (controller.get_key_state(DIR_RIGHT, 
                                       ControlInput.DOWN)):
            self.direction =  1
        else:
            self.direction =  0
    
    @abstractmethod  
    def update(self, 
               entity: Entity,
               dt: int):
        pass
    
    def __str__(self) -> str:
        return (f"{self.label.name}(speed= {self.speed}, "
                f"accl= {self.accl}, "
                f"decl= {self.decl}, "
                f"drag= {self.drag_factor})")


CONSTANTXMOTION = Label("ConstantXMotion")
class ConstantXMotion(XMotion):
    
    type: Label = CONSTANTXMOTION
    
    def __init__(self, 
                 /,
                 speed: float):
        super().__init__(speed, 0, 0, 0)
        
    def update(self, 
               entity: Entity,
               dt: int):
        pass
    
    def __str__(self) -> str:
        return (f"{self.label.name}(speed= {self.speed})")


VARIABLEXMOTION = Label("VariableXMotion")
class VariableXMotion(XMotion):
    
    type: Label = VARIABLEXMOTION
    
    def __init__(self, 
                 /,
                 speed: float, 
                 accl: float = 0,
                 decl: float = 0,
                 drag_factor: float = 0):
        super().__init__(speed, 
                         accl,
                         decl,
                         drag_factor)
        
    def update(self, 
               entity: Entity,
               dt: int):
        
        dx: float = entity.delta.x
        abs_dx: float = abs(dx)
        
        if (self.direction != 0):
            dx += self.accl * self.direction * dt
            self.distance += abs_dx * dt
            
            self.heading = self.direction
        elif (dx != 0):
            deceleration: float = min(abs_dx, self.decl * dt)
            dx += -deceleration if (dx > 0) else deceleration
        else:
            self.distance = 0
        
        drag: float = self.drag_factor * dx * abs_dx
        dx -= drag
        
        entity.delta = Vector2(dx, entity.delta.y)


# x = VariableXMotion(1, 2, 3, 4)
# y = ConstantXMotion(3)
    
# print()

# print(x)
# print(y)

# import inspect
# print(inspect.isabstract(XMotion)) 
# print(issubclass(VariableXMotion, Trait))

# print(isinstance(x, XMotion))
# print(*(f"{k} : {v}" for k, v in x.__dict__.items()), sep="\n")
# print(is_updateable(x))
# print(is_restartable(x))
# print(x.able)
# x.disable()
# print(x.able)
# print()
# print()


JUMP = Label("Jump")

@has_implemented(Trait, 
                 respond_to_input=True,
                 update=True,
                 handle_collision=True)
class Jump(Toggleable, Trait):
    
    label: Label = JUMP
    
    combo: Combo1Key
    
    # STILL UNSURE HOW IT WORKS
    @property
    def jumping(self) -> bool: return self.combo.confirmed_performing
    
    falling: bool
    grounded: bool
    
    dy: float
    
    
    def __init__(self, 
                 /,
                 dy: float, 
                 max_time: int,
                 accept_time: int = 1):
        super().__init__()
        
        def perform(entity: Entity,
                    dt: int):
            self.perform(entity, dt)
        
        def cancel():
            self.cancel()
        
        self.combo = Combo1Key(DIR_UP, 
                               max_time, 
                               accept_time, 
                               perform, 
                               cancel)
        
        self.falling = False
        self.grounded = False
        
        self.dy = dy
    
    def respond_to_input(self, 
                         entity: Entity,
                         controller: Controller,
                         dt: int):
        self.combo.respond_to_input(entity, controller=controller, dt=dt)
    
    def update(self, 
               entity: Entity,
               dt: int):
        
        # print()
        
        if (entity.delta.y > 0): # may need to confirm falling after 2 frames
            self.grounded = False
            self.falling = True
        
        
        if (self.combo.confirmed):
            self.grounded = False
            # print(f"START JUMP")
        
        # print(f"{self.falling = }")
        # print(f"{self.jumping = }")
    
    def handle_collision(self,
                         entity: Entity,
                         tile_infos: tuple[TileInfo, ...],
                         tiles: tuple[tuple[tuple[Label, Label], 
                                            ...],
                                      ...]):
        for tile_info, tile_labels in zip(tile_infos, tiles):
            
            affects_jump = False
            for tile_label, tile_pack_label in tile_labels:
                
                # check if any tiles affect jump
                affects_jump = True 
            
            if (affects_jump):
                if   (tile_info.tile_side == TOP_SIDE):
                    self.combo.can_perform = True
                    self.falling = False
                    self.grounded = True
                    # print(f"{self.falling = }")
                    # print(f"{self.grounded = }")
                elif (tile_info.tile_side == BOTTOM_SIDE):
                    self.combo.cancel()
            
    def cancel(self):
        self.falling = True
        # print(f"{self.falling = }")
    
    def perform(self, entity: Entity, dt: int):
        entity.delta = Vector2(entity.delta.x, self.dy)
    

# j = Jump(-5, 10, 4)


# print()
# print(isinstance(j, Trait))
# print(is_toggleable(j))
# print(j.label)
# print(*(f"{k} : {v}" for k, v in j.__dict__.items()), sep="\n")
# print(is_updateable(j))
# print(j.able)
# j.disable()
# print(j.able)
# print()


trait_types: dict[Label, type[Trait]] = {
    
    TILE_COLLISION:     TileCollision,
    ACCELERATION:       Acceleration,
    TRANSPORTATION:     Transportation,
    GRAVITY:            Gravity,
    CONSTANTXMOTION:    ConstantXMotion,
    VARIABLEXMOTION:    VariableXMotion,
    JUMP:               Jump,
    
    PUSH:               Push,
    KICK:               Kick
    
}



def is_tile_collision_able(entity: Entity):
    try: 
        _ = entity[TILE_COLLISION]
        return True
    except AttributeError: 
        return False