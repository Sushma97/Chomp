import numpy as np
import constants as c
import pygame
import random
import pickle
import training


class ChompGame:
    def __init__(self, row, column, player):
        self.row = row
        self.column = column
        self.fplayer = player
        # todo: define players and set the limit on row and column
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
            font = pygame.font.SysFont('Calibri', int(c.theight * self.row * 0.25), True, False)
            message = 'Winner: ' + win
            message_size = font.size(message)
            text = font.render(message, True, c.black)
            text_coordinates = [int((c.theight * self.row * 0.75) - (message_size[0] * 0.5)),
                                int((c.twidth * self.column * 1.05) - (message_size[1] * 0.5))]
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
        last_move_H = []
        last_move_C = []
        # player = Player()
        player = training.load_player(self.row, self.column)
        while not self.end:
            if cplayer == 'H':
                pos = self.human_turn()
                Hpos = pos
                # last_move_H.append(Hpos)
            elif cplayer == 'C':
                # TODO implement smart move
                #####

                player.update_config(self.board)
                row1, col1 = player.next_move(self.board, player)
                training.add_element(row1, col1, 0, self.board)
                last_move_C.append((row1, col1))
                #####
                # pos = self.human_turn()
                pos = (row1, col1)
                Cpos = pos
            self.board[pos[0]:, pos[1]:] = 0

            self.select(pos, cplayer, screen)

            self.display(screen)
            win = self.winning_condition(pos, cplayer, screen)
            ###
            if self.end and win == 'C':
                # player.punish(last_move_H)
                player.reward(last_move_C)
            elif self.end and win == 'H':
                player.punish(last_move_C)
                # player.reward(last_move_H, 'win')


            ###
            if cplayer == 'C':
                cplayer = 'H'
            elif cplayer == 'H':
                cplayer = 'C'
        pygame.quit()
        pickle.dump(player, open("player1_" + str(self.row) + "_" + str(self.column) + ".pkl", "wb"))


if __name__ == "__main__":
    # training.initial_train(9,9, 10000)
    # training.continuous_train(9,9)
    game = ChompGame(9,9,'H')
    game.play_game()
