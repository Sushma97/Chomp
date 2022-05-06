# CHOMP

<img width="992" alt="image" src="https://user-images.githubusercontent.com/24721561/165885793-88bb5455-be58-41a5-a555-eac2145dc0b5.png">

Chomp is a two-player strategy game played on a rectangular/Sqaure grid made up of smaller square cells, which can be thought of as the blocks of a chocolate bar. The players take it in turns to choose one block and "eat it" (remove from the board), together with those that are below it and to its right. The top left block is "poisoned" and the player who eats this loses.    

Player A eats two blocks from the bottom right corner; Player B eats three from the bottom row; Player A picks the block to the right of the poisoned block and eats eleven blocks; Player B eats three blocks from the remaining column, leaving only the poisoned block. Player A must eat the last block and so loses.

This is a first player advantage game. We have used Reinforcement learning to make the machine learn to play the game for different board configurations. 

Once the machine has learnt to play the game with more than 50000 games, it is almost impossible to beat it. 

## Original version of the game

In order to play the normal version of the game, run python ChompGame.py. Follow the instructions accordingly. 

<img width="565" alt="image" src="https://user-images.githubusercontent.com/24721561/165887239-45b2f09e-cbab-4b49-a039-30d026e70eb6.png">

Note that if you wish to play against smart computer, you need to train it first. Currently only 5*5 configuration is trained.  
In order to train the a configuration from scratch, use option 2. 
If the model configuration is trained already, use option 3 to train it more. 

#### Learning rate:
<img width="416" alt="image" src="https://user-images.githubusercontent.com/24721561/165888651-f3596868-041a-4f04-8be7-5cdc1baeae9e.png">


### Game Variation 1: Poison block hidden
To play the game variation 1, where the poisonous block is hidden, run python ChompGame_variation_1.py and follow the instructions 
<img width="581" alt="image" src="https://user-images.githubusercontent.com/24721561/165888871-affc3a6d-867b-4bfd-8350-2b07a3d52d07.png">

Note that since this is a game of pure chance, there is no reinforcement training available for the computer. So computer choice is random each time. 


### Game Variation 2: Limit on the number of chocolate blocks we can eat
To play the game variation 2, where the number of chocolate blocks you can eat at once is limited, run python ChompGame_variation_2.py and follow the instructions. 
This game is similar to the original, except for the restriction on the number of blocks. The reinforcement training can be done for this variation of the game. We observed that learning rate is slower with this change for a given configuration and fixing the limit on number of blocks that can be eaten. 
If you try to eat blocks more than the limit, the block will be highlighted red. Currently 6*6 board with limit 3 is trained. For rest of the configuration, training has to be done before playing with smart computer. 

#### Learning rate
<img width="417" alt="image" src="https://user-images.githubusercontent.com/24721561/165890461-d24e3fb9-f1c6-499c-ac61-d6976d686352.png">


### Game variation 3: Poison and antidote
To play the game variation 3, where there are a number of poisoned blocks and antidotes, run python Chomp_Poison_Antidote.py
- This game has hidden poisoned blocks and antidotes in the chocolate, whenever a player picks a poison block he doesn't die or lose immediately.
- As soon as a player eats a poisoned cell a counter called `sustenance` is initiated and it reduced for each subsequent moves. If the player does not
find an antidote within the next moves(`sustenance`) he will lose

#### Instructions
- First instantiate the game `Poison_Antidote(<no_of_rows>,<no_of_cols><'C'/'H'>)`
- 'C' if Computer plays first and 'H' if Human plays first
- run the `play_game()` for the instantiated object

e.g
>game = Poison_Antidote(20,20,'C')\
>game.play_game()


### Big O analysis
#### Time Complexity
- Let's take N as the number of tiles/chocolate pieces on the board
- The program runs for each cell until there are no cells remaining.
- For each turn it calculates the possible moves which is number of remaining cells. O(N)
- It randomly chooses a possible move from this. O(1)
- After winning the game the AI rewards all its winning moves and, thus it goes through every move it has made until that point. O(N)
- All this training runs for a set number of iterations P
- Hence, the time complexity can be written as O(P*(N+N)\*N)->O(P*N^2)

#### Space Complexity
- The training is done by storing the configuration and corresponding possible moves.
- The two main things stored are the config of the board and corresponding possible moves, and the next is the configuration of the board after each move
- The config is a dictionary with key as a flattened array and value as the list of rows & cols
- The config file is a large dictionary file stored as a pickle
- The space complexity is of the order of O(N\*N*P)
- Where P are the number of iterations and N are the number of tiles on the board.

