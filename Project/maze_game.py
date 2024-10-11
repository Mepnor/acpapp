import os
from maze import *
import pygame
from pygame.locals import *
import MAIN_VALUE

SCREEN_WIDTH_SETTING = MAIN_VALUE.SCREEN_SETTING_size()[0]
SCREEN_HIGHT_SETTING = MAIN_VALUE.SCREEN_SETTING_size()[1]
WINSIZE = (SCREEN_WIDTH_SETTING, SCREEN_HIGHT_SETTING)
# Assuming you want a fixed size grid for demonstration
tile_size = MAIN_VALUE.tile_size()
grid_rows = int(MAIN_VALUE.SCREEN_SETTING_size()[1] // tile_size)
grid_cols = int(MAIN_VALUE.SCREEN_SETTING_size()[0] // tile_size)

def draw_maze(screen):
    maze = Maze(WINSIZE)
    maze.generate(screen, True)

def check_color_at_position(screen, pos):
    pixel_array = pygame.PixelArray(screen)
    color = pixel_array[pos[0], pos[1]]
    pixel_array.close()  # Close the PixelArray to avoid memory leaks
    return color

def main():
    pygame.init()
    scr_inf = pygame.display.Info()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{}, {}'.format(scr_inf.current_w // 2 - WINSIZE[0] // 2,
                                                         scr_inf.current_h // 2 - WINSIZE[1] // 2)
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Maze')
    screen.fill((0, 0, 0))

    clock = pygame.time.Clock()
    b = draw_maze(screen)

    run = True
    grid = [[0 for i in range(grid_rows)] for i in range(grid_cols)]
    while run:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                
        for wall in range(0, grid_rows):
            for walls in range(0, grid_cols):
                grid_y = (wall * tile_size) 
                grid_x = (walls * tile_size)
                if check_color_at_position(screen, [grid_x, grid_y]) == 0:
                    grid[walls][wall] = 1
            text = ''
            openfile = open('Maze.txt', 'w')
            for row in grid:
                text = "".join(map(str, row))
                openfile.write(text + '\n')
        pygame.display.update()
        clock.tick()
        run = False

if __name__ == '__main__':
    main()