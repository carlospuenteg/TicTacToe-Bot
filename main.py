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

def play(auto):
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
                    if  (i >= 4) and  (len(d) == (i+2))  and  (d[i] in positions)  and  (game[:i] == d[:i]):  # 100% win
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
            if auto:
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

        drawGame(game)

        player1 = game[0::2]
        player2 = game[1::2]
        for w in posWins:
            if all(elem in player1 for elem in w):
                print("\nAI won\n")
                return 1
            elif all(elem in player2 for elem in w):
                print("\nPlayer won\n")
                return 2
    print("\nIt's a tie\n")
    return 0

######################################################################

def test(nGames):
    winsCount = 0
    defeatsCount = 0
    tieCount = 0
    for tryNum in range(nGames):
        print("Try number " + str(tryNum) + ":")
        result = play(1)
        if result == 1:
            winsCount += 1
        elif result == 2:
            defeatsCount += 1
        else:
            tieCount += 1

    print("In " + str(nGames) + " games:")
    print("- Wins: " + str(winsCount))
    print("- Defeats: " + str(defeatsCount))
    print("- Ties: " + str(tieCount))

    '''
    From 10000 games:
    - 9895 won
    - 0 lost
    - 105 tied
    '''

######################################################################

def drawGame(game):
    display = "\n"
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

def menu():
    while True:
        print("\n0. EXIT")
        print("1. Train AI")
        print("2. Test AI")
        print("3. PLAY")

        op = int(input("\nOption: "))

        if op == 0:
            break
        elif op == 1:
            train()
        elif op == 2:
            test(int(input("Number of games to test: ")))
        elif op == 3:
            play(0)

######################################################################

menu()
#train()