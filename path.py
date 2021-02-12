#!/usr/bin/python3

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

def get_path(start, end, surface, window): #compute and print path from start to end
    global openList
    global closedList
    global path
    global grid
    print(start, end)
    start_node = Cell(start[0], start[1])
    end_node = Cell(end[0], end[1])
    openList.append(start_node)
    current_node = openList[0]
    current_indx = 0
    while len(openList) > 0:
        current_node = openList[0]
        current_indx = 0
        for indx, item in enumerate(openList): #checks openList for available nodes
            if item.f < current_node.f: #node on the list has a better f value than current node
                current_node = item
                current_indx = indx
        openList.pop(current_indx) #delete current node from the open list
        closedList.append(current_node) #add current node to the closed list
        if current_node.position == end_node.position: #reached end cell - finished
            print(current_node.position, end_node.position)
            current = current_node
            while current is not None:
                path.append(current)
                grid[current.position[0]][current.position[1]].print_path(surface, window)
                current = current.parent
            return (path[::-1]) #inversed path
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # cells surrounding current node
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0: #check grid bounds
                continue
            if grid[node_position[0]][node_position[1]].walkable == 0:
                continue
            if Cell(node_position[0], node_position[1], current_node) in closedList:
                continue
            new_node = Cell(node_position[0], node_position[1], current_node)
            children.append(new_node)
        for child in children: #loops through children
            for closed_child in closedList:
                if child == closed_child: #child in the closed list
                    break
            else: #child not closed
                child.g = current_node.g + 1
                child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h
            for open_node in openList:
                if child == open_node and child.g >= open_node.g: #child in openList
                    break
            else:
                openList.append(child) #better node found

def handle_input(surface, window):
    global run
    global start
    global end
    global path
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: #generate new map
                for i in range(col): #unprint previous sqrs from grid before drawing in the new ones
                    for j in range(row):
                        grid[i][j].unprint(surface, window)
                start, end = random_cell(surface, window)
                print("NEW MAP GENERATED")
                run = 1
            if run == 1 and event.key == pg.K_RETURN: #find path from current generated path
                print("FINDING PATH...")
                run = 0
                path = get_path(start, end, surface, window)
                print("PATH FOUND")

def draw_grid(surface, window): #draw grid lines
    blockSize = int(window_h / col)
    for x in range(window_w):
        for y in range(window_h):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pg.draw.rect(surface, (255, 255, 255), rect, 1)

def random_cell(surface, window): #generate two random spawning cells
    r_x1 = random.randint(0, row-1)
    r_y1 = random.randint(0, col-1) #random x and random y for start and end points
    r_x2 = random.randint(0, row-1)
    r_y2 = random.randint(0, col-1)

    while (grid[r_x2][r_y2].printed == 1): #checks if both points have been createed in the same place
        r_x2 = random.randint(0, row-1)
        r_y2 = random.randint(0, col-1)

    for i in range(col): #unprint previous sqrs from grid before drawing in the new ones
        for j in range(row):
            if grid[i][j].printed == 1 or grid[i][j].walkable == 0:
                grid[i][j].unprint(surface, window)

    for i in range(int(col * row / 7)): #% of the map will be covered by obstacles
        rx = random.randint(0, row-1)
        ry = random.randint(0, col-1)
        while (grid[rx][ry].printed == 1): #walls do not spawn on top of eachother
            rx = random.randint(0, row-1)
            ry = random.randint(0, col-1)
        grid[rx][ry].print_wall(surface, window)

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
    run = 0
    while True: #main loop
        handle_input(surface, window)
        draw_grid(surface, window)
        window.blit(surface, (0, 0))
        pg.display.update()

if __name__ == "__main__":
    main()
