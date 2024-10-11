import pygame, random
from pygame.sprite import Group
import maze_game
from maze import *
import algoritm
import MAIN_VALUE

# GAME WINDOW
pygame.init()
SCREEN_WIDTH_SETTING = MAIN_VALUE.SCREEN_SETTING_size()[0]
SCREEN_HEIGHT_SETTING = MAIN_VALUE.SCREEN_SETTING_size()[1]
SCREEN_WIDTH = MAIN_VALUE.SCREEN_size() 
SCREEN_HIGHT = MAIN_VALUE.SCREEN_size()  
SCREEN = pygame.display.set_mode((SCREEN_WIDTH_SETTING, SCREEN_HEIGHT_SETTING))
pygame.display.set_caption('Escaping Maze')

# Clock object
clock = pygame.time.Clock()
FPS = 10

# GAME VARIABLES
tile_size = MAIN_VALUE.tile_size()
number_grid = (SCREEN_HIGHT/tile_size) - 2

# Create the walls of the level
world_data = []

# Create wall group
wall_group = pygame.sprite.Group()

# Create wall group
path_group = pygame.sprite.Group()

# Define spawn position for the mobile robot
spawn_position = ()
walls = []

# Track the player's quantities
quantities = 0

# Time
start_time = 0

# COLORS
GREY = (60, 60, 60)
BG = (50, 50, 50)
GREEN = (100, 255, 10)
BLUE = (70, 130, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (140, 0, 255)
PINK = (255, 0, 200)
CYAN = (0, 255, 195)

black = (0, 0, 0)
white = (255, 255, 255)
col_spd = 1

col_dir = [-30, 30, 30]
def_col = [120, 120, 240]

minimum = 0
maximum = 255

# Assuming you want a fixed size grid for demonstration
grid_rows = SCREEN_HIGHT // tile_size
grid_cols = SCREEN_WIDTH // tile_size


# FONT
FONT = pygame.font.SysFont('Futura', 30)

# FUNCTIONS
def draw_grid(tile_size) :
    # Fill screen
    SCREEN.fill(BG)

    # Draw vertical lines
    for x in range(tile_size, SCREEN_WIDTH_SETTING, tile_size) :
        pygame.draw.line(SCREEN, GREY, (x, 0), (x, SCREEN_HEIGHT_SETTING))

    # Draw horizontal lines
    for y in range(tile_size, SCREEN_HEIGHT_SETTING, tile_size) :
        pygame.draw.line(SCREEN, GREY, (0, y), (SCREEN_WIDTH_SETTING, y))


def new_object_position() :
    #generate random collectable position
    pos = [random.randint(1, number_grid), random.randint(1, number_grid)]
    while pos[0] == mobile_robot.rect.x or pos[1] == mobile_robot.rect.y or pos in walls :
        pos = [random.randint(1, number_grid), random.randint(1, number_grid)]

    return pos

def new_target_position() :
    #generate random collectable position
    pos = [random.randint(1, number_grid), random.randint(1, number_grid)]
    while pos[0] == mobile_robot.rect.x or pos[0] == object1.rect.x or pos[1] == mobile_robot.rect.y or pos[1] == object1.rect.y or pos in walls :
        pos = [random.randint(1, number_grid), random.randint(1, number_grid)]

    return pos

"""
def manaul_target_position(x, y) :
    #generate random collectable position
    target_m = Target_Position(CYAN)
    target_m.rect.x = x*tile_size
    target_m.rect.y = y*tile_size
    return target_m
"""

def display_text(txt, color, font, x, y) :
    text = font.render(txt, True, color)
    SCREEN.blit(text, (x, y))

def end_journey(quantities, time) :
    # Fill the screen
    SCREEN.fill(GREY)

    # Display the end game text
    display_text(f'Mission done : {quantities} pieces in {time} seconds', WHITE, FONT, 150, 295)

def col_change_breathe(color: list, direction: list) -> None:
    """
    This function changes an RGB list in a way that we achieve nice breathing effect.
    :param color: List of RGB values.
    :param direction: List of color change direction values (-1, 0, or 1).
    :return: None
    """
    for i in range(3):
        color[i] += col_spd * direction[i]
        if color[i] >= maximum or color[i] <= minimum:
            direction[i] *= -1
        if color[i] >= maximum:
            color[i] = maximum
        elif color[i] <= minimum:
            color[i] = minimum

def wall_code_gen():
        grid = [[0 for i in range(grid_cols)] for i in range(grid_rows)]
        for wall in wall_group:
            grid_y = wall.rect.y // tile_size
            grid_x = wall.rect.x // tile_size
            if 0 <= grid_y < grid_rows and 0 <= grid_x < grid_cols:
                grid[grid_y][grid_x] = 1
        for row in grid:
            print("".join(map(str, row)))

# CLASSES
class Mobile_Robot:
    def __init__(self, x, y, color) :
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Attributes for moving
        self.moving = False
        self.velocity = 1
        self.dx = 0
        self.dy = 0

    def update(self) :
        # Fill the robot with color
        self.image.fill(self.color)

        # Keep position of snake inside of tiles
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

        # Draw the robot on the screen
        SCREEN.blit(self.image, self.rect)

    def move(self) :
        # Check if mobile robot is moving and mobile robot not colliding with walls
        if self.moving and not self.collision_with_walls():
            self.x += self.dx
            self.y += self.dy
    
    def collision_with_walls(self) :
        # Check for collision with walls
        for wall in wall_group :
            if wall.x == self.x + self.dx and wall.y == self.y + self.dy :
                return True
        return False

class Walls(pygame.sprite.Sprite) :
    def __init__(self, x, y, color) :
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

class Object_Position() :
    def __init__(self, color) :
        self.pos = new_object_position()
        self.x = self.pos[0] * tile_size
        self.y = self.pos[1] * tile_size
        self.image = pygame.Surface((tile_size, tile_size))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self) :
        SCREEN.blit(self.image, self.rect)

