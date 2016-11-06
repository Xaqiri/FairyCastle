import pygame as p 
import random 
import sys 
import os 
from time import * 

import pyRL 
from ui import * 
from tile import * 
from entity import * 
from combat_component import * 

p.init() 
# Version #.  Release.mainBranch.testBranch 
VER =           '0.10.18' 
p.display.set_caption('Fairy Castle' + ',    version:  ' + VER) 

''' TODO ''' 
# Fix phantom wall bug:  Some times the player can walk through tiles that are displayed as walls, and can't walk through tiles displayed as floors 
# Add comments 
# Make code cleaner 
# Make tiles outside of the player's fov more interesting, possibly have tiles fade out after they leave the player's fov 
# e.g. a tile's visible to the player.  They move one tile to the right, so the tiles that are now outside of the player's fov fade out over two seconds or so 

''' Colors ''' 
TRANS = (128, 0, 128) 
BLACK = pyRL.colors.Colors.BLACK 
GREEN = pyRL.colors.Colors.GREEN 
GRAY  = pyRL.colors.Colors.DRKR_GRAY 

SCALE = 2 
TILE_DIMENSION = int(16*SCALE) 
window_size = window_width, window_height = 1200, 700 
SCREEN_CENTER = (window_width//2, window_height//2) 
screen = p.display.set_mode(window_size) 
game_panel = pyRL.panel.Panel(0, 0, window_width, window_height-100, pyRL.colors.Colors.BLACK, screen) 
message_panel = pyRL.panel.Panel(0, game_panel.height, window_width, window_height-game_panel.height, pyRL.colors.Colors.GRAY, screen) 
panels = [game_panel, message_panel] 
font_size = TILE_DIMENSION 
font = p.font.SysFont('comicsans', font_size) 
        
sprites = dict(actorSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'actorSpriteSheet13x6.png')).convert(), 
                environmentSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'environmentSpriteSheet15x8.png')).convert(), 
                itemSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'itemSpriteSheet12x8.png')).convert(), 
                cursor=p.image.load(os.path.join('..', 'assets', '1', 
                                                    'cursor.png')).convert()) 

# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions 
for i in sprites: 
    sprites[i].set_colorkey(TRANS) 
    
# Splits the sprite sheet into individual sprites 
actor_sprite_sheet = pyRL.sprite_loader.SpriteLoader(sprites['actorSheet'], TILE_DIMENSION, (0, 0), 
                                    16, 1, 13, 6).sprites 
environment_sprite_sheet = pyRL.sprite_loader.SpriteLoader(sprites['environmentSheet'], TILE_DIMENSION, (0, 0), 
                                    16, 1, 15, 8).sprites 
item_sprite_sheet = pyRL.sprite_loader.SpriteLoader(sprites['itemSheet'], TILE_DIMENSION, (0, 0), 
                                    16, 1, 12, 8).sprites 

combat_component = CombatComponent() 
player = Entity(x=1, y=1, sprites=[actor_sprite_sheet[0][0]], tile_size=TILE_DIMENSION, name='player', color=pyRL.colors.Colors.DRK_BLUE, combat_component=combat_component, font=font) 
entities = [player] 
#ui = UI(window_size, (level.board_width, level.board_height), 24, TILE_DIMENSION, screen_offset, sprites['cursor']) 
level = pyRL.random_level_gen.RandomLevelGen(room_min_size=10, room_max_size=10, max_rooms=400, level_width=100, level_height=100, tile_size=TILE_DIMENSION, sprites=[environment_sprite_sheet[1][6], environment_sprite_sheet[4][6]]) 
player.x, player.y = level.make_level(entities=entities) 
screen_offset = [game_panel.center[0]-player.x*TILE_DIMENSION, game_panel.center[1]-player.y*TILE_DIMENSION] 
#player.x, player.y = screen_offset 
player.pos_coordinates = [player.x*player.tile_size+screen_offset[0], player.y*player.tile_size+screen_offset[1]] 
player.visible = True 
    
states = ['game', 'lose', 'win'] 
state = states[0] 
fov = pyRL.fov.FOV() 

def in_bounds(tile): 
    if type(tile.pos_coordinates) == int: 
        return False 
    if (tile.pos_coordinates[0] > -TILE_DIMENSION and tile.pos_coordinates[0] < game_panel.width+TILE_DIMENSION and
        tile.pos_coordinates[1] > -TILE_DIMENSION and tile.pos_coordinates[1] < game_panel.height+TILE_DIMENSION): 
        return True 
    else: 
        return False 

