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
        self.is_walkable = False 
        self.vision_range = 5 
        self.fov = fov.FOV(game_board, actor_board) 
        self.revealed = True 
        self.crit_chance = 4 
        self.inventory = dict() 
        self.enemy_id = ['enemy', 'skeleton'] 
        self.surr_game_tiles = [] 
        self.surr_actor_tiles = [] 
        self.speed = 10 
        self.attack_speed = 20 
        self.cast_speed = 40 
        self.wait = 0 
        
        self.melee = 1 
        self.archery = 1 
        self.magic = 1 
        self.runecrafting = 1 
        
        self.mining = 1 
        self.smithing = 1 
        self.woodcutting = 1 
        self.farming = 1 
        self.fletching = 1 
    
    def can_move(self, level, direction): 
        if direction == 'up': 
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
        
        
    def attack(self, enemy): 
        crit_roll = random.randint(1, 10) 
        if crit_roll > self.crit_chance: 
            enemy.hp -= self.melee * 2 
        else: 
            enemy.hp -= self.melee 
        self.wait = self.attack_speed 

    def ranged_attack(self, enemy, level): 
        if self.mp > 0: 
            enemy.hp -= self.magic * 4 
            enemy.effects.append(level.itemSprites[2][4])
            self.mp -= 1 
            self.wait = self.cast_speed 

    def heal(self): 
        if 'hp_potion' in self.inventory: 
            if self.hp < self.max_hp: 
                self.hp += 4 
                if self.hp > self.max_hp: 
                    self.hp = self.max_hp 
                self.inventory['hp_potion'] -= 1 

    def update(self, SCREEN_OFFSET, level): 
        self.alive = False if (self.hp <= 0) else True 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
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
        loc = level.game_board[self.pos_index[0]][self.pos_index[1]] 
        if loc.id == 'weapon': 
            loc.id = 'floor' 
            loc.sprite.pop() 
            self.sprite.append(level.itemSprites[4][3]) 
            if 'weapon' in self.inventory: 
                self.inventory['weapon'] += 1 
            else: 
                self.inventory['weapon'] = 1 
            self.melee += 2 
        if loc.id == 'hp_potion': 
            loc.id = 'floor' 
            loc.sprite.pop() 
            if 'hp_potion' in self.inventory: 
                self.inventory['hp_potion'] += 1 
            else: 
                self.inventory['hp_potion'] = 1 
        if loc.id == 'barrel': 
            if loc.charges > 0: 
                loc.charges -= 1 
                self.mp += 8 
        if loc.id == 'crate': 
            if loc.charges > 0: 
                loc.charges -= 1 
                if 'hp_potion' in self.inventory: 
                    self.inventory['hp_potion'] += 2 
                else: 
                    self.inventory['hp_potion'] = 2 
        if loc.id == 'door': 
            if not loc.open: 
                loc.open = True 
        self.fov.update(self.pos_index, self.vision_range) 