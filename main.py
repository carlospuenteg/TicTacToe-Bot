import random
import os

######################################################################

wins = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [3,5,7] ]

######################################################################

def play():
    global won, lost
    locations = [0,1,2,3,4,5,6,7,8]
    game = []

    for i in range(9): # 9 are the max turns
        winLocs = []
        lostLocs = []

        if i % 2:  # If it's AI's turn
            for w in won:
                if  w[:i] == game  and  len(w) > i  and  w[i] not in winLocs:
                    winLocs.append(w[i])

            for l in lost:
                if  l[:i] == game  and  len(l) > i  and  l[i] not in lostLocs:
                    lostLocs.append(l[i])
            
            winLocs = [x for x in winLocs if x not in lostLocs and x in locations]

            if winLocs:
                r = random.choice(winLocs)
                game.append(r)
                locations.remove(r)
            else:
                locs = [x for x in locations if x not in lostLocs]
                if locs:
                    r = random.choice(locs)
                else:
                    r = random.choice(locations)
                game.append(r)
                locations.remove(r)

        else:
            r = random.choice(locations)
            game.append(r)
            locations.remove(r)

        player1 = game[0::2]
        player2 = game[1::2]
        
        for w in wins:
            if all(elem in player1 for elem in w):
                if game not in won:
                    won.append(game)
                return 1
            elif all(elem in player2 for elem in w):
                if game not in lost:
                    lost.append(game)
                return 0

    return 0

######################################################################

def train():
    global won, lost
    createFiles()

    totalWins = 0
    won = eval(open("won.txt", "r").read())
    lost = eval(open("lost.txt", "r").read())

    for t in range(times):
        totalWins += play()

    wonFile = open("won.txt", "w")
    wonFile.write(str(won))
    wonFile.close()

    lostFile = open("lost.txt", "w")
    lostFile.write(str(lost))
    lostFile.close()

    return totalWins

######################################################################

def createFiles():
    if "won.txt" not in os.listdir(os.getcwd()):
        wonFile = open("won.txt", "w")
        wonFile.write("[]")
        wonFile.close()

    if "lost.txt" not in os.listdir(os.getcwd()):
        lostFile = open("lost.txt", "w")
        lostFile.write("[]")
        lostFile.close()

######################################################################

for _ in range(1000):
    print(train(100))