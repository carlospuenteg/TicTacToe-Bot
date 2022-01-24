import random

######################################################################

wins = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [3,5,7] ]
gamesWon = []
wonNum = 0
data = eval(open("data.txt", "r").read())

######################################################################

def play():
    global gamesWon, wonNum
    found = False
    winner = 0

    game = []
    locations = [0,1,2,3,4,5,6,7,8]

    for i in range(9):
        found = False

        if i%2:  # If AI is playing  0
            if data:
                for x in data:
                    if len(x) > (i+1) and x[:i] == game and x[i] in locations:  # If the AI has a game that started like this, copy it
                        game.append(x[i])
                        locations.remove(x[i])
                        found = True
            if not found:
                r = random.choice(locations)
                game.append(r)
                locations.remove(r)

        else:  # If user is playing
            r = random.choice(locations)
            game.append(r)
            locations.remove(r)
        
        player1 = game[0::2]
        player2 = game[1::2]
        
        for w in wins:
            if all(elem in player1 for elem in w):
                winner = 1
                break
            elif all(elem in player2 for elem in w):
                winner = 2
                break

    if winner == 1:
        wonNum += 1
        #if game not in data and game not in gamesWon:
        gamesWon.append(game)

######################################################################

def train(tries):
    global data, gamesWon
    for _ in range(tries//100):
        gamesWon = []
        data = eval(open("data.txt", "r").read())
        for _ in range(200):
            play()
        
        data += gamesWon
        f = open("data.txt", "w")
        f.write(str(data))
        f.close()

######################################################################

def goodness():
    global data
    data = eval(open("data.txt", "r").read())
    for _ in range(100):
        play()
        
    print(wonNum)

######################################################################

#train(1000000)
goodness()