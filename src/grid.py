from src.cell import *

def draw_grid(surface, window): #draw grid lines
    blockSize = int(window_h / col)
    for x in range(window_w):
        for y in range(window_h):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pg.draw.rect(surface, (255, 255, 255), rect, 1)

def random_cell(surface, window): #generate two random spawning cells
    global openList
    global closedList
    global path
    r_x1 = random.randint(0, row-1)
    r_y1 = random.randint(0, col-1) #random x and random y for start and end points
    r_x2 = random.randint(0, row-1)
    r_y2 = random.randint(0, col-1)

    while (r_x1 == r_x2 or r_y1 == r_y2): #checks if both points have been createed in the same place
        r_x2 = random.randint(0, row-1)
        r_y2 = random.randint(0, col-1)

    for i in range(col):
        for j in range(row):
            grid[i][j].unprint(surface, window)
            grid[i][j] = Cell(i, j)

    openList = []
    closedList = []
    path = []

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