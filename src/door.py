import pygame as p 
from tile import * 

class Door(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A container', id='container', walkable=True): 
        super().__init__(sprite, pos, tile_size, name, id, walkable) 
        self.open = False 
        self.blocks_sight = False if self.open else True 
        self.closed_sprite = sprite[1] 
        self.open_sprite = sprite[2] 

    def update(self, SCREEN_OFFSET): 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
        self.blocks_sight = False if self.open else True 

    def render(self, screen): 
        if self.open: 
            screen.blit(self.sprite[0], (self.pos_coordinates[0], self.pos_coordinates[1])) 
            screen.blit(self.open_sprite, (self.pos_coordinates[0], self.pos_coordinates[1])) 
        else: 
            screen.blit(self.closed_sprite, (self.pos_coordinates[0], self.pos_coordinates[1])) 