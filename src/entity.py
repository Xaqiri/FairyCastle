import math 

class Entity(): 
    def __init__(self, x=0, y=0, tile_size=16, sprites=None, ascii_tile='@', 
                    color=None, is_walkable=False, name='entity', always_visible=False, combat_component=None, 
                    ai_component=None, font=None): 
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
        self.visible = True if self.name == 'player' else False 
        self.combat_component = combat_component 
        if self.combat_component: 
            self.combat_component.parent = self 
            self.living_sprite = sprites[0] 
            self.death_sprite = sprites[1] 
        self.current_sprite = self.living_sprite if self.combat_component else self.sprites[0] 
        self.ai_component = ai_component 
        if self.ai_component: 
            self.ai_component.parent = self 
        self.level = 1 
        self.id = 'friend' if self.name is 'player' else 'enemy' 
        self.took_turn = False 
        
    def distance_to(self, other): 
        dx = other.x - self.x 
        dy = other.y - self.y 
        return math.sqrt(dx ** 2 + dy ** 2) 

    def distance(self, x, y): 
        return math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2) 

    def move_towards(self, target_x, target_y, map, objects): 
        dx = target_x - self.x 
        dy = target_y - self.y 
        distance = math.sqrt(dx ** 2 + dy ** 2) 
        dx = int(round(dx/distance)) 
        dy = int(round(dy/distance)) 
        self.move(dx, dy, map, objects) 

    def is_blocked(self, x, y, map, entities): 
        if not map[x][y].is_walkable: 
            return True 
        for e in entities: 
            if not e.is_walkable and e.x == x and e.y == y: 
                if e.id is not self.id: 
                    self.combat_component.attack(e, entities[0]) 
                    if self.name == 'player': 
                        self.took_turn = True 
                return True 
        return False 
        
    def move(self, dx, dy, map, entities): 
        x = self.x + dx 
        y = self.y + dy 
        if not self.is_blocked(x, y, map, entities): 
            self.x += dx 
            self.y += dy 
            if self.name == 'player': 
                self.took_turn = True 

    def heal(self, amount): 
        self.combat_component.current_hp += amount 
        if self.combat_component.current_hp > self.combat_component.max_hp: 
            self.combat_component.current_hp = self.combat_component.max_hp 

    def update(self, screen_offset=0): 
        if self.name is not 'player': 
            self.pos_coordinates = [self.x*self.tile_size+screen_offset[0], self.y*self.tile_size+screen_offset[1]] 
        if self.name == 'player': 
            if self.combat_component.xp >= 100: 
                self.level += 1 
                self.combat_component.xp -= 100 
                self.combat_component.max_hp += 10 
                self.combat_component.current_hp = self.combat_component.max_hp 
                self.combat_component.strength += 1 
                self.combat_component.defense += 1 

    def render(self, screen, mode=0): 
        if self.visible or self.always_visible: 
            if self.sprites and mode == 0: 
                screen.blit(self.current_sprite, self.pos_coordinates) 
            else: 
                try: 
                    screen.blit(self.font.render(self.ascii_tile, 1, self.color), self.pos_coordinates) 
                except: 
                    print(self.ascii_tile) 
                    pass 