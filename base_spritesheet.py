from typing import Union
import pygame # type: ignore
from pygame.surface import Surface # type: ignore
from pygame.rect import Rect # type: ignore

from base_labels import Label

# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)



class Spritesheet(object):
    
    sheet: Surface
    label: Label
    
    def __init__(self, label: Label, filename: str):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.label = label
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise (SystemExit, message) # type: ignore
    
    # Load a specific image from a specific rectangle
    def image_at(self,
                 rect: Union[tuple[float, float, 
                                   float, float], 
                             Rect], 
                 colorkey = None
                 ) -> Surface:
        "Loads image from x, y, x+offset, y+offset"
        rect = Rect(rect)
        image = Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, 
                  rects: list[tuple[float, float, 
                                    float, float]], 
                  colorkey = None
                  ) -> list[Surface]:
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, 
                   rect: tuple[float, float, 
                               float, float], 
                   image_count: int, 
                   colorkey = None
                   ) -> list[Surface]:
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)