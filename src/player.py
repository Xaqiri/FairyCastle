import pygame as p 
import random 
from tile import * 
import fov 

p.init() 

''' TODO ''' 
# Add combat method once appropriate stats are added to Tile class 
# Use distance formula for enemy ai i.e. once the player's within a certain range of the enemy, the enemy starts moving toward the player 
# can_move should be here rather than in game.py.  This will allow enemies to move without a lot of extra code 


class Player(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=False): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 1 
        self.id = 'player' 
        self.job = 'peasant' 
        self.name = 'A {0}'.format(self.job) 
        self.alive = True if (self.hp > 0) else False 
        self.is_walkable = False 
        self.vision_range = 5 
        self.revealed = True 
        self.inventory = dict() 
        
    def can_move(self, level, direction): 
        '''if direction == 'up': 
            if type(self.surr_actor_tiles[0]) != int: 
                if self.surr_actor_tiles[0].id in self.enemy_id: 
                    self.attack(self.surr_actor_tiles[0]) 
                else: 
                    return self.surr_game_tiles[0].is_walkable and self.surr_actor_tiles[0].is_walkable 
            else: 
                return self.surr_game_tiles[0].is_walkable 
        if direction == 'down': 
            if type(self.surr_actor_tiles[1]) != int: 
                if self.surr_actor_tiles[1].id in self.enemy_id: 
                    self.attack(self.surr_actor_tiles[1])
                else: 
                    return self.surr_game_tiles[1].is_walkable and self.surr_actor_tiles[1].is_walkable 
            else: 
                return self.surr_game_tiles[1].is_walkable 
        if direction == 'left': 
            if type(self.surr_actor_tiles[2]) != int: 
                if self.surr_actor_tiles[2].id in self.enemy_id: 
                    self.attack(self.surr_actor_tiles[2]) 
                else: 
                    return self.surr_game_tiles[2].is_walkable and self.surr_actor_tiles[2].is_walkable 
            else: 
                return self.surr_game_tiles[2].is_walkable 
        if direction == 'right': 
            if type(self.surr_actor_tiles[3]) != int: 
                if self.surr_actor_tiles[3].id in self.enemy_id: 
                    self.attack(self.surr_actor_tiles[3]) 
                else: 
                    return self.surr_game_tiles[3].is_walkable and self.surr_actor_tiles[3].is_walkable 
            else: 
                return self.surr_game_tiles[3].is_walkable 
'''
    def move(self, direction): 
        if direction == 'up': 
            self.pos_index[1] -= 1  
        if direction == 'down': 
            self.pos_index[1] += 1 
        if direction == 'left': 
            self.pos_index[0] -= 1 
        if direction == 'right': 
            self.pos_index[0] += 1 
        self.wait = self.speed 
        
        
    def update(self, SCREEN_OFFSET): 
        self.alive = False if (self.hp <= 0) else True 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
        