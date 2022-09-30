

from base_tile_map_form import TileMapForm 
from base_traits_entities import Entity


class Camera:
    
    @property
    def x(self) -> float: return self._x
    @property
    def y(self) -> float: return self._y
    @property
    def w(self) -> float: return self._w
    @property
    def h(self) -> float: return self._h
    
    @property
    def max_x(self) -> float: return self._max_x
    @property
    def max_y(self) -> float: return self._max_y
    
    @property
    def anchor_x_proportion(self) -> float: return self._anchor_x_proportion
    @property
    def anchor_y_proportion(self) -> float: return self._anchor_y_proportion
    
    def __init__(self, 
                 world_w: float, world_h: float, 
                 w: float, h: float,
                 anchor_x_proportion: float = 1/2, 
                 anchor_y_proportion: float = 1/2,
                 x: float = 0, y: float = 0):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        
        self._max_x = (world_w - self.w) if (world_w > 0) else self.w
        self._max_y = (world_h - self.h) if (world_h > 0) else self.h
        
        self._anchor_x_proportion = anchor_x_proportion
        self._anchor_y_proportion = anchor_y_proportion
    
    def anchorX(self, w: float) -> float: 
        return self.x + self.anchor_x_proportion * (self.w - w) 
    
    def anchorY(self, h: float) -> float: 
        return self.y + self.anchor_y_proportion * (self.h - h) 
    
    def follow(self,
               x: float,     y: float, 
               w: float = 0, h: float = 0):
        # find new camera position
        dx =  x - self.anchorX(w);
        x  =  max(0, min(self.x + dx, self.max_x))
        
        dy =  y - self.anchorY(h)
        y  =  max(0, min(self.y + dy, self.max_y))
        
        # set new camera position
        self._x = x
        self._y = y
    
    def follow_entity(self, entity: Entity):
        self.follow(entity.pose.x, entity.pose.y, 
                    entity.size.x, entity.size.y)
        
    