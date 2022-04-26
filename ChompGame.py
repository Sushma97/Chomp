import numpy as np
import constants as c
import pygame
import random
import pickle


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
            font = pygame.font.SysFont('Calibri', int(c.theight * 1.5), True, False)
            message = 'Winner: ' + win
            message_size = font.size(message)
            text = font.render(message, True, c.black)
            text_coordinates = [int(c.twidth * self.column * 1.5*0.5),int(c.theight * self.row * 1.5*0.5)]
            # text_coordinates = [int((c.theight * self.row) * 0.5 - message_size[0] * 0.5),
            #                     int((c.twidth * self.column) * 1.25 - message_size[1] * 0.5)]
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

    def play_game(self, player):
        screen = self.visualization_init()
        cplayer = self.fplayer
        last_move_H = []
        last_move_C = []
        # player = Player()
        while not self.end:
            if cplayer == 'H':
                pos = self.human_turn()
                Hpos = pos
                last_move_H.append(Hpos)
            elif cplayer == 'C':
                # TODO implement smart move
                #####
                player.update_config(self.board)
                row1, col1 = next_move(self.board, player)
                add_element(row1, col1, 0, self.board)
                last_move_C.append((row1, col1))
                #####
                # pos = self.human_turn()
                pos = (row1, col1)
                Cpos = pos
            self.board[pos[0]:, pos[1]:] = 0

            self.select(pos, cplayer, screen)

            self.display(screen)
            self.winning_condition(pos, cplayer, screen)
            ###
            if self.end and cplayer == 'C':
                player.punish(last_move_H)
                player.reward(last_move_C, 'win')
            ###
            if cplayer == 'C':
                cplayer = 'H'
            elif cplayer == 'H':
                cplayer = 'C'
        pygame.quit()


def win(position):
    if position[0] == 0 and position[1] == 0:
        return True


def play_games(player1, player2, size, num_of_games=1):
    for i in range(num_of_games):
        array = np.full((size, size), fill_value=1, dtype=int)
        play_computers(array, player1, player2)


def play_computers(array, player1, player2):
    last_move1 = []
    last_move2 = []
    move_1 = 0
    # move_2 = 0
    while True:
        # print(array)
        # Player 1
        # Check the current configuration and the next possible move
        # print("Before",player1.config)
        player1.update_config(array)
        # print("After",player1.config)
        # print(move_1)
        move_1+=1
        row1, col1 = next_move(array, player1)
        add_element(row1, col1, 0, array)
        last_move1.append((row1, col1))
        if win((row1, col1)):
            # print(array)
            print(f'{player1.name} wins')
            player2.games_won += 1
            player1.games_lost += 1
            ##################
            # Punish Player 2 by removing the last element from it's configuration
            # print(len(player1.stack_configs), len(last_move1))
            player1.punish(last_move1)
            player2.reward(last_move2, 'win')
            break

        # Player 2
        # Check the current configuration and the next possible move
        player2.update_config(array)
        # print(move_1)
        move_1 += 1
        row2, col2 = next_move(array, player2)
        add_element(row2, col2, 1, array)
        last_move2.append((row2, col2))
        if win((row2, col2)):
            player1.games_won += 1
            player2.games_lost += 1
            print(f'{player2.name} wins')
            # print(array)
            ##################
            # Punish Player 1 by removing the last element from it's configuration
            # print(len(player2.stack_configs), len(last_move2))
            player2.punish(last_move2)
            player1.reward(last_move1, 'win')
            break


def possible_moves(array):
    rows, cols = np.where(array == 1)
    possible = []
    for r, c in zip(rows, cols):
        if (r,c) != (0,0):
            possible.append((r, c))
    return possible if len(possible)>0 else [(0, 0)]


def next_move(array, player=None):
    # print(len(player.player_possible_moves(array)))
    if player:
        x = player.player_possible_moves(array)
        if len(x)!=0: # no choice which means that the player has lost
            return random.choice(x)
        else:
            return (0,0)
    else:
        return random.choice(possible_moves(array))


def add_element(row, col, element, array):
    array[row, col] = element
    array[row:, col:] = 0


class Player:
    def __init__(self, name, dumb=False):
        self.config = {}
        self.stack_configs = []
        # self.move = move
        self.games_won = 0
        self.games_lost = 0
        self.games_drawn = 0
        self.dumb = dumb
        self.name = name

    def update_config(self, array1):
        temp = tuple(array1.flatten())
        self.stack_configs.append(temp)
        if temp not in self.config:
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
                if (r,c) in self.config[last_config]:
                    self.config[last_config].remove((r, c))
        self.stack_configs = []

    def reward(self, last_move, win_draw):
        if not self.dumb:
            for i in range(len(last_move)):
                r, c = last_move[i]
                last_config = self.stack_configs[i]
                if win_draw == 'win':
                    ####
                    #remove all the other moves and replace with the winning move
                    # self.config[last_config]
                    ####
                    self.config[last_config].append((r, c))
                    self.config[last_config].append((r, c))
                    self.config[last_config].append((r, c))
                elif win_draw == 'draw':
                    self.config[last_config].append((r, c))
        self.stack_configs = []


# player1 = Player('player1')
# player2 = Player('player2',dumb=True)

player1 = pickle.load(open("player1.pkl", "rb"))
player2 = pickle.load(open("player2.pkl", "rb"))
print('games1',player1.games_won)
print('games2',player2.games_won)
play_games(player2, player1, 9, 100000)

#Save the config of the players
pickle.dump(player1, open("player1.pkl", "wb"))
pickle.dump(player2, open("player2.pkl", "wb"))
game = ChompGame(18,18,'H')
game.play_game(player2)
