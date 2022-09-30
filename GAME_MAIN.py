import sys
import pygame # type: ignore

from base_camera import Camera
from base_engine import Engine
from base_labels import DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP, Label
from base_level import Level, LevelForm
from base_sprite_animator import SpriteAnimator
from controls import ControlInput, ControlPreset, Controller
from screen import on_screen, position_to_screen
from tile_drawing import draw_tile_layer
from traits import TILE_COLLISION, is_tile_collision_able
from draw_tests import draw_entity_hitbox, draw_tile_outlines

print("\n\n")


#initialising pygame
pygame.init()



# defining game window
window = pygame.display.set_mode((675, 495))
pygame.display.set_caption("Hmmm")





FPS = 30

scale = 4.5





# PUT IN JSON!!!

LEVEL_1 = Label("Level-1")

FOREGROUND = Label("foreground")
BACKGROUND = Label("background")






game_state = {
  
  "levels": [],
  "level_index": 0,
  
  "current_frame": 0
  
}






controller = Controller(
    presets=(ControlPreset.UP_DOWN_LEFT_RIGHT,),
    key_mappings=((Label("dash"),    pygame.K_d),)
)






class Level_1(Level):
    
    label = LEVEL_1
    
    def __init__(self):
        super().__init__(Level_1.label)
        
        self._tile_collisions = []
    
    def update(_, form: LevelForm,
                  controller: Controller, 
                  dt: int):
        
        _._tile_collisions = []
        
        if (form.character_entity_pack is not None):
            
            # RESPOND TO INPUT
            for entity in form.character_entity_pack.entities.values():
                entity.respond_to_input(controller, dt)
            
            # UPDATE
            for entity in form.character_entity_pack.entities.values():
                entity.update(dt)
            
            # CHECK TILE COLLISION
            if (form.collision_observer and
                form.map_form and
                form.tile_pack_form):
                
                for entity in form.character_entity_pack.entities.values():
                
                    if (is_tile_collision_able(entity) and
                        entity[TILE_COLLISION].able == True):
                        
                        (new_form, collisions) = form.collision_observer.check_collision(
                            entity,
                            form.map_form.collision_map,
                            form.map_form.tile_width
                        )
                        
                        entity.pose = new_form["pose"]
                        entity.delta = new_form["delta"]
                        
                        
                        # TESTING
                        if (entity is form.player):
                            _._tile_collisions = collisions
                        
                        
                        tiles: list[tuple[tuple[Label, Label], ...]] = []
                        
                        for tile_info in collisions:
                            
                            labels: list[tuple[Label, Label]] = []
                            
                            for tile_map in form.map_form.tile_maps.values():
                                tile_pack = form.tile_pack_form[tile_map.label]
                                tile = tile_pack[tile_map[tile_info.row][tile_info.column]]
                                
                                if (tile is not None):
                                    labels.append((tile.label, tile_pack.label))
                            
                            tiles.append(tuple(labels))
                            
                        entity.handle_collision(tuple(collisions), tuple(tiles))

            
        # if (controller.get_key_state(Label("dash"), ControlInput.DOWN)):
        #     print("dash")
        # else:
        #     print()
        
        
        # CAMERA
        if (form.player is not None):
            form.camera.follow_entity(form.player)
    
    
    def display(_, form: LevelForm, dt: int):
        
        
        
        window.fill(pygame.Color(184, 227, 228))
        
        # if (form.map_form and
        #     form.tile_pack_form):
        #     draw_tile_layer(window,
        #                     form.camera,
        #                     form.map_form,
        #                     form.tile_pack_form,
        #                     BACKGROUND)
        # if (form.map_form and
        #     form.tile_pack_form):
        #     draw_tile_layer(window,
        #                     form.camera,
        #                     form.map_form,
        #                     form.tile_pack_form,
        #                     FOREGROUND)
        
        # DRAW ENTITIES
        if (form.character_entity_pack is not None):
            
            for entity in form.character_entity_pack.entities.values():
                
                if (entity.animation_pack):
                    animation = entity.animation_pack.current_animation()
                    
                    next(animation) # progress animation
                    
                    # entity is on screen
                    if (on_screen(form.camera, 
                                  pose=(entity.pose + animation.offset), 
                                  size=animation.size)):

                        window.blit(animation.image(), 
                                         position_to_screen(form.camera, 
                                                            entity.pose + animation.offset))
        
        
        # TESTING
        
        # if (form.player is not None):
        #     draw_entity_hitbox(window, 
        #                        form.player, 
        #                        form.camera, 
        #                        pygame.Color("purple"))
        if (form.map_form and
            form.tile_pack_form):
            draw_tile_outlines(window, 
                               _._tile_collisions, 
                               form.camera,
                               form.map_form, 
                               pygame.Color("red"))
        
    
    
    def setup(self, *args, **kwargs):
        self.form.load(*args, **kwargs)
        self.paused = False
        
        




level_1 = Level_1()




level_1.setup(scale, 
              FPS)






def update(controller: Controller, dt: int):
    
    controller.update(pygame.key.get_pressed())
    
    level_1.update(level_1.form, controller, dt)
    
    


def display(dt: int):
    level_1.display(level_1.form, dt)







engine = Engine(FPS)





engine.set_update_funct(update)
engine.set_display_funct(display)

engine.start(controller)



print("\n\n")
pygame.quit()
sys.exit()






