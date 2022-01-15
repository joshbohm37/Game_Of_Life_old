import math
import sys

import pygame
from pygame.locals import *
from cell import Cell
from grid import gen_grid

from sys import exit

pygame.init()

vec = pygame.math.Vector2

resolution = pygame.display.Info()
screen = pygame.display.set_mode((resolution.current_w, resolution.current_h), flags=pygame.FULLSCREEN|pygame.SCALED)

screen_w = screen.get_width()
screen_h = screen.get_height()

FPS = 60
clock = pygame.time.Clock()

grid_size = 75
grid_padding = 1
cell_size = (screen_h//grid_size)//2
grid_width = ((grid_size - 1) * (cell_size + grid_padding)) + cell_size
global_center = (screen_w/2, screen_h/2)
grid_top_left = ((global_center[0] - (grid_width/2)), (global_center[1] - (grid_width/2)))

# print(f'cell_size = {cell_size}')


def quit():
    pygame.quit()
    sys.exit()


def draw(entity):
    screen.blit(entity.surf, entity.rect)


rect_group = pygame.sprite.Group()


starting_grid = gen_grid(grid_size)


def draw_grid_sprites(size, grid):
    padding = grid_padding
    grid_w = ((grid_size - 1) * (cell_size + padding)) + cell_size
    center = (screen_w/2, screen_h/2)
    top_left = ((center[0] - (grid_w/2)), (center[1] - (grid_w/2)))

    # print(f'grid_w = {grid_w}')
    # print(f'center = {center}')
    # print(f'top_left = {top_left}')

    for entity in rect_group:
        entity.kill()

    for row in range(size):
        for col in range(size):
            position = (
                top_left[0] + ((cell_size + padding) * col),
                top_left[1] + ((cell_size + padding) * row)
            )

            cell = Cell(start_pos = position, state = grid[row][col], cell_size = cell_size)
            rect_group.add(cell)



draw_grid_sprites(grid_size, starting_grid)

# starting_grid = gen_grid_sprites(grid_size)


def validate_neighbors(grid, size, cell_row, cell_col):
    valid_neighbors = []
    for row in [-1, 0, 1]:
        for col in [-1, 0 , 1]:
            neighbor_col = cell_col + col
            neighbor_row = cell_row + row


            valid = True

            if neighbor_col < 0 or neighbor_col >= size or neighbor_row < 0 or neighbor_row >= size or (cell_row == neighbor_row and cell_col == neighbor_col):
                valid = False

            if valid:
                valid_neighbors.append(grid[neighbor_row][neighbor_col])

    return sum(valid_neighbors)




def update_grid(strt_grd):
    new_grid = []
    for row in range(len(strt_grd)):
        tmp_row = []
        for col in range(len(strt_grd[row])):
            score = validate_neighbors(strt_grd, grid_size, row, col)

            if not strt_grd[row][col]:
                if score == 3:
                    tmp_row.append(1)
                else:
                    tmp_row.append(0)

            else:
                if score < 2:
                    tmp_row.append(0)
                if score > 3:
                    tmp_row.append(0)
                if score == 2 or score == 3:
                    tmp_row.append(1)

        new_grid.append(tmp_row)

    return  new_grid


new_generation = pygame.USEREVENT + 1
generation_time = 50
pygame.time.set_timer(new_generation, generation_time)

PAUSE = True

while True:
    screen.fill((128, 128, 128))

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
        if not PAUSE:
            if event.type == new_generation:
                starting_grid = update_grid(starting_grid)
                draw_grid_sprites(grid_size, starting_grid)

        if PAUSE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for entity in rect_group:
                    if entity.check_click(event.pos):
                        # print(f'Cell clicked!\nCell topleft is {entity.rect.topleft}\nGrid topleft is {grid_top_left}\nCell size is {cell_size}\nPadding is {grid_padding}')
                        cellrow = math.ceil((entity.rect.topleft[1] - grid_top_left[1])/(cell_size + grid_padding))
                        cellcol = math.ceil((entity.rect.topleft[0] - grid_top_left[0])/(cell_size + grid_padding))
                        print(f'Cell clicked: starting_grid[{cellrow}][{cellcol}]\nCell data: {starting_grid[cellrow][cellcol]}')
                        if starting_grid[cellrow][cellcol] == 1:
                            entity.surf.fill((0,0,0))
                            starting_grid[cellrow][cellcol] = 0
                        elif starting_grid[cellrow][cellcol] == 0:
                            entity.surf.fill((255,255,255))
                            starting_grid[cellrow][cellcol] = 1


    for entity in rect_group:
        draw(entity)

    pygame.display.update()
    clock.tick(FPS)

#This is another test

