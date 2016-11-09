import pygame as p 
import random 
import sys 
import os 
from time import * 

import pyRL 
import random_level_gen 
from ui import * 
from tile import * 
from entity import * 
from combat_component import * 
from basic_ai import * 

p.init() 
# Version #.  Release.mainBranch.testBranch 
VER =           '0.10.19' 
p.display.set_caption('Fairy Castle' + ',    version:  ' + VER) 

''' TODO ''' 
# Fix phantom wall bug:  Some times the player can walk through tiles that are displayed as walls, and can't walk through tiles displayed as floors 
# After moving around the level for a while, the game things the player is one tile further to the right than they actually are 
# i.e. start the dungeon at (7, 34), going (floor, player, floor, wall).  After walking around for a while and returning to the start position, 
# the player at (7, 34) will be one to the left, (player, floor, floor, wall), and will not be able to move to the right 
# Not limited to the x direction 
# Bug doesn't seem to be caused by the screen_offset (returning to the start position after the bug sets in displays the same screen_offset the game started with) 

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
game_panel = pyRL.panel.Panel(0, 0, window_width, window_height-100, pyRL.colors.Colors.DRKR_GRAY, screen, True) 
message_panel = pyRL.panel.Panel(0, game_panel.height, window_width, window_height-game_panel.height, pyRL.colors.Colors.DRK_GRAY, screen, True) 
character_sheet_panel = pyRL.panel.Panel(0, 0, game_panel.width/3, game_panel.height, pyRL.colors.Colors.DRK_GREEN, screen) 
base_panels = [game_panel, message_panel] 
temp_panels = [character_sheet_panel] 
font_size = 16 
fonts = ['palatino', 'consolas', 'courier', 'terminal']
ui_font = p.font.SysFont('consolas', font_size) 
game_font = p.font.SysFont('terminal', 48) 
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

combat_component = CombatComponent(strength=40, defense=10) 
player = Entity(x=1, y=1, sprites=[actor_sprite_sheet[0][0]], tile_size=TILE_DIMENSION, name='player', color=pyRL.colors.Colors.CYAN, combat_component=combat_component, font=game_font) 
entities = [player] 
level = random_level_gen.RandomLevelGen(room_min_size=2, room_max_size=5, max_rooms=50, level_width=10, level_height=10, tile_size=TILE_DIMENSION, sprites=[environment_sprite_sheet[1][6], environment_sprite_sheet[4][6]], level_font=game_font) 
level.make_level(entities) 
screen_offset = [game_panel.center[0]-player.x*TILE_DIMENSION, game_panel.center[1]-player.y*TILE_DIMENSION] 
player.pos_coordinates = [player.x*player.tile_size+screen_offset[0], player.y*player.tile_size+screen_offset[1]] 
#ui = UI(message_panel.size, (level.level.level_width, level.level.level_height), 24, TILE_DIMENSION, screen_offset, sprites['cursor']) 
player.took_turn = True 

look_mode = False 
dungeon_level = 1 
states = ['game', 'lose', 'win'] 
state = states[0] 

def init_fov(): 
    global fov_recompute, fov 
    fov_recompute = True 
    fov.visible_tiles = [] 
    fov.explored_tiles = [] 
    fov_recompute = False 
    
def next_level(): 
    global entities, level, screen_offset, dungeon_level 
    entities = [player] 
    level = random_level_gen.RandomLevelGen(room_min_size=2, room_max_size=8, max_rooms=50, level_width=32, level_height=32, tile_size=TILE_DIMENSION, sprites=[environment_sprite_sheet[1][6], environment_sprite_sheet[4][6]], level_font=game_font) 
    level.make_level(entities) 
    screen_offset = [game_panel.center[0]-player.x*TILE_DIMENSION, game_panel.center[1]-player.y*TILE_DIMENSION] 
    player.pos_coordinates = [player.x*player.tile_size+screen_offset[0], player.y*player.tile_size+screen_offset[1]] 
    for r in level.rooms: 
        place_objects(r) 
    init_fov() 
    player.took_turn = True 
    dungeon_level += 1 
    
