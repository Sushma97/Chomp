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
        #
        # static
    def possible_moves(self,array):
        rows, cols = np.where(array != 0)
        possible = []
        for r, c in zip(rows, cols):
            if (r, c) != (0, 0):
                possible.append((r, c))
        return possible if len(possible) > 0 else [(0, 0)]

class Human_Player:
    def __init__(self, game):
        self.sustenance = int(game.poisons)
        self.has_eaten_poison = False


class Poison_Antidote(ChompGame):

    def __init__(self, *args):
        super().__init__(*args)
        self.poisons = None
        self.antidotes = None
        self.board = self.board.astype(object)
        # self.sustenance = None
    # def display(self, screen):
    #     for row in range(self.row):
    #         for column in range(self.column):
    #             color = C.brown
    #             if self.board[row, column] == 0:
    #                 color = C.white
    #             # elif self.board[row,column]=='P':
    #             #     color = C.green
    #             # elif self.board[row, column]=='A':
    #             #     color = C.yellow
    #             pygame.draw.rect(screen, color,
    #                              [C.twidth * column + C.margin, C.theight * row + C.margin, C.width, C.height])
    #     # color = C.purple
    #     # pygame.draw.rect(screen, color, [C.twidth * 0 + C.margin, C.theight * 0 + C.margin, C.width, C.height])
    #     pygame.display.flip()
    # def select(self, position, turn, screen):
    #     if position[0] != 'NULL' and position[1] != 'NULL':
    #         if turn == 'H':
    #             color = c.blue
    #         else:
    #             color = c.red
    #         pygame.draw.rect(screen, color,
    #                          [c.twidth * position[1] + c.margin, c.theight * position[0] + c.margin,
    #                           c.width, c.height])
    #
    #         pygame.display.flip()
    #         pygame.time.wait(500)
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
        # self.sustenance = int(self.poisons*0.5)
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

    #     #Place the antidotes and poisons on the board
    #
    #     poison_positions = np.random.choice()
    # def eat_poison(self, position, player_turn, screen):
    #     if self.board[position[0], position[1]] == 'P':

    def winning_condition(self, position, player, screen):
        if player.sustenance <=0:
            #player has lost since he has zero sustenance
            if player == 'H':
                win = 'C'
            else:
                win = 'H'
            print("{} WON!".format(win))
            self.end = True
            font = pygame.font.SysFont('Calibri', int(C.theight * self.row * 0.25), True, False)
            message = 'Winner: ' + win
            message_size = font.size(message)
            text = font.render(message, True, C.black)
            text_coordinates = [int((C.theight * self.row * 0.75) - (message_size[0] * 0.5)),
                                int((C.twidth * self.column * 1.05) - (message_size[1] * 0.5))]
            screen.blit(text, text_coordinates)
            pygame.display.flip()
            pygame.time.wait(2000)
            return win
        if self.board[position[0], position[1]]=='P':
            player.has_eaten_poison = True
            player.sustenance -= 1
            font = pygame.font.SysFont('Calibri', int(C.theight* 0.25), True, False)
            message = 'You have been poisoned!'
            message_size = font.size(message)
            text = font.render(message, True, C.black)
            text_coordinates = [int((C.theight * self.row ) - (message_size[0] * 0.5)),
                                int((C.twidth * self.column ) - (message_size[1] * 0.5))]
            # screen.fill(pygame.Color('white'),tuple(text_coordinates))
            pygame.display.update()
            screen.blit(text, text_coordinates)
            pygame.display.flip()
            pygame.time.wait(2000)
        elif self.board[position[0], position[1]]=='A':
            if player.has_eaten_poison:
                player.sustenance = self.poisons
                player.has_eaten_poison = False
                font = pygame.font.SysFont('Calibri', int(C.theight* 0.25), True, False)
                message = 'You have found the antidode!'
                message_size = font.size(message)
                text = font.render(message, True, C.black)
                text_coordinates = [int((C.theight * self.row ) - (message_size[0] * 0.5)),
                                    int((C.twidth * self.column ) - (message_size[1] * 0.5))]
                screen.blit(text, text_coordinates)
                pygame.display.flip()
                pygame.time.wait(2000)
        else:
            if player.has_eaten_poison:
                player.sustenance -= 1
                font = pygame.font.SysFont('Calibri', int(C.theight * self.row * 0.25), True, False)
                message = f'You have {player.sustenance} chances remaining to live!'
                message_size = font.size(message)
                text = font.render(message, True, C.black)
                text_coordinates = [int((C.theight * self.row * 0.75) - (message_size[0] * 0.5)),
                                    int((C.twidth * self.column * 1.05) - (message_size[1] * 0.5))]
                screen.blit(text, text_coordinates)
                pygame.display.flip()
                pygame.time.wait(2000)




    def play_game(self):
        screen = self.visualization_init()
        self.set_poison_antidote()
        print(self.board)
        cplayer = self.fplayer
        # if cplayer == 'H':
        human_player = Human_Player(self)
        # if cplayer == 'C':
        ai_player = Antidote_Player(self,'player1',dumb = True)
        last_move_H = []
        last_move_C = []
        # player = Antidote_Player(self, 'player1',dumb = True)
        while not self.end:
            if cplayer == 'H':
                pos = self.human_turn()
                player = human_player
                print(pos)
            elif cplayer == 'C':
                player = ai_player
                # player = training.load_player(self.row, self.column)
                player.update_config(self.board)
                row1, col1 = player.next_move(self.board, player)
                # training.add_element(row1, col1, 0, self.board)
                last_move_C.append((row1, col1))
                pos = (row1, col1)
                Cpos = pos
            #check the poison_antidote
            # if self.board[pos[0], pos[1]]=='P':
            #
            # elif self.board[pos[0], pos[1]]=='A':
            #
            win = self.winning_condition(pos, player, screen)
            self.board[pos[0], pos[1]] = 0
            self.select(pos, cplayer, screen)
            self.display(screen)

            if self.end and win == 'C':
                # player.punish(last_move_H)
                ai_player.reward(last_move_C)
            elif self.end and win == 'H':
                ai_player.punish(last_move_C)
                # player.reward(last_move_H, 'win')
            # pickle.dump(player, open("player1_" + str(self.row) + "_" + str(self.column) + ".pkl", "wb"))

            ###
            if cplayer == 'C':
                cplayer = 'H'
            elif cplayer == 'H':
                cplayer = 'C'
        pygame.quit()

if __name__ == '__main__':
    # player =
    game1 = Poison_Antidote(10,10,'H')
    # print(game1.poisons)
    # player = Antidote_Player(game1,'Player1',dumb=False)
    game1.play_game()
