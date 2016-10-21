import pygame as p 
p.init() 

''' TODO ''' 
# Add additional stats 
# Implement support for tiles larger than 1x1 e.g. to support a fully grown tree that's 1x2 or a dragon that's 4x4 
# Consider adding pointers to surrounding tiles for movement purposes 


class Tile(): 
    """ Every object in the game, from the floor to the walls to the player to the player's equipment is a Tile object """
    def __init__(self, sprite, pos, tile_size, name='A tile', id='tile', walkable=True): 
        self.tile_size = tile_size
        self.pos_index = [pos[0], pos[1]] 
        self.pos_coordinates = 0 
        self.sprite = sprite 
        self.is_walkable = walkable 
        self.name = name 
        self.id = id 
        self.hp = 0 
        self.revealed = False 
        self.alpha = 255 
        if self.id == 'wall' or self.id == 'door' or self.id == 'enemy': 
            self.blocks_sight = True 
        else: 
            self.blocks_sight = False 
        
    def __str__(self): 
        return self.name 

    def __repr__(self): 
        return self.id 

    def update(self, SCREEN_OFFSET): 
        self.pos_coordinates = self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1] 
        
    def render(self, screen): 
        for i in self.sprite: 
            screen.blit(i, (self.pos_coordinates[0], self.pos_coordinates[1])) 