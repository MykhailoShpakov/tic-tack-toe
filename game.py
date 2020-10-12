from random import randint

# Define the pattern of possible lines
# e - empty line, num - line that serves to indicate the number of cell if its free, lb - lower border line
patterns = {'e': "\t\t\t|", 'num': "\t  {n}\t\t|", 'x': "\t  X\t\t|", 'o': "\t  O\t\t|", 'lb': " ___________"}

# define the cell, which is combination of lines
# it is more convenient to change the cell than its specific row
e_cell = ['e', 'e', 'num', 'e', 'lb']
x_cell = ['e', 'e', 'x', 'e', 'lb']
o_cell = ['e', 'e', 'o', 'e', 'lb']

# how many lines there are per cell
lpc = 5

# how many cells there are per row
cpr = 3

# how many cells there are per column
cpc = 3

# Board that contains 9 cells
board = [e_cell]
board *= 9

# Indicates symbol inside the cell contained in my board
board_status = ['empty']
board_status *= 9

# true if player won the game or game not started yet
end_game = True


# Asks the cell number and returns the data for cell updating
def readMove(pl):
    print(f"{pl[0]} you are {pl[1]}\nChoose the cell\nHint: Cells are numbered from 1 to 9\n")
    target = 'none'
    while not(target.isdigit() and int(target) in range(1, 10)):
        target = input("I chose cell number: ")

    # return tuple of player`s symbol and number of cell in array, which is less by 1
    out_tp = (pl[1], int(target) - 1)
    return out_tp


# changes the board status
def writeMove(new):
    # Receive tuple consisting of symbol to write into cell and index of this cell

    if board_status[new[1]] == 'empty':
        board_status[new[1]] = new[0]
        return True
    else:
        return False


def updateBoard():
    for ind, mark in enumerate(board_status):
        if mark == 'O':
            board[ind] = o_cell
        elif mark == 'X':
            board[ind] = x_cell


# prints the game board given an array of cells
def printBoard():
    # Lines that i print out to show my board
    # stpc - stop cell, not print it
    # 3 is the stop cell in the first row that i don`t want to print
    for stpc in range(cpr, len(board) + 1, cpr):
        # Get the number of first cell in a row to print them numerated
        cell_num = stpc - cpr + 1

        for l in range(0, lpc):
            # ltp - line to print
            ltp = ""

            for c in board[stpc - cpr: stpc]:

                # get the middle line, the one where numeration of cell is contained
                if l == lpc//2:
                    ltp += patterns[c[l]].format(n=cell_num)
                    cell_num += 1

                else:
                    # get line number l from each cell
                    ltp += patterns[c[l]]

            print(ltp)


# Checks if player won
def checkBoard(sym, num_to_win):

    for row in range(0, cpc):

        for col in range(0, cpr):

            # check if symbol is the one that i search for
            if board_status[row*cpr + col] == sym:

                # define directions that may contain winning combination
                go_row = cpr - col >= num_to_win
                go_col = cpc - row >= num_to_win

                # go in diagonal from left to right
                go_diag_ltr = go_col and go_row

                # go in diagonal from right to left
                go_diag_rtl = go_col and col+1 >= num_to_win

                if go_col:
                    match = True
                    sub_row = row
                    # iterate through current column
                    while (sub_row < row + num_to_win) and match:

                        if board_status[sub_row*cpr + col] != sym:
                            # there is a symbol that breaks the winning combination
                            match = False
                        sub_row += 1

                    if match:
                        return match

                if go_row:
                    match = True
                    sub_col = col
                    # iterate through current row
                    while (sub_col < col + num_to_win) and match:
                        if board_status[row*cpr + sub_col] != sym:
                            # there is a symbol that breaks the winning combination
                            match = False
                        sub_col += 1

                    if match:
                        return match

                if go_diag_ltr:
                    match = True
                    sub_row = row
                    sub_col = col

                    # iterate through current diagonal
                    while (sub_row < row + num_to_win) and (sub_col < col + num_to_win) and match:

                        if board_status[sub_row*cpr + sub_col] != sym:
                            # there is a symbol that breaks the winning combination
                            match = False

                        sub_col += 1
                        sub_row += 1

                    if match:
                        return match

                if go_diag_rtl:
                    match = True
                    sub_row = row
                    sub_col = col
                    # iterate through current diagonal in opposite verse
                    while (sub_row < row + num_to_win) and (sub_col > col - num_to_win) and match:
                        if board_status[sub_row * cpr + sub_col] != sym:
                            # there is a symbol that breaks the winning combination
                            match = False

                        sub_col -= 1
                        sub_row += 1

                    if match:
                        return match

    # Never found a winning combination
    return False


# executes game actions
print("Welcome to TIC-TAC_TOE game !\n")
symbols_set = ['X', 'O']

# define the array of tuples = (name, symbol)
name1 = input("Player 1, what`s your name?: ")
name2 = input("Player 2, what`s your name?: ")

# if even starts the first player, if odd starts the second player
if not randint(0, 10) % 2 == 0:
    # The second player won and he starts the game, so becomes the first one
    tmp = name1
    name1 = name2
    name2 = tmp

print(name1 + " you start\nInsert the symbol that you want to play for")
sym = 'empty'

# Doesnt accept the players symbol unless it is X or O
while not (sym == 'X' or sym == 'O'):
    sym = input(f"Write only {symbols_set[0]} or {symbols_set[1]}: ").upper()

# Assign first player`s data to the first tuple, because he starts
pl1 = (name1, sym)

# Assign second player`s data to the second tuple
symbols_set.remove(sym)
pl2 = (name2, symbols_set[0])

# Create array of game members
players = [pl1, pl2]

# Showing chosen symbols for each name
for n, s in players:
    print(f"{n} - {s}")

print("\nAre you ready ?")
if input("Type yes or no: ").upper() == 'YES':

    # game process
    end_game = False
    move_num = 0
    move_correct = False
    clear = 200*'\n'

    while not end_game:
        print(clear)
        printBoard()
        # move num is even then i pass data of 1 player, otherwise of 2 player
        up_cell = readMove(players[move_num % 2])
        move_correct = writeMove(up_cell)
        while not move_correct:
            print("This cell is already filled. Try another one !")
            up_cell = readMove(players[move_num % 2])
            move_correct = writeMove(up_cell)

        updateBoard()

        # Pass the symbol that I want to check for and how many symbols i should have in winning combination
        won = checkBoard(players[move_num % 2][1], 3)
        if won:
            printBoard()
            print(players[move_num % 2][0] + " - " + players[move_num % 2][1])
            print("You won, congratulations !")
            end_game = True

        move_num += 1
        if move_num >= 9:
            end_game = True
            print("Nobody won, you are losers")
else:
    print("Goodbye")
