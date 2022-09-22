import os
import numpy as np
import itertools
import random
from utils.progress_bar import progress_bar
from utils.draw_game import draw_game

#---------------------------------------------------------------

win_positions = np.array(( (0,1,2) , (3,4,5) , (6,7,8) , (0,3,6) , (1,4,7) , (2,5,8) , (0,4,8) , (2,4,6) ))

#---------------------------------------------------------------

def train():
    os.mkdir("analysis")
    positions = np.array((0,1,2,3,4,5,6,7,8))
    wins = []
    defeats = []

    print("Generating all posible combinations...")
    perms = list(perm for i in range(5, 10) for perm in itertools.permutations(positions, i))

    for p in perms:
        player1 = p[0::2] # odd positions
        player2 = p[1::2] # even positions
        winCombs = []
        defCombs = []
        for win_pos in win_positions:
            if all(pos in player1 for pos in win_pos):
                winCombs.append(p)
            elif all(pos in player2 for pos in win_pos):
                defCombs.append(p)
        if winCombs and not defCombs:
            wins.append(p)
        elif defCombs and not winCombs:
            defeats.append(p) 

    np.save("analysis/wins.npy", wins)
    np.save("analysis/defeats.npy", defeats) 

#---------------------------------------------------------------

def loadFiles():
    if "analysis" not in os.listdir(os.getcwd()):
        train()
    return [
        np.load("analysis/wins.npy", allow_pickle=True),
        np.load("analysis/defeats.npy", allow_pickle=True)
    ]

#---------------------------------------------------------------

def play():
    wins, defeats = loadFiles()
    positions = [0,1,2,3,4,5,6,7,8]
    game = []
    wins = [list(x) for x in wins]
    defeats = [list(x) for x in defeats]

    for i in range(9):
        if not i % 2:  # If it's BOT's turn
            foundWin = False
            winLocs = [0,0,0,0,0,0,0,0,0]
            defLocs = [0,0,0,0,0,0,0,0,0]
            locs = []
            for w in wins:
                if  (i >= 4) and  (len(w) == (i+1))  and  (w[i] in positions)  and  (game[:i] == w[:i]):  # 100% win
                    game.append(w[i])
                    positions.remove(w[i])
                    foundWin = True
                    break
                if game[:i] == w[:i]  and  w[i] in positions  and  len(w) >= (i+1):
                    winLocs[w[i]] += 1
            
            if not foundWin:
                for d in defeats:
                    if  (i >= 4) and  (len(d) == (i+2))  and  (d[i] in positions)  and  game[:i] == d[:i]:  # 100% win
                        winLocs[d[i]] = 0
                    if game[:i] == d[:i]  and  d[i] in positions  and  len(w) >= (i+1):  # [4, 6, 0, 8, 2, 7]
                        defLocs[d[i]] += 1

                for l in range(9):
                    if winLocs[l] > 0  and  defLocs[l] == 0  and  l in positions:
                        locs.append(l)

                if locs:
                    r = random.choice(locs)
                    game.append(r)
                    positions.remove(r)
                elif not all(v == 0 for v in winLocs):
                    bestChoice = winLocs.index(max(winLocs))
                    game.append(bestChoice)
                    positions.remove(bestChoice)
                else:
                    r = random.choice(positions)
                    game.append(r)
                    positions.remove(r)

        else:
            while True:
                choice = int(input("\nNew position: "))
                if choice in positions:
                    break
                else:
                    print("\nInvalid position!")
            game.append(choice)
            positions.remove(choice)

        draw_game(game)

        player1 = game[0::2]
        player2 = game[1::2]
        for w in win_positions:
            if all(elem in player1 for elem in w):
                print("\nBOT won\n")
                return 1
            elif all(elem in player2 for elem in w):
                print("\nPlayer won\n")
                return 2
    print("\nIt's a tie\n")
    return 0

#---------------------------------------------------------------

play()