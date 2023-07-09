# Sudoku Game with CLI
# Author: Srinivas Setty
# Last Edited: 2/12/20
import random
import sys


class Doku:

    #want to maximize board difficulty
    #want such that removing the location will make the board tough by giving a ton of possibilities at that position
    #have ability to see what the number of possibilities at a point are
    def __init__(self, diff):
        self.board = [[0 for i in range(9)] for j in range(9)]
        rand_rows = [random.randrange(0, 9, 1) for i in range(9)]
        rand_cols = [random.randrange(0, 9, 1) for i in range(9)]
        point = 0
        for r, c in zip(rand_rows, rand_cols):
            self.place_num(point, r, c)
            point += 1
        cond = self.solve()
        if cond:
            rand_r = [random.randrange(0, 9, 1) for i in range(diff)]
            rand_c = [random.randrange(0, 9, 1) for i in range(diff)]
            for i, j in zip(rand_r, rand_c):
                self.place_num(0, i, j)

    def print_board(self):
        #prints board of 9x9 into separate 3x3 blocks
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("----------------------")
            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    print('|', end=" ")
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(self.board[i][j], end=" ")

    def find_empty(self):
        #finds the first empty entry in the board
        #empty is represented by 0
        #parses row by row
        #helper function for solve
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j
        return False



    def is_valid(self, num, x, y):
        #checks if board placement is valid based on sudoku game rules

        #rules: number cannot already be in the same row, column, or box
        # if num == 0:
        #     #print("Not valid, input must be numbers 1-9")
        #     return False

        if x > 8 or y > 8 or x < 0 or y < 0:
            #print("Not valid, coordinates must be between 0-8 for 9x9 board")
            return False

        #check row
        for i in range(len(self.board[x])):
            if num == self.board[x][i] and i != y:
                return False

        #check col
        for j in range(len(self.board)):
            if num == self.board[j][y] and j != x:
                return False

        #check box
        a = x // 3
        b = y // 3

        for i in range(3*a, 3*a + 3):
            for j in range(3*b, 3*b + 3):
                if num == self.board[i][j] and i != x and j != y:
                    return False
        return True

    def get_valid_at(self, x, y):
        #returns list of all valid inputs for a point
        #be used as helper for solve
        return [i for i in range(1,10) if self.is_valid(i,x,y) and i != 0]


    def place_num(self, num, x, y):
        #places number at given row and column spot
        #if placement is not valid,
        if self.is_valid(num, x, y):
            self.board[x][y] = num
            return True
        else:
            #print("WARNING: " + str(num) + " is not valid at " + str((x,y)))
            self.board[x][y] = num
            return False

    def is_solved(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return False
        return True

    def get(self, row_num, col_num):
        return self.board[row_num][col_num]

    def solve(self):
        spot = self.find_empty()
        if spot is False:
            return True
        row = spot[0]
        col = spot[1]
        for num in range(1,10):
            if self.is_valid(num, row, col):
                self.place_num(num, row, col)
                if self.solve():
                    return True
                else:
                    self.place_num(0, row, col)
        return False


if __name__ == "__main__":

    board = Doku()

    board.print_board()

    while not board.is_solved():
        print()
        inp = input("Please type your input: ")
        print()
        if inp == "quit":
           sys.exit()
        else:
            n, row, col = inp.split()
        if board.place_num(int(n), int(row), int(col)):
            board.place_num(int(n), int(row), int(col))
            board.print_board()
        else:
            continue