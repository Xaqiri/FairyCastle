import pygame as p 
import random 
import sys 
import os 
from time import * 

import pyRL 
import random_level_gen 
from ui import * 
from item import * 
from heal import * 
from tile import * 
from entity import * 
from basic_ai import * 
from combat_component import * 

p.init() 
# Version #.  Release.mainBranch.testBranch 
VER =           '0.10.23' 
p.display.set_caption('Fairy Castle' + ',    version:  ' + VER) 

''' BUGS ''' 
# Fix phantom wall bug:  Some times the player can walk through tiles that are displayed as walls, and can't walk through tiles displayed as floors 
# After moving around the level for a while, the game things the player is one tile further to the right than they actually are 
# i.e. start the dungeon at (7, 34), going (floor, player, floor, wall).  After walking around for a while and returning to the start position, 
# the player at (7, 34) will be one to the left, (player, floor, floor, wall), and will not be able to move to the right 
# Not limited to the x direction 
# Bug doesn't seem to be caused by the screen_offset (returning to the start position after the bug sets in displays the same screen_offset the game started with) 

# Fix efficiency 
# A 32x32 map takes about 20ms to update and 30ms to render.  A 64x64 map takes about 70ms and 100ms. (on my laptop) 

''' TODO ''' 
# Add comments 
# Make code cleaner 
# Make tiles outside of the player's fov more interesting, possibly have tiles fade out after they leave the player's fov 
# e.g. a tile's visible to the player.  They move one tile to the right, so the tiles that are now outside of the player's fov fade out over two seconds or so 
# Add equipment 
# Add spell scrolls 
# Add mouseover info for enemies 

''' Colors ''' 
TRANS = (128, 0, 128) 
BLACK = pyRL.colors.Colors.BLACK 
GREEN = pyRL.colors.Colors.GREEN 
GRAY  = pyRL.colors.Colors.DRKR_GRAY 

try: 
    arg = int(sys.argv[1]) 
    if arg <= 3: 
        SCALE = arg 
    else: 
        SCALE = 1 
except: 
    SCALE = 1 

try: 
    arg = int(sys.argv[2]) 
    if arg == 0 or arg == 1: 
        render_mode = arg 
    else: 
        render_mode = 1 
except: 
    render_mode = 1 

TILE_DIMENSION = int(16*SCALE) 
window_size = window_width, window_height = 1200, 700 
SCREEN_CENTER = (window_width//2, window_height//2) 
screen = p.display.set_mode(window_size) 
game_panel = pyRL.panel.Panel(0, 0, window_width, window_height-100, pyRL.colors.Colors.DRKR_GRAY, screen, True) 
message_panel = pyRL.panel.Panel(0, game_panel.height, window_width, window_height-game_panel.height, pyRL.colors.Colors.DRK_GRAY, screen, True) 
character_sheet_panel = pyRL.panel.Panel(0, 0, game_panel.width/3, game_panel.height, pyRL.colors.Colors.DRK_GREEN, screen) 
mouse_info_panel = pyRL.panel.Panel(0, 0, 350, 100, pyRL.colors.Colors.DRK_GREEN, screen) 
base_panels = [game_panel, message_panel] 
temp_panels = [character_sheet_panel, mouse_info_panel] 
font_size = 16 
fonts = ['palatino', 'consolas', 'courier', 'terminal']
ui_font = p.font.SysFont('consolas', font_size) 
game_font = p.font.SysFont('terminal', 32) 
sprites = dict(actorSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'actorSpriteSheet13x6.png')).convert(), 
                environmentSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'environmentSpriteSheet15x8.png')).convert(), 
                itemSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 
                                                    'itemSpriteSheet14x14.png')).convert(), 
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
                                    16, 1, 14, 14).sprites 

