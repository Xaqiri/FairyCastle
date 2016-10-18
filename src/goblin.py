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
        self.effects = [] 
        self.count = 0 

    def update(self, SCREEN_OFFSET): 
        self.alive = False if (self.hp <= 0) else True 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
    
    def render(self, screen): 
        for i in self.sprite: 
            screen.blit(i, (self.pos_coordinates[0], self.pos_coordinates[1])) 
        if len(self.effects) > 0: 
            self.count += 1 
            screen.blit(self.effects[0], (self.pos_coordinates[0], self.pos_coordinates[1])) 
            if self.count >= 30: 
                self.effects.pop() 
                self.count = 0 
        if self.count >= 30: 
            self.count = 0 