import pygame as p 
from tile import * 

class Container(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A container', id='container', walkable=True): 
        super().__init__(sprite, pos, tile_size, name, id, walkable) 
        self.charges = 1 
        self.full_sprite = sprite[0] 
        self.closed_sprite = sprite[1] 

    def render(self, screen): 
        screen.blit(self.sprite[0], (self.pos_coordinates[0], self.pos_coordinates[1])) 
        if self.charges >= 1: 
            screen.blit(self.sprite[1], (self.pos_coordinates[0], self.pos_coordinates[1])) 
        else: 
            screen.blit(self.sprite[2], (self.pos_coordinates[0], self.pos_coordinates[1])) 