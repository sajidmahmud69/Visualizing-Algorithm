import pygame
import random
from Cell import Cell

"""
PRO TIP: For WIDTH and ROWS use some integer where WIDTH can be divided by ROWS without any remainder
"""

# pygame initialization
pygame.init()
WIDTH = 800             # window resolution
WIN = pygame.display.set_mode ((WIDTH, WIDTH))
clock = pygame.time.Clock()
pygame.display.set_caption ("Maze Builder")

# constants
ROWS = 20               # number of ROWS in the grid
COLS = ROWS             # number of COLS in the grid (it's a square board so COLS = ROWS)

# color constants
WHITE = (255, 255, 255)
PURPLE = (102, 0, 204)


def make_grid (n_rows, n_cols):
    # make all the cells for the grid using a loop
    # for some arbitrary rows there should be arbitrary number of cols
    """
    Make a 2d array  of cell objects
    params:
        n_rows: number of rows the grid should have
        n_cols: number of cols the grid should have
    
    output:
        return the 2d list of grid
    """
    
    grid = []                           # 2d array to contain the grid
    for i in range (n_rows):
        grid.append ([])
        for j in range (n_cols):
            row = i
            col = j
            width = WIDTH // n_rows           # width of individual cell
            cell = Cell (row, col, width)
            grid[i].append (cell)

    return grid

GRID = make_grid (ROWS, COLS)


# draw the vertical and horizontal lines for the grid
def draw_gridlines (win, grid):

    """
    This method uses the cell object to check if the cell has a wall and if they do 
    then draw the corresponsing top, bottom, left and right wall line individually
    """
    line_color = WHITE
    
    for row in grid:
        for cell in row:
            cell_width = cell.width

            # draw the top wall
            if cell.walls['top']:
                pygame.draw.line (win, line_color, (cell.x, cell.y), (cell.x + cell_width, cell.y))

            # draw the bottom wall
            if cell.walls['bottom']:
                pygame.draw.line (win, line_color, (cell.x, cell.y + cell_width), (cell.x + cell_width, cell.y + cell_width))

            # draw the left wall
            if cell.walls['left']:
                pygame.draw.line (win, line_color, (cell.x, cell.y), (cell.x, cell.y + cell_width))

            # draw the right wall
            if cell.walls['right']:
                pygame.draw.line (win, line_color, (cell.x + cell_width, cell.y), (cell.x + cell_width, cell.y + cell_width))

            
            # draw the current cell with a purple color
            # current_cell = grid[3][0]
            # current_cell.visited = True
            # if current_cell.visited:
            #     pygame.draw.rect (win, PURPLE, (current_cell.y + 1, current_cell.x + 1, current_cell.width - 2, current_cell.width - 2))        


            # next_cell = grid[4][0]
            # next_cell.check_neighbors(grid)
            # print(len (next_cell.neighbors))
            # pygame.quit()

def draw_cell(win, cell):
    """
    Draw a single cell if it's marked as visited
    params:
        win: the pygame window to draw on
        cell: a cell object that will be drawn on the window   
    """


    if cell.visited:
         pygame.draw.rect (win, PURPLE, (cell.y + 1, cell.x + 1, cell.width - 2, cell.width - 2))




# make a current cell
current_cell = GRID[0][0]
current_cell.visited = True
next_cell = None


# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draw the gridlines
    draw_gridlines(WIN, GRID)
    draw_cell (WIN, current_cell)

    # if current_cell has neighbors get a random neighbor
    if len (current_cell.check_neighbors (GRID)) > 0:
        next_cell = random.choice(current_cell.check_neighbors(GRID))

    if next_cell is not None:
        next_cell.visited = True
        current_cell = next_cell



    pygame.display.flip()
    clock.tick (15)

pygame.quit()