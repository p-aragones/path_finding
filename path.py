import pygame as pg
import random
import sys

window_w = 800
window_h = 800
col = 20
row = 20
#init grid
grid = [[None for i in range(col)] for j in range(row)]
visited = [[None for i in range(col)] for j in range(row)]
#give each node an id
id = 0
for i in range(col):
    for j in range(row):
        grid[i][j] = id
        id += 1

class Cell():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.id = value
        self.printed = 0
    def print(self, surface, window):
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (0, 190, 0), sqr)
        self.printed = 1
    def unprint(self, surface, window):
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (0, 0, 0), sqr)
        self.printed = 0
    def g(self, i, j, start): #distance from current node to start node
        return (i - start[0] + j - start[1])
    def h(self, i, j, end): #heuristic - distance from node to end node
        return (pow(i - start[0], 2) + pow(j - start[1], 2))

def run_program(start, finish):
    pass

def handle_input(surface, window):
    run = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                start, finish = random_cell(surface, window)
                run = 1
            if run == 1 and event.key == pg.K_RETURN:
                run_program(start, finish)

def draw_grid(surface, window):
    blockSize = int(window_h / col)
    for x in range(window_w):
        for y in range(window_h):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pg.draw.rect(surface, (255, 255, 255), rect, 1)

def random_cell(surface, window):
    r_x1 = random.randint(0, row-1)
    r_y1 = random.randint(0, col-1)
    r_x2 = random.randint(0, row-1)
    r_y2 = random.randint(0, col-1)

    for i in range(col):
        for j in range(row):
            if grid[i][j].printed == 1:
                grid[i][j].unprint(surface, window)
    
    grid[r_x1][r_y1].print(surface, window)
    grid[r_x2][r_y2].print(surface, window)
    #grid[0][0].print(r_x1, r_y1, surface, window)
    #grid[0][0].print(r_x2, r_y2, surface, window)
    return (r_x1, r_y1), (r_x2, r_y2)
#create cells with their value
for i in range(col):
    for j in range(row):
        grid[i][j] = Cell(i, j, grid[i][j])
def main():
    pg.init()
    pg.display.set_caption('PATH FINDER')
    window = pg.display.set_mode((window_w, window_h), 0, 32)
    surface = pg.Surface(window.get_size())
    surface = surface.convert()
    clock = pg.time.Clock()
    clock.tick(60)
    while True:
        handle_input(surface, window)
        draw_grid(surface, window)
        window.blit(surface, (0, 0))
        pg.display.update()
        

if __name__ == "__main__":
    main()