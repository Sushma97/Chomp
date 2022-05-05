import numpy as np
import pickle
import random
from ChompGame import ChompGame
import pygame
import constants as C
from Player import Player
import training

class Antidote_Player(Player):
    # original_sustenance = int(game.poisons)
    def __init__(self, game, *args, **kwargs):

        self.sustenance = int(game.poisons)
        self.has_eaten_poison = False
        super().__init__(*args, **kwargs)

    def possible_moves(self,array):
        rows, cols = np.where((array != 0) & (array != 'X') & (array != 'O'))
        possible = []
        for r, c in zip(rows, cols):
            if (r, c) != (0, 0):
                possible.append((r, c))
        return possible if len(possible) > 0 else [(0, 0)]

class Human_Player:
    def __init__(self, game):
        self.sustenance = int(game.poisons)
        self.has_eaten_poison = False
        self.name = 'Human'


class Poison_Antidote(ChompGame):

    def __init__(self, *args):
        super().__init__(*args)
        self.poisons = None
        self.antidotes = None
        self.board = self.board.astype(object)

    def display(self, screen):
        screen.fill(C.white)
        for row in range(self.row):
            for column in range(self.column):
                color = C.brown
                if self.board[row, column] == 0:
                    color = C.white
                elif self.board[row,column]=='X':
                    color = C.green
                elif self.board[row, column]=='O':
                    color = C.yellow
                pygame.draw.rect(screen, color,
                                 [C.twidth * column + C.margin, C.theight * row + C.margin, C.width, C.height])

        pygame.display.flip()
    def display_msg(self,screen,player1, player2 ):
        font = pygame.font.SysFont('Calibri', int(C.theight - 4), True, False)
        message1 = f'{player1.name} has {player1.sustenance} chances remaining to live!'
        message2 = f'{player2.name} has {player2.sustenance} chances remaining to live!'
        message_size1 = font.size(message1)
        message_size2 = font.size(message2)
        text1 = font.render(message1, True, C.black)
        text2 = font.render(message2, True, C.black)
        text_coordinates1 = [int((C.theight * self.row * 0.75) - (message_size1[0] * 0.5)),
                             int((C.twidth * self.column * 1.05) - (message_size1[1] * 0.5))]
        text_coordinates2 = [int((C.theight * self.row * 0.75) - (message_size2[0] * 0.5)),
                             int((C.twidth * self.column * 1.05) - (message_size2[1] * 0.5))+20]
        screen.blit(text1, text_coordinates1)
        screen.blit(text2, text_coordinates2)
        pygame.display.flip()
    def human_turn(self):
        select = False
        while not select:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = pygame.mouse.get_pos()
                    column = loc[0] // C.twidth
                    row = loc[1] // C.theight
                    if self.board[row, column] in (1,'P','A'):
                        select = True
                if event.type == pygame.QUIT:
                    self.end = True
                    pygame.quit()
        return row, column

    def set_poison_antidote(self):
        #Number of poisons and antidote
        self.antidotes = self.poisons = int(C.poison_antidote_ratio*self.row*self.column)
        #randomly choose antidotes + poisons number of points from the board
        total_cells_board = self.row*self.column
        points = np.random.choice(total_cells_board,self.antidotes*self.poisons,replace = False)
        flag = -1
        for i in points:
            row = i//self.row
            col = i%self.column
            if flag >0:
                self.board[row, col] = 'A'
                flag*=-1
            else:
                self.board[row,col] = 'P'
                flag *=-1


    def winning_condition(self, position, player, screen):

        if self.board[position[0], position[1]] == 'P':
            self.board[position[0], position[1]] = 'X'
            player.has_eaten_poison = True
            player.sustenance -= 1
            # font = pygame.font.SysFont('Calibri', int(C.theight* 0.25), True, False)
            message = f'{player.name} You have been poisoned!'
            print(message)

        elif self.board[position[0], position[1]] == 'A':
            self.board[position[0], position[1]] = 'O'
            if player.has_eaten_poison:
                player.sustenance = self.poisons
                player.has_eaten_poison = False
                # font = pygame.font.SysFont('Calibri', int(C.theight* 0.25), True, False)
                message = f'{player.name} You have found the antidode!'
                print(message)

        else:
            self.board[position[0], position[1]] = 0
            if player.has_eaten_poison:
                player.sustenance -= 1
        if player.has_eaten_poison:
            if player.sustenance <= 0:
                # player has lost since he has zero sustenance
                if player.name == 'Human':
                    win = 'Computer'
                else:
                    win = 'Human'
                message = "{} WON!".format(win)
                print("{} WON!".format(win))
                self.end = True
                screen.fill(C.white)
                font = pygame.font.SysFont('Calibri', int(C.theight), True, False)
                message_size = font.size(message)
                text = font.render(message, True, C.black)
                text_coordinates = [int((C.theight * self.row * 0.5) - (message_size[0] * 0.5)),
                                    int((C.twidth * self.column * 0.5) - (message_size[1] * 0.5))]
                screen.blit(text, text_coordinates)
                pygame.display.flip()
                pygame.time.wait(2000)
                return win
            else:
                message = f'{player.name} has {player.sustenance} chances remaining'
                print(f'{player.name} has {player.sustenance} chances remaining')


    def play_game(self):
        screen = self.visualization_init()
        self.set_poison_antidote()
        print(self.board)
        cplayer = self.fplayer
        human_player = Human_Player(self)
        ai_player = Antidote_Player(self,'Computer',dumb = True)
        last_move_H = []
        last_move_C = []
        while not self.end:
            if cplayer == 'H':
                pos = self.human_turn()
                player = human_player
                print('Human selected: ',pos)
            elif cplayer == 'C':
                player = ai_player
                player.update_config(self.board)
                row1, col1 = player.next_move(self.board, player)
                # training.add_element(row1, col1, 0, self.board)
                last_move_C.append((row1, col1))
                pos = (row1, col1)
                Cpos = pos
                print('Computer selected: ', pos)
            win = self.winning_condition(pos, player, screen)

            self.select(pos, cplayer, screen)
            self.display(screen)
            self.display_msg(screen, human_player, ai_player)

            if self.end and win == 'C':
                ai_player.reward(last_move_C)
            elif self.end and win == 'H':
                ai_player.punish(last_move_C)
                # player.reward(last_move_H, 'win')
            if cplayer == 'C':
                cplayer = 'H'
            elif cplayer == 'H':
                cplayer = 'C'
        pygame.quit()

if __name__ == '__main__':
    # player =
    game1 = Poison_Antidote(10,10,'C')
    # print(game1.poisons)
    # player = Antidote_Player(game1,'Player1',dumb=False)
    game1.play_game()