class Target_Position() :
    def __init__(self, color) :
        self.pos = new_target_position()
        self.x = self.pos[0] * tile_size
        self.y = self.pos[1] * tile_size
        self.image = pygame.Surface((tile_size, tile_size))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self) :
        SCREEN.blit(self.image, self.rect)

class Paths(pygame.sprite.Sprite) :
    def __init__(self, x, y, color) :
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

maze_game.main()

# Open the level file
with open('Maze.txt', 'r') as world :
    for line in world :
        world_data.append(line)

# Create walls
for row, tiles in enumerate(world_data) :
    for col, tile in enumerate(tiles) :
        if tile == '1' :
            wall = Walls(row, col, BLUE)
            walls.append([row, col])
            wall_group.add(wall)
        elif tile == 'P' :
            spawn_position = (row, col)

# Create walls
grid = []
for row, tiles in enumerate(world_data) :
    sub_grid = []
    for col, tile in enumerate(tiles) :
        if tile == '1' :
            wall = Walls(row, col, BLUE)
            walls.append([row, col])
            wall_group.add(wall)
        elif tile == 'P' :
            spawn_position = (row, col)
        if tile != '\n' and tile != 'P': sub_grid.append(int(tile))
        elif tile != '\n' and tile == 'P': sub_grid.append(int(0))
    grid.append(sub_grid)

# Create the mobile robot
mobile_robot = Mobile_Robot(1, 1, GREEN)
storage = [[mobile_robot.x, mobile_robot.y]]

# Create Object
object1 = Object_Position(RED)

# Create Target
target1 = Target_Position(def_col)

