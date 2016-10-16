import pygame as p 
p.init() 

''' TODO ''' 
# Display more information on the tile that the mouse is on, such as entity stats, class, equipment, etc. 
# Fix cursor position 
# Consider moving all cursor code outside of ui.  One fix might be to make the cursor a tile in its own ui_board to make determining the position of things easier 

class UI(): 
    ''' Holds all information relating to the ui '''
    def __init__(self, window_size, board_size, font_size, tile_size, SCREEN_OFFSET, cursor): 
        self.edge = (window_size[0] // 4*3, 0), (window_size[0] // 4*3, window_size[1]) 
        self.board_size = board_size[0]*tile_size, board_size[1]*tile_size 
        self.ui_pos = window_size[0] // 4*3 + 10 
        self.font_size = font_size 
        self.font = p.font.SysFont('comicsans', font_size) 
        self.tile_size = tile_size 
        self.cursor = cursor 
        self.SCREEN_OFFSET = SCREEN_OFFSET 
        self.mouse_pos = 0 
        self.mouse_index = [0, 0] 
        self.fps_counter = 0 
        
    def update(self, clock, SCREEN_OFFSET, game_board): 
        self.SCREEN_OFFSET = SCREEN_OFFSET[0], SCREEN_OFFSET[1] 
        self.mouse_pos = (p.mouse.get_pos()[0], p.mouse.get_pos()[1]) 
        #self.mouse_index = self.mouse_pos[0]//self.tile_size, self.mouse_pos[1]//self.tile_size 
        self.fps_counter = clock.get_fps() 
        self.mouse_index = [ 
            (self.mouse_pos[0]-self.SCREEN_OFFSET[0])//32, 
            (self.mouse_pos[1]-self.SCREEN_OFFSET[1])//32 
        ] 
        try: 
            game_board[self.mouse_index[0]][self.mouse_index[1]].sprite.append(self.cursor) 
        except: 
            pass 
        
    def render(self, screen, color, game_board, actor_board): 
        try: 
            game_board[self.mouse_index[0]][self.mouse_index[1]].sprite.pop() 
        except: 
            pass 
        # Draws the edge of the ui 
        p.draw.line(screen, color, self.edge[0], self.edge[1], 2) 
        # Displays the mouse position in pixel coordinates 
        screen.blit(self.font.render(str((self.mouse_pos[0], self.mouse_pos[1])), 1, color), (self.ui_pos, 10)) 
        # Displays the fps counter 
        screen.blit(self.font.render("fps: " + str('{:.2f}'.format(self.fps_counter)), 1, color), (self.ui_pos+60, 400)) 
        # Check to see if mouse is within bounds of the game board 
        if (self.mouse_pos[0] < self.edge[0][0] and self.mouse_pos[0] > 0 and self.mouse_pos[0] < self.board_size[0] and self.mouse_pos[1] > 0 and self.mouse_pos[1] < self.board_size[1] and self.mouse_index[0] >= 0 and self.mouse_index[1] >= 0 and game_board[self.mouse_index[0]][self.mouse_index[1]].revealed): 
            # If it is, check to see what type of tile the mouse is over 
            if type(actor_board[self.mouse_index[0]][self.mouse_index[1]]) != int: 
                # If the tile is an actor, display the tile information in the ui 
                screen.blit(self.font.render(str(game_board[self.mouse_index[0]][self.mouse_index[1]]), 1, color), (self.ui_pos, 40)) 
                screen.blit(self.font.render(str(actor_board[self.mouse_index[0]][self.mouse_index[1]]), 1, color), (self.ui_pos, 80)) 
                try: 
                    screen.blit(self.font.render("HP:  {}".format(actor_board[self.mouse_index[0]][self.mouse_index[1]].hp), 1, (255, 100, 100)), (self.ui_pos, 120)) 
                except: 
                    pass 
                try: 
                    screen.blit(self.font.render("MP:  {}".format(actor_board[self.mouse_index[0]][self.mouse_index[1]].mp), 1, (100, 100, 255)), (self.ui_pos, 150)) 
                except: 
                    pass 
            else: 
                # If the tile isn't an actor, just display the floor information 
                screen.blit(self.font.render(str(game_board[self.mouse_index[0]][self.mouse_index[1]]), 1, color), (self.ui_pos, 40)) 
            # Display the position in the game board of the tile the mouse is over 
            screen.blit(self.font.render('(' + (str(game_board[self.mouse_index[0]][self.mouse_index[1]].pos_index[0])) + ', ' + (str(game_board[self.mouse_index[0]][self.mouse_index[1]].pos_index[1])) + ')', 1, color), (self.ui_pos+120, 10)) 
        else: 
            # If the mouse is not in the bounds of the game board 
            screen.blit(self.font.render('The ui', 1, color), (self.ui_pos, 40)) 

    def draw_cursor(self, screen, game_board): 
        # Get game_board index using cursor position, then draw cursor at game_board index position 

        # Displays the cursor sprite on the tile the mouse is over 
        #screen.blit(self.cursor, (x, y)) 
        pass 