import random
import MAIN_VALUE

def create_connected_path(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]
    
    start_x, start_y = random.randint(1, height - 2), random.randint(1, width - 2)
    grid[start_x][start_y] = 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    stack = [(start_x, start_y)]
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        found_path = False
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (1 <= nx < height - 1) and (1 <= ny < width - 1) and grid[nx][ny] == 1:
                grid[nx][ny] = 0
                stack.append((nx, ny))
                visited.add((nx, ny))
                found_path = True
                break
        
        if not found_path:
            stack.pop()

    connect_paths(grid, visited)
    return grid

def connect_paths(grid, visited):
    visited = list(visited)
    random.shuffle(visited)  # Randomize the order to add some messiness
    for i in range(len(visited) - 1):
        x1, y1 = visited[i]
        x2, y2 = visited[i + 1]
        
        if y1 == y2:
            for j in range(min(x1, x2), max(x1, x2) + 1):
                grid[j][y1] = 0
        elif x1 == x2:
            for j in range(min(y1, y2), max(y1, y2) + 1):
                grid[x1][j] = 0
        else:
            for j in range(min(x1, x2), max(x1, x2) + 1):
                grid[j][y2] = 0
            for j in range(min(y1, y2), max(y1, y2) + 1):
                grid[x2][j] = 0

def add_random_buildings(grid, building_density=0.2):
    rows = len(grid)
    cols = len(grid[0])
    
    for _ in range(int((rows - 2) * (cols - 2) * building_density)):
        x, y = random.randint(1, rows - 2), random.randint(1, cols - 2)
        
        # Randomly choose a building size
        if can_place_building(grid, x, y):
            place_building(grid, x, y)

def can_place_building(grid, x, y):
    building_sizes = [(2, 3), (2, 2), (1, 3)]
    size = random.choice(building_sizes)
    
    height, width = size
    
    # Check if there is enough space
    if (x + height - 1 < len(grid) - 1 and 
        y + width - 1 < len(grid[0]) - 1):
        
        # Check if the area is clear (allowing some overlap)
        for i in range(height):
            for j in range(width):
                if grid[x + i][y + j] != 0:
                    return False
        
        return True
    return False

def place_building(grid, x, y):
    building_sizes = [(2, 3), (2, 2), (1, 3)]
    size = random.choice(building_sizes)
    height, width = size
    
    for i in range(height):
        for j in range(width):
            grid[x + i][y + j] = 1

def remove_isolated_paths(grid):
    # Find and remove isolated '0's
    rows, cols = len(grid), len(grid[0])
    
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j] == 0:
                # Check if the '0' is isolated
                if all(grid[i + dx][j + dy] == 1 for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx != 0 or dy != 0)):
                    # If isolated, turn it back to '1'
                    grid[i][j] = 1

def print_map(grid):
    for row in grid:
        print(''.join(str(cell) for cell in row))

def main() :
    # Generate a city map with connected paths and random buildings
    tile_size = MAIN_VALUE.tile_size()
    width = int(MAIN_VALUE.SCREEN_SETTING_size()[0]/tile_size)
    height = int(MAIN_VALUE.SCREEN_SETTING_size()[1]/tile_size)
    city_map = create_connected_path(height, width)
    add_random_buildings(city_map, building_density=0.05)  # Adjust density as needed
    remove_isolated_paths(city_map)  # Ensure no isolated paths remain

    def save_map(grid):
        text = ''
        openfile = open('test.txt', 'w')
        for row in grid:
            text = "".join(map(str, row))
            openfile.write(text + '\n')

    # Generate and print the city map
    save_map(city_map)
