class Entity(): 
    def __init__(self, x=0, y=0, tile_size=16, sprites=None, ascii_tile='@', 
                    color=None, is_walkable=False, name='entity', always_visible=False, combat_component=None, font=None): 
        self.x = x 
        self.y = y 
        self.tile_size = tile_size 
        self.pos_coordinates = 0
        self.sprites = sprites 
        self.ascii_tile = ascii_tile 
        self.font = font 
        self.color = color 
        self.is_walkable = is_walkable 
        self.name = name 
        self.always_visible = always_visible 
        self.visible = False 
        self.combat_component = combat_component 
        if self.combat_component: 
            self.combat_component.parent = self 
    
    def move(self, dx, dy): 
        self.x += dx 
        self.y += dy 

    def update(self, screen_offset=0): 
        if self.name is not 'player': 
            self.pos_coordinates = [self.x*self.tile_size+screen_offset[0], self.y*self.tile_size+screen_offset[1]] 

    def render(self, screen, mode=0): 
        if self.visible: 
            if self.sprites and mode == 0: 
                for i in self.sprites: 
                    screen.blit(i, self.pos_coordinates) 
            else: 
                screen.blit(self.font.render(self.ascii_tile, 1, self.color), self.pos_coordinates) 