# MAIN LOOB
point1 = 0
j = 0
limit = 0
count = 0
run = True
while run :
    col_change_breathe(def_col, col_dir)
    # Set frame rate
    clock.tick(FPS)

    # Draw grid
    draw_grid(tile_size)

    # Check for collision with object
        
    if object1.rect.colliderect(mobile_robot.rect) :
        object1.image.fill(BLUE)
        object1.rect.x, object1.rect.y = [0,0]
        point1 = 1
    
    # Check for collision with target
        
    if target1.rect.colliderect(mobile_robot.rect) :
        target1.image.fill(mobile_robot.color)
    else :
        target1.image.fill(target1.color)

    if target1.rect.colliderect(mobile_robot.rect) and point1 == 1:
        quantities += 1
        object1 = Object_Position(RED)
        target1 = Target_Position(def_col)
        point1 = 0

    # Draw object
    object1.draw()

    # Draw target
    target1.draw()

    # Draw walls
    wall_group.draw(SCREEN)

    # Draw path
    path_group.draw(SCREEN)

    # Draw robot
    mobile_robot.update()
    mobile_robot.move()

    # timer
    timer = pygame.time.get_ticks() // 1000

    # Display quantites amd time
    display_text(f'Time : {start_time + timer} seconds', WHITE, FONT, 5, 5)
    display_text(f'Quantities : {quantities}', WHITE, FONT, 400, 5)

    # Display end game screen
    if quantities < 20 :
        end = timer
    if quantities == 20 :
        end_journey(quantities, end)

    # Event handler
    for event in pygame.event.get() :
        # Quit
        if event.type == pygame.QUIT:
            run = False
        
        # Key presses for moving the robot
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_e :
                x = int(pygame.mouse.get_pos()[0]/tile_size)
                y = int(pygame.mouse.get_pos()[1]/tile_size)
                for wall in wall_group :
                    if wall.x == x and wall.y == y:
                        wall_group.remove(wall)
            elif event.key == pygame.K_q :
                x = int(pygame.mouse.get_pos()[0]/tile_size)
                y = int(pygame.mouse.get_pos()[1]/tile_size)
                wall = Walls(x, y, BLUE)
                wall_group.add(wall)
                print(wall_group)
            
            elif event.key == pygame.K_LEFT:
                mobile_robot.moving = True
                mobile_robot.dx = -mobile_robot.velocity
                mobile_robot.dy = 0
            
            elif event.key == pygame.K_e :
                x = int(pygame.mouse.get_pos()[0]/tile_size)
                y = int(pygame.mouse.get_pos()[1]/tile_size)
                for wall in wall_group :
                    if wall.x == x and wall.y == y:
                        wall_group.remove(wall)

            elif event.key == pygame.K_RIGHT:
                mobile_robot.moving = True
                mobile_robot.dx = mobile_robot.velocity
                mobile_robot.dy = 0

            elif event.key == pygame.K_UP:
                mobile_robot.moving = True
                mobile_robot.dy = -mobile_robot.velocity
                mobile_robot.dx = 0

            elif event.key == pygame.K_DOWN:
                mobile_robot.moving = True
                mobile_robot.dy = mobile_robot.velocity
                mobile_robot.dx = 0
            
            elif event.key == pygame.K_k :
                wall_code_gen()
            
            elif event.key == pygame.K_s :
                src = [mobile_robot.x, mobile_robot.y]
                if point1 == 0 :
                    dest = [object1.pos[0], object1.pos[1]]
                elif point1 == 1 :
                    dest = [target1.pos[0], target1.pos[1]]
                a = algoritm.main(grid, src, dest)
                limit = len(a)-1
                count = 1
                j = 0
            
            elif event.key == pygame.K_w :
                count = 0

        elif event.type == pygame.KEYUP:
            mobile_robot.moving = False
            mobile_robot.dy = 0
            mobile_robot.dx = 0

    pygame.display.update()

    # Path Drawing
    if [mobile_robot.x, mobile_robot.y] not in storage:
        storage.append([mobile_robot.x, mobile_robot.y])
        if len(storage) > 3 :
            del storage[0]
        for i in storage :
            if i != object1.pos and i != target1.pos:
                path = Paths(i[0], i[1], WHITE)
                path_group.add(path)
            elif i == object1.pos :
                path = Paths(i[0], i[1], object1.color)
            elif i == target1.pos :
                path = Paths(i[0], i[1], target1.color)
    
    # Path Finding

    if j <= limit and count == 1:
        mobile_robot.moving = True
        path = a[j]
        mobile_robot.x = path[0]
        mobile_robot.y = path[1]
        j += 1
    elif  j > limit and count == 1:
        if target1.rect.colliderect(mobile_robot.rect) and point1 == 1 :
            point1 = 0
            object1 = Object_Position(RED)
            target1 = Target_Position(def_col)
            quantities += 1
        elif object1.rect.colliderect(mobile_robot.rect) :
            point1 = 1
        j = 0
        src = [mobile_robot.x, mobile_robot.y]
        if point1 == 0 :
            dest = [object1.pos[0], object1.pos[1]]
        elif point1 == 1 :
            dest = [target1.pos[0], target1.pos[1]]
        a = algoritm.main(grid, src, dest)
        limit = len(a) - 1

pygame.quit()