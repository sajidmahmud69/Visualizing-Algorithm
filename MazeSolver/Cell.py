class Cell:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.neighbors = []
        self.visited = False
        self.color = (0, 0, 0)

    def check_neighbors (self, grid):
        """
        find the cell's left, right, top, and bottom neighbors
        and if they are not visited add it to the neighbors list
        """
        
        # store the top, right, bottom and left neighbor if it's a valid index
        top  = None
        right = None
        bottom = None
        left = None

        if check_valid_index (self.row - 1, self.col, grid):
            top = grid[self.row - 1][self.col]
        
        if check_valid_index (self.row, self.col + 1, grid):
            right = grid[self.row][self.col + 1]
        
        if check_valid_index (self.row + 1, self.col, grid):
            bottom = grid[self.row + 1][self.col]

        if check_valid_index (self.row, self.col - 1, grid):
            left = grid[self.row][self.col - 1]

        


        # if top is not visited and top is not None then the add it to the neighbors list
        if top is not None and not top.visited:
            self.neighbors.append (top)
            print ('Found top')


        # if right is not visited and right is not None then the add it to the neighbors list
        if right is not None and not right.visited:
            self.neighbors.append (right)
            print ('Found right')


        # if bottom is not visited and bottom is not None then the add it to the neighbors list
        if bottom is not None and not bottom.visited :
            self.neighbors.append (bottom)
            print ('Found bottom')


        # if left is not visited and left is not None then the add it to the neighbors list
        if left is not None and  not left.visited:
            self.neighbors.append (left)
            print ('Found left')

        return self.neighbors



# utility function
def check_valid_index (i, j, grid):
    """
    check that index doesn't go out of bounds for either row or column
    """
    if i >= 0 and i < len (grid)  and j >= 0 and j < len (grid[0]):
        return True
    return False
        
