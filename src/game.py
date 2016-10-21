import pygame as p 
import sys 
import os 
from time import * 

from tile import * 
from ui import * 
from player import * 
from goblin import * 
from spriteLoader import * 
from levelLoader import * 

p.init() 
# Version #.  Release.mainBranch.testBranch 
VER =           '0.10.18' 
p.display.set_caption('Fairy Castle' + ',    version:  ' + VER) 

''' TODO ''' 
# Add comments 
# Make code cleaner 
# Reconsider having game_board and actor_board be separate 
# Add heartbeat code 
# Add the ability for tiles to remember if they've been revealed by the player already seeing them. 
# Revealed tiles would show up darker than tiles currently in the player's los 
# Or possibly have tiles fade out after they leave the player's fov 
# e.g. a tile's visible to the player.  They move one tile to the right, so the tiles that are now outside of the player's fov fade out over two seconds or so 

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
                                                    'actorSpriteSheet13x6.png')).convert(), 
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
                                    16, 1, 13, 6).sprites 
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
ui = UI(window_size, (level.board_width, level.board_height), 24, TILE_DIMENSION, SCREEN_OFFSET, sprites['cursor']) 

states = ['game', 'lose', 'win'] 
state = states[0] 

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
    if level.player.wait > 0: 
        level.player.wait -= 1 
        return 
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
                if level.actor_board[ui.mouse_index[0]][ui.mouse_index[1]].id in level.player.enemy_id and level.actor_board[ui.mouse_index[0]][ui.mouse_index[1]].revealed: 
                    level.player.ranged_attack(level.actor_board[ui.mouse_index[0]][ui.mouse_index[1]], level) 
            except: 
                pass 
            #if e.key == p.K_SPACE: 
            #    direction = 'reload' 
    return direction 

def update(direction, clock): 
    global state 
    dir = ['up', 'down', 'left', 'right'] 
    if state == states[0]: 
        ui.update(clock, SCREEN_OFFSET, level.game_board) 
        if direction in dir and level.player.can_move(level, direction): 
            level.actor_board[level.player.pos_index[0]][level.player.pos_index[1]] = 0 
            level.player.move(direction) 
            level.actor_board[level.player.pos_index[0]][level.player.pos_index[1]] = level.player 
            move_board(direction) 
        level.player.update(SCREEN_OFFSET, level) 
        for i in level.player.fov.visible_tiles: 
            try: 
                i.update(SCREEN_OFFSET) 
            except: 
                pass 
        for e in level.enemies: 
            level.actor_board[e.pos_index[0]][e.pos_index[1]] = 0 
            e.update(SCREEN_OFFSET, level, dir) 
            level.actor_board[e.pos_index[0]][e.pos_index[1]] = e 
            if not e.alive: 
                level.actor_board[e.pos_index[0]][e.pos_index[1]] = 0 
                level.enemies.remove(e) 
                
        if not level.player.alive: 
            state = states[1] 
        if len(level.enemies) <= 0: 
            state = states[2] 

def render(): 
    global state 
    screen.fill(GRAY) 
    if state == states[0]: 
        ui.render(screen, GREEN, level) 
        level.render(screen, level.player, TILE_DIMENSION, SCREEN_OFFSET, ui) 
    elif state == states[1]: 
        screen.blit(ui.font.render("Game Over", 1, GREEN), (window_width//2, window_height//2)) 
    elif state == states[2]: 
        screen.blit(ui.font.render("You win", 1, GREEN), (window_width//2, window_height//2)) 
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