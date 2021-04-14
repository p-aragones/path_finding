#!/usr/bin/python3

from src.cell import *
from src.algo import *
from src.grid import *

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
                start, end = random_cell(surface, window)
                print("NEW MAP GENERATED")
                run = 1
            if run == 1 and event.key == pg.K_RETURN: #find path from current generated path
                print("FINDING PATH...")
                run = 0
                path = get_path(start, end, surface, window)
                print("PATH FOUND")

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
