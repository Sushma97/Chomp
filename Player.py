import numpy as np
import random

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
            self.config[temp] = self.possible_moves(array1)

    def player_possible_moves(self, array1):
        temp = tuple(array1.flatten())
        if temp not in self.config:
            self.update_config(array1)
        return self.config[temp]

    def punish(self, last_move):
        if not self.dumb:
            for i in range(len(last_move)-1, -1,  -1):
                r, c = last_move[i]
                last_config = self.stack_configs[i]
                # print(len(self.config[last_config]))
                if (r, c) in self.config[last_config]:
                    print("removing {} {}".format((r,c), last_config))
                    self.config[last_config].remove((r, c))
                    break
        self.stack_configs = []

    def reward(self, last_move):
        if not self.dumb:
            for i in range(len(last_move)):
                r, c = last_move[i]
                last_config = self.stack_configs[i]

                ####
                #remove all the other moves and replace with the winning move
                # self.config[last_config]
                ####
                self.config[last_config].add((r, c))
                # self.config[last_config].append((r, c))
                # self.config[last_config].append((r, c))
        self.stack_configs = []

    def possible_moves(self,array):
        rows, cols = np.where(array == 1)
        possible = set()
        for r, c in zip(rows, cols):
            if (r, c) != (0, 0):
                possible.add((r, c))
        return possible if len(possible) > 0 else [(0, 0)]

    def next_move(self, array, player=None):
        # print(len(player.player_possible_moves(array)))
        if player:
            x = player.player_possible_moves(array)
            if len(x) != 0:  # no choice which means that the player has lost
                return random.sample(x, 1)[0]
            else:
                return (0, 0)
        else:
            return random.sample(self.possible_moves(array), 1)[0]