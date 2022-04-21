import numpy as np
import constants as c
import pygame
import random

class ChompGame:
    def __init__(self, row, column, player):
        self.row = row
        self.column = column
        self.fplayer = player
        #todo: define players and set the limit on row and column
        self.board = np.full((row, column), fill_value=1, dtype=int)
        self.end = False

    def visualization_init(self):
        pygame.init()
        size = [int(c.twidth * self.column * 1.5), int(c.theight * self.row * 1.5)]
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Chomp Chomp!")
        screen.fill((c.white))
        refresh = pygame.time.Clock()
        refresh.tick(60)
        self.display(screen)
        return screen

    def display(self, screen):
        for row in range(self.row):
            for column in range(self.column):
                color = c.brown
                if self.board[row, column] == 0:
                    color = c.white
                pygame.draw.rect(screen, color,
                                 [c.twidth * column + c.margin, c.theight * row + c.margin, c.width, c.height])
        color = c.purple
        pygame.draw.rect(screen, color, [c.twidth * 0 + c.margin, c.theight * 0 + c.margin, c.width, c.height])
        pygame.display.flip()

    def select(self, position, turn, screen):
        if position[0] != 'NULL' and position[1] != 'NULL':
            if turn == 'H':
                color = c.blue
            else:
                color = c.red
            pygame.draw.rect(screen, color,
                             [c.twidth * position[1] + c.margin, c.theight * position[0] + c.margin,
                              c.width, c.height])

            pygame.display.flip()
            pygame.time.wait(500)

    def winning_condition(self, position, turn, screen):
        if position[0] == 0 and position[1] == 0:
            if turn == 'H':
                win = 'C'
            else:
                win = 'H'
            print("{} WON!".format(win))
            self.end = True
            font = pygame.font.SysFont('Calibri', int(c.theight * self.row * 1.5), True, False)
            message = 'Winner: ' + win
            message_size = font.size(message)
            text = font.render(message, True, c.black)
            text_coordinates = [int((c.theight * self.row) * 0.5 - message_size[0] * 0.5),
                                int((c.twidth * self.column) * 1.25 - message_size[1] * 0.5)]
            screen.blit(text, text_coordinates)
            pygame.display.flip()
            pygame.time.wait(2000)
            return win

    def human_turn(self):
        select = False
        while not select:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = pygame.mouse.get_pos()
                    column = loc[0] // c.twidth
                    row = loc[1] // c.theight
                    if self.board[row, column] == 1:
                        select = True
                if event.type == pygame.QUIT:
                    self.end = True
                    pygame.quit()
        return row, column


    def play_game(self):
        screen = self.visualization_init()
        cplayer = self.fplayer
        while not self.end:
            if cplayer == 'H':
                pos = self.human_turn()

            elif cplayer == 'C':
                #TODO implement smart move
                pos = self.human_turn()


            self.board[pos[0]:, pos[1]:] = 0

            self.select(pos, cplayer, screen)

            self.display(screen)
            self.winning_condition(pos,cplayer, screen)
            if cplayer == 'C':
                cplayer = 'H'
            elif cplayer == 'H':
                cplayer = 'C'
        pygame.quit()

def possible_moves(array):
    rows, cols = np.where(array == "_")
    possible = []
    for r, c in zip(rows, cols):
        possible.append((r, c))
    return possible

class Player:
    def __init__(self, move='X', dumb=False):
        self.config = {}
        self.stack_configs = []
        self.move = move
        self.games_won = 0
        self.games_lost = 0
        self.games_drawn = 0
        self.dumb = dumb

    def update_config(self, array1):
        temp = tuple(array1.flatten())
        self.stack_configs.append(temp)
        self.config[temp] = possible_moves(array1)

    def player_possible_moves(self, array1):
        temp = tuple(array1.flatten())
        if temp not in self.config:
            self.update_config(array1)
        return self.config[temp]

    def punish(self, last_move):
        if not self.dumb:
            for i in range(len(last_move)):
                r, c = last_move[i]
                last_config = self.stack_configs[i]
                # print(len(self.config[last_config]))
                self.config[last_config].remove((r, c))
        self.stack_configs = []

    def reward(self, last_move, win_draw):
        if not self.dumb:
            for i in range(len(last_move)):
                r, c = last_move[i]
                last_config = self.stack_configs[i]
                if win_draw == 'win':
                    self.config[last_config].append((r, c))
                    self.config[last_config].append((r, c))
                    self.config[last_config].append((r, c))
                elif win_draw == 'draw':
                    self.config[last_config].append((r, c))
        self.stack_configs = []






game = ChompGame(18,18,'H')
game.play_game()




