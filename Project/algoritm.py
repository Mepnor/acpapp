import math
import heapq
import create_map
import MAIN_VALUE
import time

# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination

# Check if a cell is valid (within the grid)
def is_valid(row, col, ROW, COL):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 0

# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination
def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append([row, col])
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append([row, col])
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    return path

# Implement the A* search algorithm
def a_star_search(grid, src, dest, ROW, COL):
    ROW = ROW
    COL = COL
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1], ROW, COL) or not is_valid(dest[0], dest[1], ROW, COL):
        print("1 Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("2 Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return 

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j, ROW, COL) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    # Trace and print the path from source to destination
                    way = trace_path(cell_details, dest)
                    found_dest = True
                    return way
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")

def main(grid, src, dest):
    # Define new row and col
    ROW = int(MAIN_VALUE.SCREEN_SETTING_size()[0]/MAIN_VALUE.tile_size())
    COL = int(MAIN_VALUE.SCREEN_SETTING_size()[1]/MAIN_VALUE.tile_size())
    # Define the grid (1 for unblocked, 0 for blocked)
    grid = grid

    # Define the source and destination
    src = src
    dest = dest

    # Run the A* search algorithm
    route = a_star_search(grid, src, dest, ROW, COL)
    return route

def shortest_way(mobile_robot, all_object, grid) :
    # Define new row and col
    ROW = int(MAIN_VALUE.SCREEN_SETTING_size()[0]/MAIN_VALUE.tile_size())
    COL = int(MAIN_VALUE.SCREEN_SETTING_size()[1]/MAIN_VALUE.tile_size())

    # Define the grid (1 for unblocked, 0 for blocked)
    grid = grid

    # list of route
    route = []

    # dict of route
    dict_route = []

    number = 0
    for object in all_object :
        if object.pos != [0,0] :
            # Define the source and destination
            src = [mobile_robot.x, mobile_robot.y]
            dest = object.pos

            route = a_star_search(grid, src, dest, ROW, COL)
            if type(route) == list :
                dict_route.append([number, len(route)])
        number += 1
    dict_route = sorted(dict_route, key=lambda x: x[1])
    route = [i[0] for i in dict_route]
    return route
