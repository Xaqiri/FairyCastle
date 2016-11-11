import pygame as p 
p.init() 

''' TODO ''' 
# Implement support for tiles larger than 1x1 e.g. to support a fully grown tree that's 1x2 or a dragon that's 4x4 
# Consider adding pointers to surrounding tiles for movement purposes 

class Tile(): 
    def __init__(self, sprite=None, ascii_tile='#', font=None, pos=(0, 0), tile_size=16, name='A tile', id='tile', walkable=True, visible_color=None, explored_color=None): 
        self.tile_size = tile_size
        self.pos_index = [pos[0], pos[1]] 
        self.pos_coordinates = 0 
        self.sprite = sprite 
        self.is_walkable = walkable 
        self.name = name 
        self.id = id 
        self.hp = 0 
        self.visible = True if self.id == 'player' else False 
        self.explored = False 
        self.alpha = 255 
        self.ascii_tile = ascii_tile 
        if self.id == 'wall' or self.id == 'door' or self.id == 'enemy' or self.ascii_tile == '#': 
            self.blocks_sight = True 
        else: 
            self.blocks_sight = False 
        self.visible_color = visible_color 
        self.explored_color = explored_color 

    def __str__(self): 
        return self.name 

    def __repr__(self): 
        return self.id 

    @property 
    def x(self): 
        return self.pos_index[0] 
    
    @property 
    def y(self): 
        return self.pos_index[1] 
        
    def update(self, SCREEN_OFFSET=0): 
        if SCREEN_OFFSET is not 0: 
            self.pos_coordinates = [self.pos_index[0]*self.tile_size+SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+SCREEN_OFFSET[1]] 
        
    def render(self, screen, font=None, mode=0): 
        if self.sprite and mode == 0: 
            if self.visible: 
                screen.blit(self.sprite, (self.pos_coordinates[0], self.pos_coordinates[1])) 
            else: 
                #p.draw.rect(screen, self.explored_color, (self.pos_coordinates[0], self.pos_coordinates[1], self.tile_size, self.tile_size)) 
                self.sprite.set_alpha(int(self.alpha/4)) 
                screen.blit(self.sprite, (self.pos_coordinates[0], self.pos_coordinates[1])) 
                self.sprite.set_alpha(self.alpha)
        else: 
            if self.visible: 
                #p.draw.rect(screen, self.explored_color, (self.pos_coordinates[0], self.pos_coordinates[1], self.tile_size, self.tile_size)) 
                screen.blit(font.render(self.ascii_tile, 1, self.visible_color), self.pos_coordinates) 
            else: 
                #p.draw.rect(screen, self.explored_color, (self.pos_coordinates[0], self.pos_coordinates[1], self.tile_size, self.tile_size)) 
                screen.blit(font.render(self.ascii_tile, 1, self.explored_color), self.pos_coordinates) 