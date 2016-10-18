import pygame as p 
import sys 
import os 

from tile import * 
from ui import * 
from player import * 
from goblin import * 
from spriteLoader import * 
from levelLoader import * 

p.init() 
# Version #.  Release.mainBranch.testBranch 
VER =           '0.10.15' 
p.display.set_caption('Fairy Castle' + ',    version:  ' + VER) 

''' TODO ''' 
# Add comments 
# Make code cleaner 
# Reconsider having game_board and actor_board be separate 
# Add heartbeat code 
# Add the ability for tiles to remember if they've been revealed by the player already seeing them. 
# Revealed tiles would show up darker than tiles currently in the player's los 

''' Colors ''' 
TRANS = (128, 0, 128) 
BLACK = (0, 0, 0) 
GREEN = (0, 255, 0) 
GRAY  = (16, 16, 16) 

SCALE = 2 
TILE_DIMENSION = int(16*SCALE) 
window_size = window_width, window_height = 1280, 960 
SCREEN_CENTER = (window_width//2, window_height//2) 
screen = p.display.set_mode(window_size) 

sprites = dict(actorSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'actorSpriteSheet8x6.png')).convert(), 
                environmentSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'environmentSpriteSheet15x8.png')).convert(), 
                itemSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'itemSpriteSheet12x8.png')).convert(), 
                cursor=p.image.load(os.path.join('..', 'assets', '1', 
                                                    'cursor.png')).convert()) 
levels = dict(level_t=os.path.join('..', 'levels', 'level_1.txt')) 
# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions 
for i in sprites: 
    sprites[i].set_colorkey(TRANS) 
    
# Splits the sprite sheet into individual sprites 
actor_sprite_sheet = SpriteLoader(sprites['actorSheet'], TILE_DIMENSION, (0, 0), 
                                    16, 1, 8, 6).sprites 
environment_sprite_sheet = SpriteLoader(sprites['environmentSheet'], TILE_DIMENSION, (0, 0), 
                                    16, 1, 15, 8).sprites 
item_sprite_sheet = SpriteLoader(sprites['itemSheet'], TILE_DIMENSION, (0, 0), 
                                    16, 1, 12, 8).sprites 

level = LevelLoader(levels['level_t'], window_size, actor_sprite_sheet, environment_sprite_sheet, 
                    item_sprite_sheet) 
level.load(TILE_DIMENSION) 

# Subtracting 4*TILE_DIMENSION to move the player to the center of the playable window rather than the entire window.  Don't know where the 32 comes from 
# Offsets the game board by a certain amount 
SCREEN_OFFSET = [SCREEN_CENTER[0]-level.player.pos_index[0]*TILE_DIMENSION-4*TILE_DIMENSION+32, SCREEN_CENTER[1]-level.player.pos_index[1]*TILE_DIMENSION] 
level.player.pos_coordinates = SCREEN_OFFSET 
ui = UI(window_size, (level.board_width, level.board_height), 32, TILE_DIMENSION, SCREEN_OFFSET, sprites['cursor']) 

# Should be moved to player class 
def can_move(tile, direction): 
    # Need to rework this function to handle movement checking more elegantly 
    game_up = level.game_board[tile.pos_index[0]][tile.pos_index[1] - 1] 
    game_down = level.game_board[tile.pos_index[0]][tile.pos_index[1] + 1] 
    game_left = level.game_board[tile.pos_index[0] - 1][tile.pos_index[1]] 
    game_right = level.game_board[tile.pos_index[0] + 1][tile.pos_index[1]] 
    act_up = level.actor_board[tile.pos_index[0]][tile.pos_index[1] - 1] 
    act_down = level.actor_board[tile.pos_index[0]][tile.pos_index[1] + 1] 
    act_left = level.actor_board[tile.pos_index[0] - 1][tile.pos_index[1]] 
    act_right = level.actor_board[tile.pos_index[0] + 1][tile.pos_index[1]] 
    if direction == 'up': 
        if type(act_up) != int: 
            if act_up.id == 'enemy': 
                level.player.attack(act_up) 
            else: 
                return game_up.is_walkable and act_up.is_walkable 
        else: 
            return game_up.is_walkable 
    if direction == 'down': 
        if type(act_down) != int: 
            if act_down.id == 'enemy': 
                level.player.attack(act_down)
            else: 
                return game_down.is_walkable and act_down.is_walkable 
        else: 
            return game_down.is_walkable 
    if direction == 'left': 
        if type(act_left) != int: 
            if act_left.id == 'enemy': 
                level.player.attack(act_left) 
            else: 
                return game_left.is_walkable and act_left.is_walkable 
        else: 
            return game_left.is_walkable 
    if direction == 'right': 
        if type(act_right) != int: 
            if act_right.id == 'enemy': 
                level.player.attack(act_right) 
            else: 
                return game_right.is_walkable and act_right.is_walkable 
        else: 
            return game_right.is_walkable 
    
def move_board(direction): 
    global SCREEN_OFFSET 
    if  direction == 'up': 
        SCREEN_OFFSET[1] += TILE_DIMENSION 
    if  direction == 'down': 
        SCREEN_OFFSET[1] -= TILE_DIMENSION
    if  direction == 'left': 
        SCREEN_OFFSET[0] += TILE_DIMENSION
    if  direction == 'right': 
        SCREEN_OFFSET[0] -= TILE_DIMENSION 
    
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
            if e.key == p.K_DOWN: 
                direction = 'down' 
            if e.key == p.K_LEFT: 
                direction = 'left' 
            if e.key == p.K_RIGHT: 
                direction = 'right' 
            if e.key == p.K_q: 
                level.player.heal() 
        if e.type == p.MOUSEBUTTONDOWN: 
            try: 
                if level.actor_board[ui.mouse_index[0]][ui.mouse_index[1]].id == 'enemy': 
                    level.player.ranged_attack(level.actor_board[ui.mouse_index[0]][ui.mouse_index[1]], level) 
            except: 
                pass 
            #if e.key == p.K_SPACE: 
            #    direction = 'reload' 
    return direction 

def update(direction, clock): 
    ui.update(clock, SCREEN_OFFSET, level.game_board) 
    if direction in ['up', 'down', 'left', 'right'] and can_move(level.player, direction): 
        level.actor_board[level.player.pos_index[0]][level.player.pos_index[1]] = 0 
        level.player.move(direction) 
        move_board(direction) 
        level.actor_board[level.player.pos_index[0]][level.player.pos_index[1]] = level.player 
    for e in level.enemies: 
        if not e.alive: 
            level.actor_board[e.pos_index[0]][e.pos_index[1]] = 0 
            level.enemies.remove(e) 
    if not level.player.alive: 
        print("You lose") 
        sys.exit() 
    if len(level.enemies) <= 0: 
        print("You win") 
        sys.exit() 

def render(): 
    screen.fill(GRAY) 
    ui.render(screen, GREEN, level) 
    level.render(screen, level.player, TILE_DIMENSION, SCREEN_OFFSET, ui) 
    p.display.flip() 
    
clock = p.time.Clock() 
done = False 
while not done: 
    direction = input() 
    if direction == 'reload': 
        reload_level() 
    else: 
        update(direction, clock) 
    render() 
    clock.tick(60) 

p.quit()    