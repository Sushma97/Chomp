import copy

import numpy as np
import Player_variation_2
import pickle

def win(position):
    if position[0] == 0 and position[1] == 0:
        return True


def play_games(player1, player2, row, col, num_of_games=1):
    games_won_1 = 0
    games_won_2 = 0
    for i in range(num_of_games):
        array = np.full((row, col), fill_value=1, dtype=int)
        player_name = play_computers(array, player1, player2)
        if player_name == player1.name:
            games_won_1 += 1
        else:
            games_won_2 += 1
    print(games_won_1, games_won_2)


def play_computers(array, player1, player2):
    last_move1 = []
    last_move2 = []

    while True:
        # print(array)
        # Player 1
        # Check the current configuration and the next possible move
        player1.update_config(array)
        row1, col1 = player1.next_move(array, player1)
        add_element(row1, col1, 0, array)
        last_move1.append((row1, col1))
        if win((row1, col1)):
            # print(array)
            print('Player 2 wins')
            player2.games_won += 1
            player1.games_lost += 1
            ##################
            # Punish Player 2 by removing the last element from it's configuration
            # print(len(player1.stack_configs), len(last_move1))
            player1.punish(last_move1)
            player2.reward(last_move2)
            return player2.name
            # break

        # Player 2
        # Check the current configuration and the next possible move
        player2.update_config(array)
        row2, col2 = player2.next_move(array, player2)
        add_element(row2, col2, 1, array)
        last_move2.append((row2, col2))
        if win((row2, col2)):
            player1.games_won += 1
            player2.games_lost += 1
            print('Player 1 wins')
            # print(array)
            ##################
            # Punish Player 1 by removing the last element from it's configuration
            # print(len(player2.stack_configs), len(last_move2))
            player2.punish(last_move2)
            player1.reward(last_move1)
            return player1.name
            # break


def add_element(row, col, element, array):
    array[row, col] = element
    array[row:, col:] = 0


def initial_train(row, col, size, iter=1000):
    player1 = Player_variation_2.Player('player1', size)
    player2 = Player_variation_2.Player('player2', size, dumb=True)
    play_games(player1, player2, row, col, iter)
    # Save the config of the players
    pickle.dump(player1, open("player1_"+str(row)+"_"+ str(col)+"_"+ str(size)+".pkl", "wb"))


def load_player(row, col, size):
    player = pickle.load(open("player1_"+str(row)+"_"+ str(col)+"_"+ str(size)+".pkl", "rb"))
    return player

def continuous_train(row, col, size, iter=1000):
    try:
        player1 = pickle.load(open("player1_" + str(row) + "_" + str(col) + "_" + str(size) + ".pkl", "rb"))
    except:
        player1 = Player_variation_2.Player('player1', size)
    # player2 = copy.deepcopy(player1)
    # player2.name = "player2"
    player2 = Player_variation_2.Player('player2', size, dumb=True)
    play_games(player1, player2, row, col, iter)
    pickle.dump(player1, open("player1_"+str(row)+"_"+ str(col)+"_"+ str(size)+".pkl", "wb"))


