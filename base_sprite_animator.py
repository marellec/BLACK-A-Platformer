
import pygame # type: ignore
from pygame.surface import Surface # type: ignore
from base_labels import Label
from base_spritesheet import Spritesheet
from vectormath.vector import Vector2 # type: ignore

class SpriteAnimator(object):
    """sprite strip animator
    
    This class provides an iterator 
    -    (__iter__() and __next__() methods), and a
    -    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    
    label: Label
    
    @property
    def frames(self) -> list[Surface]: return self._frames
    
    @property
    def loop(self) -> bool: return self._loop
    
    @property
    def frame_delay(self) -> int: return self._frame_delay
    
    @property
    def finished(self) -> bool: return self._finished
    
    @property
    def size(self) -> Vector2: return self._size.copy()
    @size.setter
    def size(self, v: Vector2): self._size = v.copy()
    
    @property
    def offset(self) -> Vector2: return self._offset.copy()
    
    def __init__(self,
                 *,
                 label: Label,
                 filename: str, 
                 rect: tuple[float, float, 
                             float, float],
                 colorkey = None, 
                 frame_count: int,
                 loop: bool = False, 
                 frame_delay: int = 1,
                 scale: float = 1,
                 crop_size: Vector2 = Vector2()):
        """construct a SpriteAnimator
        
        -    filename, rect, frame_count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        -    loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        -    frame_delay is the number of ticks to return the same image before
        the iterator advances to the next image.
        
        -    crop_size is the size of the game object that the animation is displaying
        (defaults to the same size as the image)
        """
        self.label = label
        ss = Spritesheet(label, filename)
        self._frames = ss.load_strip(rect, frame_count, colorkey)
        self.scale(scale)
        self._i = 0
        self._loop = loop
        self._frame_delay = frame_delay
        self._f = frame_delay
        self._finished = False
        
        crop_size = crop_size.copy()
        
        self.size = Vector2(rect[2], rect[3])
        
        if (crop_size.all() == Vector2().all()):
            crop_size = self.size
            
        self.size *= scale
        crop_size *= scale
        
        self._offset = Vector2((crop_size.x - self.size.x) / 2,
                                crop_size.y - self.size.y)
        
        
        print()
        print(f"{self.size = }")
        print(f"{crop_size = }")
        print(f"{self.offset = }")
        
        
    
    def __iter__(self):
        self._i = 0
        self._f = self.frame_delay
        self._finished = False
        return self
    
    def __next__(self) -> Surface:
        image = self.frames[self._i]
        self._f -= 1
        if self._f == 0:
            self._i += 1
            self._f = self.frame_delay
            
            if self._i >= len(self.frames):
                if self.loop:
                    self._i = 0
                else:
                    self._i = len(self.frames) - 1
                    self._finished = True
        return image
    
    def scale(self, /, scalar: float):
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, 
                                                    (frame.get_width() * scalar, 
                                                     frame.get_height() * scalar))
        return self
    
    def image(self):
        return self.frames[self._i]
    
    def __add__(self, ss: "SpriteAnimator"):
        self.frames.extend(ss.frames)
        return self