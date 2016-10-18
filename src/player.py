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
    def __init__(self, sprite, pos, tile_size, game_board, actor_board, name='A tile', walkable=False): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.max_hp = 8 
        self.hp = 8 
        self.mp = 2 
        self.lives = 1 
        self.id = 'player' 
        self.job = 'peasant' 
        self.name = 'A {0}'.format(self.job) 
        self.alive = True if (self.hp > 0) else False 
        self.is_walkable = walkable if not self.alive else False 
        self.vision_range = 5 
        self.fov = fov.FOV(game_board, actor_board) 
        self.revealed = True 
        self.crit_chance = 4 
        self.inventory = dict() 

        self.melee = 1 
        self.archery = 1 
        self.magic = 1 
        self.runecrafting = 1 
        
        self.mining = 1 
        self.smithing = 1 
        self.woodcutting = 1 
        self.farming = 1 
        self.fletching = 1 
        
    def move(self, direction): 
        if direction == 'up': 
            self.pos_index[1] -= 1  
        if direction == 'down': 
            self.pos_index[1] += 1 
        if direction == 'left': 
            self.pos_index[0] -= 1 
        if direction == 'right': 
            self.pos_index[0] += 1 
        
    def attack(self, enemy): 
        crit_roll = random.randint(1, 10) 
        if crit_roll > self.crit_chance: 
            enemy.hp -= self.melee * 2 
        else: 
            enemy.hp -= self.melee 
        self.hp -= enemy.melee 
    
    def heal(self): 
        if 'hp_potion' in self.inventory: 
            if self.hp < self.max_hp: 
                self.hp += 4 
                if self.hp > self.max_hp: 
                    self.hp = self.max_hp 
                self.inventory['hp_potion'] -= 1 

    def update(self, SCREEN_OFFSET, game_board): 
        self.alive = False if (self.hp <= 0) else True 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
        if game_board[self.pos_index[0]][self.pos_index[1]].id == 'weapon': 
            game_board[self.pos_index[0]][self.pos_index[1]].id = 'floor' 
            game_board[self.pos_index[0]][self.pos_index[1]].sprite.pop() 
            if 'weapon' in self.inventory: 
                self.inventory['weapon'] += 1 
            else: 
                self.inventory['weapon'] = 1 
            self.melee += 2 
        if game_board[self.pos_index[0]][self.pos_index[1]].id == 'hp_potion': 
            game_board[self.pos_index[0]][self.pos_index[1]].id = 'floor' 
            game_board[self.pos_index[0]][self.pos_index[1]].sprite.pop() 
            if 'hp_potion' in self.inventory: 
                self.inventory['hp_potion'] += 1 
            else: 
                self.inventory['hp_potion'] = 1 
        self.fov.update(self.pos_index, self.vision_range) 