combat_component = CombatComponent(strength=10, defense=1) 
player = Entity(x=1, y=1, sprites=[actor_sprite_sheet[0][0], actor_sprite_sheet[0][4]], tile_size=TILE_DIMENSION, name='player', color=pyRL.colors.Colors.CYAN, combat_component=combat_component, font=game_font) 
entities = [player] 
level = random_level_gen.RandomLevelGen(room_min_size=4, room_max_size=8, max_rooms=50, level_width=32, level_height=32, tile_size=TILE_DIMENSION, sprites=[environment_sprite_sheet[1][6], environment_sprite_sheet[4][6], environment_sprite_sheet[0][7]], level_font=game_font) 
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
    level = random_level_gen.RandomLevelGen(room_min_size=4, room_max_size=8, max_rooms=50, level_width=32, level_height=32, tile_size=TILE_DIMENSION, sprites=[environment_sprite_sheet[1][6], environment_sprite_sheet[4][6], environment_sprite_sheet[0][7]], level_font=game_font) 
    level.make_level(entities) 
    screen_offset = [game_panel.center[0]-player.x*TILE_DIMENSION, game_panel.center[1]-player.y*TILE_DIMENSION] 
    player.pos_coordinates = [player.x*player.tile_size+screen_offset[0], player.y*player.tile_size+screen_offset[1]] 
    dungeon_level += 1 
    for r in level.rooms: 
        place_objects(r, dungeon_level) 
    init_fov() 
    player.took_turn = True 
    
def enemy_death(monster): 
    global entities 
    monster.ascii_tile = '%' 
    monster.current_sprite = monster.death_sprite 
    monster.current_sprite.set_alpha(185) 
    monster.color = pyRL.colors.Colors.RED 
    monster.is_walkable = True 
    monster.ai_component = None 
    monster.name = 'remains of {}'.format(monster.name) 
    
def draw_panel_info(panel, label, info, start_pos, screen): 
    y_offset = 50 
    screen.blit(ui_font.render(label, 1, pyRL.colors.Colors.WHITE), (start_pos[0], start_pos[1])) 
    for key, value in info.items(): 
        screen.blit(ui_font.render('{}:  {}'.format(key, value), 1, pyRL.colors.Colors.WHITE), (start_pos[0], start_pos[1]+y_offset)) 
        y_offset+=font_size 

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

def random_choice_index(chances): 
    dice = random.randint(1, sum(chances)) 
    running_sum = 0 
    choice = 0 
    for w in chances: 
        running_sum += w 
        if dice <= running_sum: 
            return choice 
        choice += 1 

def random_choice(chances_dict): 
    chances = chances_dict.values() 
    strings = [key for key in chances_dict.keys()]
    return strings[random_choice_index(chances)] 

def from_dungeon_level(table, dungeon_level): 
    for (value, level) in reversed(table): 
        if dungeon_level >= level: 
            return value 
    return 0 

def place_objects(room, dungeon_level): 
    global entities 
    max_monsters = from_dungeon_level([[2, 1], [3, 2], [6, 3]], dungeon_level) 
    monster_chances = {} 
    monster_chances['goblin'] = 70 
    monster_chances['troll'] = from_dungeon_level([[10, 2], [20, 3], [60, 4], [80, 5]], dungeon_level) 
    num_monsters = random.randint(0, max_monsters) 

    max_items = from_dungeon_level([[1, 1]], dungeon_level) 
    item_chances = {} 
    item_chances['hp_potion'] = from_dungeon_level([[80, 1], [60, 3], [20, 4]], dungeon_level) 
    num_items = random.randint(0, max_items) 

    for i in range(num_monsters): 
        x = random.randint(room.x1+1, room.x2-1) 
        y = random.randint(room.y1+1, room.y2-1) 
        if not is_blocked(level.level[x][y], entities) and (player.x != x and player.y != y): 
            choice = random_choice(monster_chances) 
            if choice == 'goblin': 
                combat_component = CombatComponent(strength=10, defense=0, max_hp=20, xp=20, death_function=enemy_death) 
                ai_component = BasicAI() 
                monster = Entity(x, y, TILE_DIMENSION, [actor_sprite_sheet[1][0], actor_sprite_sheet[1][4]], 'g', pyRL.colors.Colors.GREEN, False, 'goblin', False, combat_component, ai_component, game_font) 
            elif choice == 'troll': 
                combat_component = CombatComponent(strength=20, defense=4, max_hp=50, xp=80, death_function=enemy_death) 
                ai_component = BasicAI() 
                monster = Entity(x, y, TILE_DIMENSION, [actor_sprite_sheet[1][1], actor_sprite_sheet[3][4]], 'T', pyRL.colors.Colors.YELLOW, False, 'troll', False, combat_component, ai_component, game_font) 
            entities.append(monster) 
    for i in range(num_items): 
        x = random.randint(room.x1+1, room.x2-1) 
        y = random.randint(room.y1+1, room.y2-1) 
        if not is_blocked(level.level[x][y], entities) and (level.stairs.x != x and level.stairs.y != y): 
            choice = random_choice(item_chances) 
            if choice == 'hp_potion': 
                heal_component = Heal(amount=30) 
                item_component = Item(use_component=heal_component) 
                item = Entity(x=x, y=y, tile_size=TILE_DIMENSION, sprites=item_sprite_sheet[3][12], ascii_tile='!', color=pyRL.colors.Colors.RED, is_walkable=True, name='hp potion', always_visible=True, combat_component=None, ai_component=None, font=game_font, item_component=item_component) 
            entities.append(item) 
    #x = random.randint(room.x1+1, room.x2) 
    #y = random.randint(room.y1+1, room.y2) 
    
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
                    if e.x == player.x and e.y == player.y: 
                        if e.name == 'stairs_down' and dungeon_level < 5: 
                            next_level() 
                        elif e.ascii_tile == '!': 
                            e.item_component.pick_up(player.inventory) 
                            entities.remove(e) 
            elif e.key == p.K_c: 
                character_sheet_panel.visible = not character_sheet_panel.visible 
            elif e.key == p.K_i: 
                print(player.inventory) 
            elif e.key == p.K_q: 
                for i in player.inventory: 
                    if i.name == 'hp potion': 
                        i.item_component.use(player) 
                        break 
            elif e.key == p.K_l: 
                look_mode = not look_mode 
                mouse_info_panel.visible = not mouse_info_panel.visible 
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
            e.explored = level.level[e.x][e.y].explored 
            e.update(screen_offset) 
    mouse_pos = p.mouse.get_pos() 
    fps_counter = clock.get_fps() 
    mouse_info_panel.origin = mouse_pos 
    
