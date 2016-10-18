import pygame as p 
from tile import * 

class Container(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A container', id='container', walkable=True): 
        super().__init__(sprite, pos, tile_size, name, id, walkable) 
        self.charges = 1 