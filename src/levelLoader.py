import pygame as p 
from tile import * 
from player import * 
from goblin import * 

''' TODO '''
# Won't load level_2.txt, probably because it's too small 

class LevelLoader(object): 
    def __init__(self, file, window_size, actorSprites, environmentSprites, itemSprites): 
        ''' The level is created from a text file containing the layout of the level 
        mapHeight and mapWidth are the dimensions of the map in the text file 
        width and height are the dimensions of the screen ''' 
        self.file = file 
        self.window_width = window_size[0] 
        self.window_height = window_size[1] 
        self.board_width = 0 
        self.board_height = 0 
        self.game_board = [] 
        self.actor_board = [] 
        self.actorSprites = actorSprites 
        self.environmentSprites = environmentSprites 
        self.itemSprites = itemSprites 
        self.player = 0 
        self.enemies = [] 
    
    def load(self, TILE_DIMENSION): 
        f = open(self.file) 
        lines = [line.rstrip('\n') for line in f] 
        self.board_height = len(lines) 
        self.board_width = len(lines[0]) 
        self.game_board = [[0]*self.board_height for x in range(self.board_width)]
        self.actor_board = [[0]*self.board_height for x in range(self.board_width)]
        for y in range(self.board_height): 
            for x in range(self.board_width): 
                if lines[y][x] == '#': 
                    self.game_board[x][y] = Tile([self.environmentSprites[1][4]], (x, y), TILE_DIMENSION, 'A wall', 'wall', False) 
                elif lines[y][x] == '.': 
                    self.game_board[x][y] = Tile([self.environmentSprites[3][6]], (x, y), TILE_DIMENSION, 'The floor', 'floor') 
                elif lines[y][x] == '@': 
                    self.game_board[x][y] = Tile([self.environmentSprites[3][6]], (x, y), TILE_DIMENSION, 'The floor', 'floor') 
                    player_pos = (x, y) 
                elif lines[y][x] == 'g': 
                    self.game_board[x][y] = Tile([self.environmentSprites[3][6]], (x, y), TILE_DIMENSION, 'The floor', 'floor') 
                    self.actor_board[x][y] = Goblin([self.actorSprites[1][0]], (x, y), TILE_DIMENSION) 
                    self.enemies.append(self.actor_board[x][y]) 
                elif lines[y][x] == '~': 
                    self.game_board[x][y] = Tile([self.environmentSprites[1][1]], (x, y), TILE_DIMENSION, 'Some water', 'tile', False) 
                elif lines[y][x] == '|': 
                    self.game_board[x][y] = Tile([self.environmentSprites[2][7]], (x, y), TILE_DIMENSION, 'A door', 'door') 
                elif lines[y][x] == '!': 
                    self.game_board[x][y] = Tile([self.environmentSprites[3][6], self.itemSprites[0][6]], (x, y), TILE_DIMENSION, 'A potion') 
                elif lines[y][x] == '>': 
                    self.game_board[x][y] = Tile([self.environmentSprites[3][6], self.environmentSprites[0][7]], (x, y), TILE_DIMENSION, 'A way down') 
                elif lines[y][x] == '0': 
                    self.game_board[x][y] = Tile([self.environmentSprites[3][6], self.itemSprites[1][7]], (x, y), TILE_DIMENSION, 'A closed barrel') 
                elif lines[y][x] == '1': 
                    self.game_board[x][y] = Tile([self.itemSprites[3][7]], (x, y), TILE_DIMENSION, 'An unopened crate') 
                else: 
                    self.game_board[x][y] = Tile([self.environmentSprites[1][6]], (x, y), TILE_DIMENSION, 'Temp Empty', 'abyss', False) 
        self.player = Player([self.actorSprites[0][0], self.itemSprites[4][1], self.itemSprites[4][2], self.itemSprites[4][3]], player_pos, TILE_DIMENSION, self.game_board, self.actor_board) 
        self.actor_board[player_pos[0]][player_pos[1]] = self.player 
        f.close() 

    def render(self, screen, player, TILE_DIMENSION, SCREEN_OFFSET, ui): 
        self.player.update(SCREEN_OFFSET) 
        self.game_board[self.player.pos_index[0]][self.player.pos_index[1]].revealed = True 
        for i in self.player.fov.visible_tiles: 
            try: 
                i.update(SCREEN_OFFSET) 
                i.render(screen) 
            except: 
                pass 
        self.player.render(screen) 