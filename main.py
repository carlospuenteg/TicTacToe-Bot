import random
import os
import itertools

######################################################################

posWins = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [3,5,7] ]
locations = [0,1,2,3,4,5,6,7,8]

######################################################################

def train():
    wins = []
    defeats = []
    perms = [list(itertools.permutations(locations, 6)),list(itertools.permutations(locations, 7)),list(itertools.permutations(locations, 8)),list(itertools.permutations(locations, 9))]

    for perm in perms:
        for p in perm:
            player1 = p[0::2]
            player2 = p[1::2]
            for w in posWins:
                if all(elem in player1 for elem in w):
                    wins.append(p)
                elif all(elem in player2 for elem in w):
                    defeats.append(p)

    winsF = open("wins.txt", "w")
    winsF.write(str(wins))
    winsF.close()    

    defeatsF = open("defeats.txt", "w")
    defeatsF.write(str(defeats))
    defeatsF.close()   

######################################################################

train()