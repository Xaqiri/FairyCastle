import pygame as p 
from goblin import * 

class Skeleton(Goblin): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=False): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 12 
        self.mp = 0 
        self.melee = 2 
        self.name = 'A spooky skellington' 
        self.id = 'skeleton' 
        self.is_walkable = False 
        self.alive = True 
        self.effects = [] 
        self.count = 0 
        self.enemy_id = ['player', 'enemy'] 
        self.revealed = False 
        self.crit_chance = 7 
        self.speed = 80 
        [i.set_alpha(100) for i in self.sprite] 