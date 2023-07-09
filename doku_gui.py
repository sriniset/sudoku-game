from sudoku import Doku
import pygame
import time
pygame.font.init()

class Board:

    #the board object from the doku class
    board = Doku(65)


    #initializer
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.boxes = [[Box(self.board.get(i, j), i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.show_help = False

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board.get(i,j) == 0:
                    self.boxes[i][j].orig = False
                else:
                    self.boxes[i][j].orig = True

    #need method to check if all spots on board are valid after placing a number on the board
    def check_valid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                valid = self.board.is_valid(self.board.get(i,j), i, j)
                if valid:
                    self.boxes[i][j].valid = True
                elif not valid:
                    self.boxes[i][j].valid = False

    #draws the board onto the window
    def draw(self, win):
        space = self.width/9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0,0,0), (0, i*space), (self.width, i*space), thickness)
            pygame.draw.line(win, (0,0,0), (i*space, 0), (i*space, self.height), thickness)
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw(win)
        if self.selected and self.boxes[self.selected[0]][self.selected[1]].orig is False:
            x = self.selected[1] * space
            y = self.selected[0] * space
            grey = (200, 200, 200)
            s = pygame.Surface((space, space))
            s.set_alpha(128)
            s.fill(grey)
            win.blit(s, (x, y))
        if self.selected and self.show_help:
            vals = "valid values: " + str(self.board.get_valid_at(self.selected[0], self.selected[1])).replace('[', '').replace(']','')
            font = pygame.font.SysFont("comicsans", 20)
            text = font.render(vals, 1, (0,0,0))
            win.blit(text, (50, 560))



    #selects a cell on the board, and deselects everything else
    def select(self, row, col):
        if self.boxes[row][col].orig is True:
            return
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selected = False
        self.boxes[row][col].selected = True
        self.selected = (row, col)

    #turns the click position on the board into coordinates
    def get_click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            space = self.width/9
            x = pos[0] // space
            y = pos[1] // space
            return int(y), int(x)
        else:
            return None


    def place(self, val, row, col):
        valid = self.board.is_valid(val, row, col)
        if valid and not self.boxes[row][col].orig:
            self.board.place_num(val, row, col)
            self.boxes[row][col].set(val)
            self.boxes[row][col].valid = True
        elif not valid and not self.boxes[row][col].orig:
            self.board.place_num(val, row, col)
            self.boxes[row][col].set(val)
            self.boxes[row][col].valid = False
        self.check_valid()

    def solve_board(self):
        spot = self.board.find_empty()
        if spot is False:
            return True
        row = spot[0]
        col = spot[1]
        for num in range(1,10):
            if self.board.is_valid(num, row, col):
                board.place(num, row, col)
                if self.solve_board():
                    return True
                else:
                    board.place(0, row, col)
        return False

    def clear(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].orig:
                    continue
                elif not self.boxes[i][j].orig:
                    self.place(0, i, j)

class Box:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.orig = False
        self.valid = True


    def draw(self, window):
        font = pygame.font.SysFont("comicsans", 40)
        space = self.width/9
        x = self.col * space
        y = self.row * space
        if self.orig:
            text = font.render(str(self.value), 1, (0,0,0))
            window.blit(text, (x + (space / 2 - text.get_width() / 2),
                               y + (space / 2 - text.get_height() / 2)))
        else:
            if self.value == 0:
                text = font.render("", 1, (0, 0, 0))
                window.blit(text, (x + (space / 2 - text.get_width() / 2),
                                   y + (space / 2 - text.get_height() / 2)))
            if self.valid and self.value != 0:
                text = font.render(str(self.value), 1, (0, 0, 0))
                if board.show_help:
                    text = font.render(str(self.value), 1, (0, 255, 0))
                window.blit(text, (x + (space / 2 - text.get_width() / 2),
                            y + (space / 2 - text.get_height() / 2)))
            elif not self.valid and self.value != 0:
                text = font.render(str(self.value), 1, (0, 0, 0))
                if board.show_help:
                    text = font.render(str(self.value), 1, (255, 0, 0))
                window.blit(text, (x + (space / 2 - text.get_width() / 2),
                                   y + (space / 2 - text.get_height() / 2)))

    def set(self, val):
        self.value = val

def redraw(win, board):
    win.fill((255,255,255))
    board.draw(win)


if __name__ == "__main__":
    run = True
    start = time.time()
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku!")
    font = pygame.font.SysFont('arial', 32)
    board = Board(9, 9, 540, 540)
    board.show_help = False
    key = None
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    key = None
                    board.clear()
                if event.key == pygame.K_SPACE:
                    key = None
                    board.clear()
                    board.solve_board()
                if event.key == pygame.K_h:
                    if(board.show_help):
                        board.show_help = False
                    else:
                        board.show_help = True
                    
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if board.get_click(pos):
                    board.select(board.get_click(pos)[0], board.get_click(pos)[1])
                    key = None

        #this sets the node to the key based on the boxes method set, we want it to work based on the actual board class
        if board.selected and key is not None:
            board.place(key, board.selected[0], board.selected[1])

        redraw(window, board)
        pygame.display.update()



pygame.quit()