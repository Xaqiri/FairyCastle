import pygame as p 
from player import * 
p.init() 

''' TODO ''' 
# Add combat method once appropriate stats are added to Tile class 

class Goblin(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=False): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 8 
        self.mp = 0 
        self.melee = 1 
        self.name = 'A goblin' 
        self.id = 'enemy' 
        self.is_walkable = walkable 
        self.alive = True 

    def update(self, SCREEN_OFFSET): 
        self.alive = False if (self.hp <= 0) else True 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 