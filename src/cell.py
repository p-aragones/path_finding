import pygame as pg
import random
import math
import sys

class Cell():
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.printed = 0
        self.walkable = 1
        self.parent = parent
        self.position = (x, y)
        self.g = 0
        self.h = 0
        self.f = 0
    def print(self, surface, window): #print green sqr in grid (start and end)
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (0, 190, 0), sqr)
        self.printed = 1
    def print_wall(self, surface, window): #print blue sqr in grid (wall)
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (31, 133, 183), sqr)
        self.printed = 1
        self.walkable = 0
    def print_path(self, surface, window): #print orange sqr in grid (path)
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (255, 100, 32), sqr)
        self.printed = 1
        self.walkable = 0
    def unprint(self, surface, window): #unprint sqr from grid
        sqr = pg.Rect(self.x * int(window_w/col), self.y * int(window_h/row), int(window_w/col), int(window_h/row))
        pg.draw.rect(surface, (0, 0, 0), sqr)
        self.printed = 0
        self.walkable = 1
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
    def comp_g(self, start): #distance from current node to start node
        return (self.x - start[0] + self.y - start[1])
    def comp_h(self, end): #heuristic - distance from current node to end node
        return (math.sqrt(pow(self.x - end[0], 2) + pow(self.y - end[1], 2)))
    def comp_f(self, start, end): #total cost of the node
        return (self.comp_g(start) + self.comp_h(end))

window_w = 800 #window size
window_h = 800
col = 20 #col and row should be equal (needs to be a square)
row = 20
run = 0

openList = [] #nodes not visited
closedList = [] #already visited nodes
path = [] #path when end node is found

#init grid and lists
grid = [[None for i in range(col)] for j in range(row)]
start = (0, 0)
end = (0, 0)

#create cells with their value
for i in range(col):
    for j in range(row):
        grid[i][j] = Cell(i, j)