def enemy_death(monster): 
    global entities 
    monster.ascii_tile = '%' 
    monster.color = pyRL.colors.Colors.RED 
    monster.is_walkable = True 
    monster.ai_component = None 
    monster.name = 'remains of {}'.format(monster.name) 
    
def draw_panel_info(panel, label, info, start_pos, screen): 
    y_offset = 50 
    screen.blit(ui_font.render(label, 1, pyRL.colors.Colors.WHITE), (panel.top_x, panel.top_y)) 
    for key in info.keys(): 
        screen.blit(ui_font.render('{}:  {}'.format(key, info[key]), 1, pyRL.colors.Colors.WHITE), (panel.top_x, panel.top_y+y_offset)) 
        y_offset+=50 

def render_bar(x, y, total_width, height, name, value, maximum, bar_color, back_color): 
    ''' Generic function for rendering ui bars for e.g. hp, mp, xp''' 
    bar_width = int(float(value) / maximum * total_width) 
    p.draw.rect(screen, back_color, (x, y, total_width, height)) 
    if bar_width > 0: 
        p.draw.rect(screen, bar_color, (x, y, bar_width, height)) 
    screen.blit(ui_font.render('{}:  {} / {}'.format(name.upper(), str(value), str(maximum)), 1, pyRL.colors.Colors.WHITE), (x, y-font_size)) 

def in_bounds(tile): 
    if type(tile.pos_coordinates) == int: 
        return False 
    if (tile.pos_coordinates[0] > -TILE_DIMENSION and tile.pos_coordinates[0] < game_panel.width+TILE_DIMENSION and
        tile.pos_coordinates[1] > -TILE_DIMENSION and tile.pos_coordinates[1] < game_panel.height-TILE_DIMENSION/2): 
        return True 
    else: 
        return False 

def is_blocked(tile, entities): 
    if not tile.is_walkable: 
        return True 
    for e in entities: 
        if e.x == tile.x and e.y == tile.y and not e.is_walkable: 
            return True 
    return False 

def player_move_or_attack(dx, dy): 
    global entities 
    x = player.x + dx 
    y = player.y + dy 
    player.move(dx, dy, level.level, entities) 
    if x == player.x and y == player.y: 
        move_board(dx, dy) 
    
def move_board(dx, dy): 
    global screen_offset 
    screen_offset[0] -= dx * TILE_DIMENSION 
    screen_offset[1] -= dy * TILE_DIMENSION 
    
def place_objects(room): 
    global entities 
    num_monsters = 3 
    for i in range(num_monsters): 
        x = random.randint(room.x1+1, room.x2) 
        y = random.randint(room.y1+1, room.y2) 
        combat_component = CombatComponent(strength=10, defense=0, max_hp=20, xp=20, death_function=enemy_death) 
        ai_component = BasicAI() 
        monster = Entity(x, y, TILE_DIMENSION, [actor_sprite_sheet[1][0]], 'g', pyRL.colors.Colors.GREEN, False, 'goblin', False, combat_component, ai_component, game_font) 
        if not is_blocked(level.level[x][y], entities) and player.x != monster.x and player.y != monster.y: 
            entities.append(monster) 
    x = random.randint(room.x1+1, room.x2) 
    y = random.randint(room.y1+1, room.y2) 
    
