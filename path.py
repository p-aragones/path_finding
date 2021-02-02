import pygame as pg
import random
import sys

class Cell():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.id = value
        self.printed = 0
    def print(self, surface, window): #print green sqr in grid
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (0, 190, 0), sqr)
        self.printed = 1
    def unprint(self, surface, window): #unprint sqr from grid
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (0, 0, 0), sqr)
        self.printed = 0
    def g(self, start): #distance from current node to start node
        return (self.x - start[0] + self.y - start[1])
    def h(self, end): #heuristic - distance from current node to end node
        return (pow(self.x - start[0], 2) + pow(self.y - start[1], 2))
    def f(self, start, end): #total cost of the node
        return (self.g(start) + self.h(end))

window_w = 800 #window size
window_h = 800
col = 10 #col and row should be equal (needs to be a square)
row = 10

#init grid and lists
grid = [[None for i in range(col)] for j in range(row)]
openList = [[None for i in range(col)] for j in range(row)] #nodes not visited
closedList = [[None for i in range(col)] for j in range(row)] #already visited nodes

#give each node an id
id = 0
for i in range(col):
    for j in range(row):
        grid[i][j] = id
        id += 1

#create cells with their value
for i in range(col):
    for j in range(row):
        grid[i][j] = Cell(i, j, grid[i][j])

def get_path(start, finish): #compute and print path from start to end
    pass

def handle_input(surface, window):
    run = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: #generate new map
                start, end = random_cell(surface, window)
                run = 1
            if run == 1 and event.key == pg.K_RETURN: #find path from current generated path
                get_path(start, end)

def draw_grid(surface, window): #draw grid lines
    blockSize = int(window_h / col)
    for x in range(window_w):
        for y in range(window_h):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pg.draw.rect(surface, (255, 255, 255), rect, 1)

def random_cell(surface, window): #generate two random spawning cells
    r_x1 = random.randint(0, row-1)
    r_y1 = random.randint(0, col-1)
    r_x2 = random.randint(0, row-1)
    r_y2 = random.randint(0, col-1)

    for i in range(col): #unprint previous sqrs from grid before drawing in the new ones
        for j in range(row):
            if grid[i][j].printed == 1:
                grid[i][j].unprint(surface, window)
    
    grid[r_x1][r_y1].print(surface, window) #print new sqrs in grid
    grid[r_x2][r_y2].print(surface, window)
    return (r_x1, r_y1), (r_x2, r_y2) #return current starting and ending cells' position

def main():
    pg.init()
    pg.display.set_caption('PATH FINDER') #window name
    window = pg.display.set_mode((window_w, window_h), 0, 32) #window mode
    surface = pg.Surface(window.get_size())
    surface = surface.convert()
    clock = pg.time.Clock()
    clock.tick(60)
    while True: #main loop
        handle_input(surface, window)
        draw_grid(surface, window)
        window.blit(surface, (0, 0))
        pg.display.update()

if __name__ == "__main__":
    main()