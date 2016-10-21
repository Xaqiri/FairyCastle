import pygame as p 
import random 
from player import * 

p.init() 

''' TODO ''' 
# Add combat method once appropriate stats are added to Tile class 

class Goblin(Player): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=False): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 8 
        self.mp = 0 
        self.melee = 1 
        self.name = 'A goblin' 
        self.id = 'enemy' 
        self.is_walkable = False 
        self.alive = True 
        self.effects = [] 
        self.count = 0 
        self.enemy_id = ['player', 'skeleton'] 
        self.revealed = False 
        self.crit_chance = 10 
        self.speed = 40 
        
    def update(self, SCREEN_OFFSET, level, dir): 
        self.alive = False if (self.hp <= 0) else True 
        self.surr_game_tiles = [ 
            level.game_board[self.pos_index[0]][self.pos_index[1]-1], 
            level.game_board[self.pos_index[0]][self.pos_index[1]+1], 
            level.game_board[self.pos_index[0]-1][self.pos_index[1]], 
            level.game_board[self.pos_index[0]+1][self.pos_index[1]]
            ] 
        self.surr_actor_tiles = [ 
            level.actor_board[self.pos_index[0]][self.pos_index[1]-1], 
            level.actor_board[self.pos_index[0]][self.pos_index[1]+1], 
            level.actor_board[self.pos_index[0]-1][self.pos_index[1]], 
            level.actor_board[self.pos_index[0]+1][self.pos_index[1]]
            ] 
        d = random.choice(dir) 
        if self.wait > 0: 
             self.wait -= 1 
        else: 
            if self.can_move(level, d): 
                self.move(d) 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
        loc = level.game_board[self.pos_index[0]][self.pos_index[1]] 
        if loc.id == 'door': 
            if not loc.open: 
                loc.open = True 
        
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