def render(): 
    global state 
    screen.fill(GRAY) 
    for panel in base_panels: 
        panel.render() 
    for v in fov.visible_tiles: 
        if in_bounds(v): 
            v.render(screen, font=game_font, mode=render_mode) 
    for ex in fov.explored_tiles: 
        if in_bounds(ex) and not ex.visible: 
            ex.render(screen, font=game_font, mode=render_mode) 
    for e in entities: 
        if e is not player: 
            try: 
                e.render(screen, render_mode) 
            except: 
                print(e.name) 
                break 
    player.render(screen, render_mode) 
    for panel in temp_panels: 
        panel.render() 
        if panel == character_sheet_panel and panel.visible: 
            draw_panel_info(panel, 'Character Info', {'Level':player.level, 'Strength':player.combat_component.strength, 'Defense':player.combat_component.defense}, (panel.top_x, panel.top_y), screen) 
        if panel == mouse_info_panel and look_mode and panel.visible: 
            draw_panel_info(panel, 'Allan', {'Description':'please add text'}, panel.origin, screen) 
    render_bar(message_panel.top_x, message_panel.top_y+50, 200, 25, 'hp', player.combat_component.current_hp, player.combat_component.max_hp, pyRL.colors.Colors.RED, pyRL.colors.Colors.DRK_RED) 
    render_bar(message_panel.top_x+250, message_panel.top_y+50, 200, 25, 'mp', player.combat_component.current_mp, player.combat_component.max_mp, pyRL.colors.Colors.BLUE, pyRL.colors.Colors.DRK_BLUE) 
    render_bar(message_panel.top_x, message_panel.top_y+message_panel.height-10, message_panel.width, 10, 'xp', player.combat_component.xp, 100, pyRL.colors.Colors.YELLOW, pyRL.colors.Colors.DRK_YELLOW) 
    screen.blit(ui_font.render('Level:  {}'.format(dungeon_level), 1, pyRL.colors.Colors.YELLOW), (message_panel.top_x, message_panel.top_y)) 
    screen.blit(ui_font.render(str((mouse_pos[0], mouse_pos[1])), 1, pyRL.colors.Colors.GREEN), (message_panel.width-100, message_panel.top_y+10)) 
    screen.blit(ui_font.render(str(('{:.2f}'.format(fps_counter))), 1, pyRL.colors.Colors.GREEN), (message_panel.width-50, message_panel.top_y+50)) 
    p.display.flip() 

def time_test(func): 
    t = p.time.get_ticks() 
    func 
    t2 = p.time.get_ticks() 
    print('Func took:  {}ms'.format(t2-t)) 

for r in level.rooms: 
    place_objects(r, dungeon_level) 

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