def input(): 
    global look_mode 
    dx = 0 
    dy = 0 
    p.event.pump() 
    for e in p.event.get(): 
        if e.type == p.QUIT: 
            sys.exit() 
        if e.type == p.KEYDOWN: 
            if e.key == p.K_ESCAPE: 
                sys.exit() 
            if e.key == p.K_UP: 
                dy = -1 
                player_move_or_attack(dx, dy) 
            elif e.key == p.K_DOWN: 
                dy = 1 
                player_move_or_attack(dx, dy) 
            elif e.key == p.K_LEFT: 
                dx = -1 
                player_move_or_attack(dx, dy) 
            elif e.key == p.K_RIGHT: 
                dx = 1 
                player_move_or_attack(dx, dy) 
            elif e.key == p.K_5: 
                player.took_turn = True 
            elif e.key == p.K_COMMA: 
                for e in entities: 
                    if e.name == 'stairs_down' and e.x == player.x and e.y == player.y: 
                        next_level() 
                    elif e.ascii_tile == '%' and e.x == player.x and e.y == player.y: 
                        player.heal(e.combat_component.max_hp) 
            elif e.key == p.K_c: 
                character_sheet_panel.visible = not character_sheet_panel.visible 
            elif e.key == p.K_l: 
                look_mode = not look_mode 
        else: 
            player.took_turn = False 
            
def update(clock): 
    global state, mouse_pos, fps_counter, screen_offset, fov_recompute 
    if player.took_turn: 
        fov_recompute = True         
    if fov_recompute: 
        fov_recompute = False 
        fov.update(entities=entities, vision_range=8, level=level.level) 
        for ex in fov.explored_tiles: 
            ex.update(screen_offset) 
    if player.took_turn: 
        player.took_turn = False 
        for e in entities: 
            if e.ai_component: 
                e.ai_component.take_turn(player, level.level, entities) 
            e.visible = level.level[e.x][e.y].visible 
            e.update(screen_offset) 
    mouse_pos = p.mouse.get_pos() 
    fps_counter = clock.get_fps() 

def render(): 
    global state 
    screen.fill(GRAY) 
    for panel in base_panels: 
        panel.render() 
    for v in fov.visible_tiles: 
        if in_bounds(v): 
            v.render(screen, font=game_font, mode=1) 
    for ex in fov.explored_tiles: 
        if in_bounds(ex) and not ex.visible: 
            ex.render(screen, font=game_font, mode=1) 
    for e in entities: 
        if e is not player: 
            e.render(screen, 1) 
    player.render(screen, 1) 
    for panel in temp_panels: 
        panel.render() 
        if panel == character_sheet_panel and panel.visible: 
            draw_panel_info(panel, 'Character Info', {'Level':player.level, 'Strength':player.combat_component.strength, 'Defense':player.combat_component.defense}, (panel.top_x, panel.top_y), screen) 
    render_bar(message_panel.top_x, message_panel.top_y+50, 200, 25, 'hp', player.combat_component.current_hp, player.combat_component.max_hp, pyRL.colors.Colors.RED, pyRL.colors.Colors.DRK_RED) 
    render_bar(message_panel.top_x+250, message_panel.top_y+50, 200, 25, 'mp', player.combat_component.current_mp, player.combat_component.max_mp, pyRL.colors.Colors.BLUE, pyRL.colors.Colors.DRK_BLUE) 
    render_bar(message_panel.top_x, message_panel.top_y+message_panel.height-10, message_panel.width, 10, 'xp', player.combat_component.xp, 100, pyRL.colors.Colors.YELLOW, pyRL.colors.Colors.DRK_YELLOW) 
    screen.blit(ui_font.render('Level:  {}'.format(dungeon_level), 1, pyRL.colors.Colors.YELLOW), (message_panel.top_x, message_panel.top_y)) 
    screen.blit(ui_font.render(str((mouse_pos[0], mouse_pos[1])), 1, pyRL.colors.Colors.GREEN), (message_panel.width-100, message_panel.top_y+10)) 
    screen.blit(ui_font.render(str(('{:.2f}'.format(fps_counter))), 1, pyRL.colors.Colors.GREEN), (message_panel.width-50, message_panel.top_y+50)) 
    p.display.flip() 
    
for r in level.rooms: 
    place_objects(r) 

fov = pyRL.fov.FOV() 
clock = p.time.Clock() 
done = False 
mouse_pos = p.mouse.get_pos() 
fps_counter = clock.get_fps() 
fov_recompute = True 
while not done: 
    update(clock) 
    render() 
    input() 
    clock.tick(60) 

p.quit()    