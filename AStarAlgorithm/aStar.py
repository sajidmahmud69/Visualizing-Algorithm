import pygame
import math
from queue import PriorityQueue

pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode ((WIDTH, WIDTH))
clock = pygame.time.Clock()
pygame.display.set_caption ("A* Pathfinding Algorithm")         # set the display resolution

# color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE  = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows                        # number of rows in the entire grid
    
    def get_pos (self):
        return self.row, self.col


    def is_closed (self):
        """
        Have we already looked at you or in other words are you a red cell?
        """

        return self.color == RED
    

    def is_open (self):
        """
        Are you a green cell? that means it's good to use
        """
        return self.color == GREEN

    def is_barrier (self):
        """
        Are you black? it means it's a barrier and can't be used for the algorithm
        """
        return self.color == BLACK

    def is_start (self):
        # start node will be orange color
        return self.color == ORANGE

    def is_end (self):
        # end node is TURQUOISE color
        return self.color == TURQUOISE

    def reset (self):
        # change the color back to white 
        self.color = WHITE

    def make_start (self):
        # make the starting cell with ORANGE color
        self.color = ORANGE

    def make_closed (self):
        self.color = RED

    def make_open (self):
        self.color = GREEN

    def make_barrier (self):
        # make the barrier cell with BLACK color
        self.color = BLACK
    
    def make_end (self):
        # make the end cell with TURQUOISE color
        self.color = TURQUOISE

    def make_path (self):
        self.color = BLUE

    def draw (self, win):
        pygame.draw.rect (win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors (self, grid):
        self.neighbors = []
        
        # If the cell you are at is not at the last row and the cell below you is not a barrier
        # then go down to that cell and add it to your neighbors list
        if self.row < self.total_rows - 1 and not grid [self.row + 1][self.col].is_barrier():       # DOWN
            self.neighbors.append (grid[self.row + 1][self.col])

        # If the cell you are at is not at the first row and the cell above you is not a barrier
        # then go up to that cell and add it to your neighbors list
        if self.row > 0 and not grid [self.row - 1][self.col].is_barrier():                         # UP
            self.neighbors.append (grid[self.row - 1][self.col])

        # If the cell you are at is not at the first column and the cell to your left is not a barrier
        # then go left to that cell and add it to your neighbors list
        if self.col > 0 and not grid [self.row][self.col - 1].is_barrier():                         # LEFT
            self.neighbors.append (grid[self.row][self.col - 1])

        # If the cell you are at is not at the last column and the cell to your right is not a barrier
        # then go right to that cell and add it to your neighbors list
        if self.col < self.total_rows - 1 and not grid [self.row][self.col + 1].is_barrier():       # RIGHT
            self.neighbors.append (grid[self.row][self.col + 1])




    def __lt__(self, other):
        return False
    


def h(p1, p2):
    """
    Heuristic function. Calculate the Manhattan distance between p1 and p2
    params:
        p1: point 1 in the grid
        p2: point 2 in the grid
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs (x1 - x2) + abs (y1 - y2)



def reconstruct_path (came_from, current, draw):
    # draw the final path with BLUE color
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()



def a_star_algorithm (draw, grid, start, end):
    count = 0
    open_set = PriorityQueue ()
    
    open_set.put ((0, count, start))        # add the first node with its fscore in Priority Queue
    came_from  = {}                         # what node did this node came from

    g_score = {cell: float ("inf") for row in grid for cell in row}
    g_score[start] = 0                      # g score of start node is Zero
    
    f_score = {cell: float ("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}

    while not open_set.empty():

        # exit the game if someone presses X or quit
        # we need this because outside the game loop this algorithm has its own loop
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit ()

        current  = open_set.get ()[2]               # 2 index stores the node from open set priority queue
        open_set_hash.remove (current)

        # if current == end we found the shortest path
        if current == end:
            # draw the shortest path
            reconstruct_path (came_from, end, draw)
            end.make_end ()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h (neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put ((f_score[neighbor], count, neighbor))
                    open_set_hash.add (neighbor)
                    neighbor.make_open()
        draw ()

        if current != start:
            current.make_closed()

    return False




def make_grid (rows, width):
    grid = []                                          # 2d array
    cell_width = width // rows                         # width of the individual cell
    # that's what grid looks like
    # outer for loop creates some empty list
    # inner for loops fill up those empty list with those cell object
    # grid = [
    #         [cell, cell, cell, cell, cell]
    #         [cell, cell, cell, cell, cell]
    #         [cell, cell, cell, cell, cell]
    #         [cell, cell, cell, cell, cell]
    #         [cell, cell, cell, cell, cell]
    #     ]

    for i in range (rows):
        grid.append ([])
        for j in range (rows):
            cell = Cell (i, j, cell_width, rows)
            grid[i].append (cell)

    return grid


def draw_gridlines (win, rows, width):
    """
    Draw the gridlines
    """
    cell_width = width // rows
    for i in range (rows):
        # draw the horizontal line of every row from one point to another point aka from left to right
        pygame.draw.line (win, GREY, (0, i * cell_width), (width, i * cell_width))    

        for j in range (rows):
            # draw the vertical line for every column from one point to another aka from left to right 
            pygame.draw.line (win, GREY, (cell_width * j, 0), (cell_width * j, width))


def draw (win, grid, rows, width):
    """
    Draw the entire grid
    """
    win.fill (WHITE)                    # fill the screen with WHITE

    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_gridlines (win, rows, width)
    pygame.display.update ()


def get_clicked_pos (pos, rows, width):
    """
    Finds out which cell are we on with the mouse cursor
    """
    cell_width = width // rows
    y, x = pos

    row = y // cell_width
    col = x // cell_width
    
    return row, col


def main(win, width):
    ROWS = 50                                           # 50 rows and 50 cols so cols isn't mentioned explicitly
    grid = make_grid (ROWS, width)                      # generate the 2d array of grid
    start = None                    # start cell
    end  = None                     # end cell

    run = True                      # run the main game loop

    while run:
        draw (win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # once the algorithm starts the user can't change anything and 
            # will only be able to quit the game

            if pygame.mouse.get_pressed ()[0]:
                # 0 is left mouse button
                pos = pygame.mouse.get_pos ()               # get the x,y coordinates of mouse on screen
                row, col = get_clicked_pos(pos, ROWS, width)    # find which row & col the cell is from 
                cell = grid[row][col]

                # if start cell isn't selected make a start cell first
                # then select an end cell

                # select a start cell and make sure it's not the end cell
                if not start and cell != end:
                    start = cell
                    start.make_start ()
                
                # select an end cell and make sure it's not the start cell
                elif not end and cell != start:
                    end = cell
                    end.make_end ()
                
                elif cell != end and cell != start:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed ()[2]:
                # 2 is right mosue button
                pos = pygame.mouse.get_pos ()               # get the x,y coordinates of mouse on screen
                row, col = get_clicked_pos(pos, ROWS, width)    # find which row & col the cell is from 
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)

                    a_star_algorithm (lambda: draw (win, grid, ROWS, width), grid, start, end)

                # if we want to run the game more than once
                if event.key == pygame.K_c:
                    # clear the screen and reset everything
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    
        # Flip the display
        pygame.display.flip()
        clock.tick (0)

    pygame.quit()



if __name__ == '__main__':
    main(WIN, WIDTH)
