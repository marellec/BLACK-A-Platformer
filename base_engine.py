
from typing import Callable
import pygame # type: ignore

from controls import Controller # type: ignore


class Engine:
    
    clock: pygame.time.Clock
    running: bool = False
    FPS: int = 60
    
    update_funct:  Callable[[Controller, int], None]
    display_funct: Callable[[int], None]
    
    def __init__(self, fps: int = 60):
        self.FPS = fps
        self.clock = pygame.time.Clock()
        pass
    
    def start(self, controller: Controller):
        self.running = True
        
        while (self.running):
            
            for event in pygame.event.get():
                
                if  (event.type == pygame.QUIT): 
                    self.stop()
                elif (event.type == pygame.KEYDOWN):
                    controller.press(event.key)
                    # print(event.key)
                elif (event.type == pygame.KEYUP):
                    controller.release(event.key)
                    # print(event.key)
                
                
            
            self.update_funct(controller, 1) # type: ignore
            self.display_funct(1) # type: ignore
            
            pygame.display.update()
            self.clock.tick(self.FPS)
    
    def stop(self):
        self.running = False
    
    
    def set_update_funct(self, update_funct: Callable[[Controller, int], 
                                                      None]):
        self.update_funct = update_funct # type: ignore
        
    def set_display_funct(self, display_funct: Callable[[int], 
                                                        None]):
        self.display_funct = display_funct # type: ignore