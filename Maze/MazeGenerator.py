import pygame                       # import for graphics
from random import choice           # chooses a random element from an array

# make constants screen resolution, tile size
# and calculate the number of rows and cols in the board
RESOLUTION = WIDTH, HEIGHT = 800, 800
TILE  = 40
cols, rows = WIDTH//TILE, HEIGHT//TILE

# initialize pygame
pygame.init()
sc = pygame.display.set_mode (RESOLUTION)
clock = pygame.time.Clock()

class Cell:

    # constructor
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.walls  = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    # draw a cell method
    def draw_current_cell (self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect (sc, pygame.Color ('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))


    # draw walls and visited cells
    def draw (self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect (sc, pygame.Color ('black'), (x, y, TILE, TILE))

        # draw the straight lines to set up the boundary
        if self.walls['top']:
            pygame.draw.line (sc, pygame.Color ('darkorange'), (x, y), (x + TILE, y), 3)

        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color ('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 3)

        if self.walls ['bottom']:
            pygame.draw.line(sc, pygame.Color ('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 3)

        if self.walls['left']:
            pygame.draw.line (sc, pygame.Color ('darkorange'), (x, y + TILE), (x, y), 3)

    
    # check cell and get random neighbors
    def check_cell (self, x, y):
        def find_index (x, y):
            return x + y * cols
        
        # invalid index condition
        if x < 0 or x > cols - 1 or y  < 0 or y > rows - 1:
            return False

        return grid_cells [find_index(x, y)]

    
    def check_neighbors (self):
        neighbors = []

        top = self.check_cell (self.x, self.y - 1)
        right = self.check_cell (self.x + 1, self.y)
        bottom = self.check_cell (self.x, self. y + 1)
        left  = self.check_cell (self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append (top)

        if right and not right.visited:
            neighbors.append (right)

        if bottom and not bottom.visited:
            neighbors.append (bottom)

        if left and not left.visited:
            neighbors.append (left)

        return choice (neighbors) if neighbors else False

    

def remove_walls (current, next):
    # dx and dy are relative position of the current cell and the next cell
    dx = current.x - next.x
    dy = current.y  - next.y


    if dx == 1:
        current.walls['left'] = False
        next.walls ['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False






# a list container to hold all the cells
grid_cells = [Cell (col, row) for row in range (rows) for col in range (cols)]
current_cell = grid_cells [0]
stack  = []
colors, color = [], 40




# write the main game loop
running = True
while running:

    # fill the background color
    sc.fill(pygame.Color ('darkslategray'))

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False

    # draw the cell
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    [pygame.draw.rect (sc, colors[i], (cell.x * TILE + 2, cell.y * TILE + 2,
                                       TILE - 4, TILE - 4)) for i, cell in enumerate (stack)]


    next_cell = current_cell.check_neighbors ()
    if next_cell:
        next_cell.visited = True
        stack.append (current_cell)
        colors.append ((min (color, 255), 10, 100))
        color += 1
        remove_walls (current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()


    # flip the display
    pygame.display.flip()
    clock.tick (60)                            # higher means go faster
pygame.quit()