def is_blocked(tile): 
    if not tile.is_walkable: 
        return True 
    else: 
        return False 

def place_objects(room, entities): 
    num_monsters = 1 
    for i in range(num_monsters): 
        x = random.randint(room.x1, room.x2) 
        y = random.randint(room.y1, room.y2) 
        combat_component = CombatComponent() 
        monster = Entity(x, y, TILE_DIMENSION, [actor_sprite_sheet[1][0]], 'g', pyRL.colors.Colors.DRK_GREEN, False, 'goblin', False, combat_component, font) 
        if not is_blocked(level.level[x][y]): 
            entities.append(monster) 

def can_move(entity, direction): 
    global fov_recompute 
    if  direction == 'up': 
        if level.level[entity.x][entity.y-1].is_walkable: 
            fov_recompute = True 
            return True 
        else: 
            return False 
    elif  direction == 'down': 
        if level.level[entity.x][entity.y+1].is_walkable: 
            fov_recompute = True 
            return True 
        else: 
            return False 
    elif  direction == 'left': 
        if level.level[entity.x-1][entity.y].is_walkable: 
            fov_recompute = True 
            return True 
        else: 
            return False 
    elif  direction == 'right': 
        if level.level[entity.x+1][entity.y].is_walkable: 
            fov_recompute = True 
            return True 
        else: 
            return False 
     
def move_board(direction): 
    global screen_offset 
    if  direction == 'up': 
        screen_offset[1] += TILE_DIMENSION 
    if  direction == 'down': 
        screen_offset[1] -= TILE_DIMENSION
    if  direction == 'left': 
        screen_offset[0] += TILE_DIMENSION
    if  direction == 'right': 
        screen_offset[0] -= TILE_DIMENSION 
    
def input(): 
    direction = '' 
    p.event.pump() 
    for e in p.event.get(): 
        if e.type == p.QUIT: 
            sys.exit() 
        if e.type == p.KEYDOWN: 
            if e.key == p.K_ESCAPE: 
                sys.exit() 
            if e.key == p.K_UP: 
                direction = 'up' 
                if can_move(player, direction): 
                    player.move(0, -1) 
                else: 
                    direction = ' ' 
            if e.key == p.K_DOWN: 
                direction = 'down' 
                if can_move(player, direction): 
                    player.move(0, 1) 
                else: 
                    direction = ' ' 
            if e.key == p.K_LEFT: 
                direction = 'left' 
                if can_move(player, direction): 
                    player.move(-1, 0) 
                else: 
                    direction = ' ' 
            if e.key == p.K_RIGHT: 
                direction = 'right' 
                if can_move(player, direction): 
                    player.move(1, 0) 
                else: 
                    direction = ' ' 
    if direction is not '': 
        move_board(direction) 
    return direction 

def update(direction, clock): 
    global state, mouse_pos, fps_counter, screen_offset, fov_recompute 
    dir = ['up', 'down', 'left', 'right'] 
    if fov_recompute: 
        fov_recompute = False 
        fov.update(entities=entities, vision_range=8, level=level.level) 
        for ex in fov.explored_tiles: 
            ex.update(screen_offset) 
    for e in entities: 
        e.visible = level.level[e.x][e.y].visible 
        e.update(screen_offset) 
    mouse_pos = p.mouse.get_pos() 
    fps_counter = clock.get_fps() 

def render(): 
    global state 
    screen.fill(GRAY) 
    game_panel.render() 
    for v in fov.visible_tiles: 
        if in_bounds(v): 
            v.render(screen, 1) 
    for ex in fov.explored_tiles: 
        if in_bounds(ex) and not ex.visible: 
            ex.render(screen, 1) 
    for e in entities: 
        if e is not player: 
            e.render(screen, 1) 
    player.render(screen, 1) 
    message_panel.render() 
    screen.blit(font.render(str((mouse_pos[0], mouse_pos[1])), 1, pyRL.colors.Colors.GREEN), (message_panel.width-100, message_panel.top_y+10)) 
    screen.blit(font.render(str(('{:.2f}'.format(fps_counter))), 1, pyRL.colors.Colors.GREEN), (message_panel.width-50, message_panel.top_y+50)) 
    p.display.flip() 
    
for r in level.rooms: 
    place_objects(r, entities) 

clock = p.time.Clock() 
done = False 
mouse_pos = p.mouse.get_pos() 
fps_counter = clock.get_fps() 
fov_recompute = True 
while not done: 
    direction = input() 
    update(direction, clock) 
    render() 
    clock.tick(60) 

p.quit()    