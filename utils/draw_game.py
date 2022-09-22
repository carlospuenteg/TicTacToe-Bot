def draw_game(game):
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