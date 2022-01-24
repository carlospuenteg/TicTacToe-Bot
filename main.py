import random
import os
import itertools

######################################################################

posWins = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [2,4,6] ]

def loadFiles():
    global wins, defeats
    if "wins.txt" in os.listdir(os.getcwd()) and "defeats.txt" in os.listdir(os.getcwd()):
        wins = eval(open("wins.txt", "r").read())
        defeats = eval(open("defeats.txt", "r").read())

loadFiles()

######################################################################

def train():
    global wins, defeats
    positions = [0,1,2,3,4,5,6,7,8]
    wins = []
    defeats = []
    perm5 = list(list(tup) for tup in itertools.permutations(positions,5))
    perm6 = list(list(tup) for tup in itertools.permutations(positions,6))
    perm7 = list(list(tup) for tup in itertools.permutations(positions,7))
    perm8 = list(list(tup) for tup in itertools.permutations(positions,8))
    perm9 = list(list(tup) for tup in itertools.permutations(positions,9))
    perms = perm5+perm6+perm7+perm8+perm9

    # [4, 2, 8, 0, 5, 6, 3]

    for p in perms:
        print(p)
        player1 = p[0::2]
        player2 = p[1::2]
        winPer = []
        defPer = []
        for w in posWins:
            if all(elem in player1 for elem in w):
                winPer.append(p)
            elif all(elem in player2 for elem in w):
                defPer.append(p)
        if winPer and not defPer:
            wins.append(p)
        elif defPer and not winPer:
            defeats.append(p) 

    winsF = open("wins.txt", "w")
    winsF.write(str(wins))
    winsF.close()    

    defeatsF = open("defeats.txt", "w")
    defeatsF.write(str(defeats))
    defeatsF.close()   

######################################################################

def play():
    positions = [0,1,2,3,4,5,6,7,8]
    game = []

    for i in range(9):
        if not i % 2:  # If it's AI's turn
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
                    if game[:i] == d[:i]  and  d[i] in positions  and  len(w) >= (i+1):  # [3, 5, 4, 2, 6, 8]
                        defLocs[d[i]] += 1

                for l in range(9):
                    if winLocs[l] > 0  and  defLocs[l] == 0  and  l in positions:
                        locs.append(l)

                if locs:
                    r = random.choice(locs)
                    game.append(r)
                    positions.remove(r)
                    # foundWin = True
                elif not all(v == 0 for v in winLocs):
                    bestChoice = winLocs.index(max(winLocs))
                    game.append(bestChoice)
                    positions.remove(bestChoice)
                else:
                    r = random.choice(positions)
                    game.append(r)
                    positions.remove(r)

        else:
            r = random.choice(positions)
            game.append(r)
            positions.remove(r)

        drawGame(game)

        player1 = game[0::2]
        player2 = game[1::2]
        for w in posWins:
            if all(elem in player1 for elem in w):
                return 1
            elif all(elem in player2 for elem in w):
                return 2
    return 0

######################################################################

def test():
    winsCount = 0
    for _ in range(100):
        if play() == 1:
            winsCount += 1

    return winsCount

######################################################################

def drawGame(game):
    display = ""
    table = [0,0,0,0,0,0,0,0,0]

    for i,x in enumerate(game):
        if not i%2:
            table[x] = 1
        else:
            table[x] = 2
    
    for i in range(3):
        display += "| "
        for j in range(3):
            display += str(table[3*i+j]) + " | "
        display += "\n"

    print(display)

######################################################################     

#train()
print(test())