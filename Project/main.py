import pygame, random
from pygame.sprite import Group
import algoritm
import create_map
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
random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

black = (0, 0, 0)
white = (255, 255, 255)
col_spd = 1

col_dir = [-30, 30, 30]
def_col = [120, 120, 240]

minimum = 0
maximum = 255

# FONT
FONT = pygame.font.SysFont('Futura', 30)

# FUNCTIONS
def draw_grid(tile_size) :
    # Fill screen
    SCREEN.fill(BG)

    # Draw vertical lines
    for x in range(tile_size, SCREEN_HIGHT, tile_size) :
        pygame.draw.line(SCREEN, GREY, (x, 0), (x, SCREEN_HIGHT))

    # Draw horizontal lines
    for y in range(tile_size, SCREEN_WIDTH, tile_size) :
        pygame.draw.line(SCREEN, GREY, (0, y), (SCREEN_WIDTH, y))

def draw_buttom(tile_size) :
    # Fill screen
    SCREEN.fill(BG)

    # Draw vertical lines
    for x in range(tile_size, SCREEN_HIGHT, tile_size) :
        pygame.draw.line(SCREEN, GREY, (x, 0), (x, SCREEN_HIGHT))

    # Draw horizontal lines
    for y in range(tile_size, SCREEN_WIDTH, tile_size) :
        pygame.draw.line(SCREEN, GREY, (0, y), (SCREEN_WIDTH, y))

def draw_wall() :
    # Create walls
    grid = []
    # Walls drawing
    wall_group = pygame.sprite.Group() 
    # Collection
    walls = [] 
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
    return grid, wall_group, walls

def new_object_position() :
    #generate random collectable position
    pos = [random.randint(1, number_grid), random.randint(1, number_grid)]
    position_robot = []
    for robot in multi_mobile_robot :
        position_robot.append([robot.rect.x, robot.rect.y])
    while pos in position_robot or pos in walls :
        pos = [random.randint(1, number_grid), random.randint(1, number_grid)]

    return pos

def new_target_position() :
    #generate random collectable position
    pos = [random.randint(1, number_grid), random.randint(1, number_grid)]
    position_robot = []
    for robot in multi_mobile_robot :
        position_robot.append([robot.rect.x, robot.rect.y])
    position_object = []
    for object in all_object :
        position_object.append([object.rect.x, object.rect.y])
    while pos in position_robot or pos in position_object or pos in walls :
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

def random_zero_coordinates(array):
    # Find all coordinates of '0's in the array
    zero_coordinates = [(i, j) for i in range(len(array)) for j in range(len(array[i])) if array[i][j] == 0]
    
    # Check if there are any zeros found
    if not zero_coordinates:
        return None  # or raise an exception or return a specific value to indicate no zeros
    
    # Randomly select one of the zero coordinates
    return random.choice(zero_coordinates)

def multi_robot(number) :
    #generate multi robot
    list_mobile_robot = []
    same_position = []
    for i in range(0, number):
        spawn_position = random_zero_coordinates(grid)
        while spawn_position in same_position:
            spawn_position = random_zero_coordinates(grid)
        mobile_robot = Mobile_Robot(spawn_position[0], spawn_position[1], GREEN)
        list_mobile_robot.append(mobile_robot)
        same_position.append(spawn_position)
    return list_mobile_robot

def multi_object(number) :
    #generate random collectable position
    list_object = []
    for i in range(0, number):
        object = Object_Position(RED)
        list_object.append(object)
    return list_object

def multi_target(number) :
    #generate random collectable position
    list_target = []
    for i in range(0, number):
        target = Target_Position(def_col)
        list_target.append(target)
    return list_target

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

create_map.main()
# Open the level file
with open('test.txt', 'r') as world :
    for line in world :
        world_data.append(line)

amount = 2
# Walls drawing
wall_components = draw_wall()
grid = wall_components[0]
wall_group = wall_components[1]
# Collection
walls = wall_components[2]

# Create the mobile robot
spawn_position = random_zero_coordinates(grid)
multi_mobile_robot = multi_robot(amount)

# Create Object
all_object = multi_object(amount)

# Create Target
all_target = multi_target(amount)
       
def main() :
    # Track the player's quantities
    quantities = 0
    amount = 2

    # Create the mobile robot
    multi_mobile_robot = multi_robot(amount)
    storage = [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot]
    a = [0 for i in range(0, amount)]

    # Create Object
    object1 = Object_Position(RED)
    all_object = multi_object(amount)

    # Create Target
    target1 = Target_Position(def_col)
    all_target = multi_target(amount)

    # MAIN LOOB
    point = [0 for i in range(0, amount)]
    identify = 0
    j = [0 for i in range(0, amount)]
    list_of_tag = [i for i in range(0, amount)]
    limit = [0 for i in range(0, amount)]
    count = 0
    run = True
    while run :
            col_change_breathe(def_col, col_dir)
            # Set frame rate
            clock.tick(FPS)

            # Draw grid
            draw_grid(tile_size)

            # Draw object
            for object in all_object :
                object.draw()

            # Draw target
            for target in all_target :
                target.draw()

            # Draw walls
            wall_group.draw(SCREEN)

            # Draw path
            path_group.draw(SCREEN)

            # Draw robot
            for number in range(0, amount) :
                multi_mobile_robot[number].update()
                multi_mobile_robot[number].move()
                # Check for collision with object
                
                if all_object[number].rect.colliderect(multi_mobile_robot[number].rect) :
                    all_object[number].image.fill(BLUE)
                    all_object[number].rect.x, all_object[number].rect.y = [0,0]
                    point[number] = 1
                else :
                    all_object[number].image.fill(all_object[number].color)
                
                # Check for collision with target
                
                if all_target[number].rect.colliderect(multi_mobile_robot[number].rect) :
                    all_target[number].image.fill(multi_mobile_robot[number].color)
                else :
                    all_target[number].image.fill(all_target[number].color)

                if all_target[number].rect.colliderect(multi_mobile_robot[number].rect) and point[number] == 1:
                    quantities += 1
                    all_object[number] = Object_Position(RED)
                    all_target[number] = Target_Position(def_col)
                    point[number] = 0

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
                
                # Manualy Adds
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    x = int(pygame.mouse.get_pos()[0]/tile_size)
                    y = int(pygame.mouse.get_pos()[1]/tile_size)
                    wall = Walls(x, y, BLUE)
                    wall_group.add(wall)
                    print(wall_group)

                c = list_of_tag[identify]
                # Key presses for moving the robot
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_1 :
                        if identify < amount-1 : 
                            identify += 1 
                        else : 
                            identify = 0

                    elif event.key == pygame.K_LEFT :
                        multi_mobile_robot[c].moving = True
                        multi_mobile_robot[c].dx = -multi_mobile_robot[c].velocity
                        multi_mobile_robot[c].dy = 0

                    elif event.key == pygame.K_RIGHT :
                        multi_mobile_robot[c].moving = True
                        multi_mobile_robot[c].dx = multi_mobile_robot[c].velocity
                        multi_mobile_robot[c].dy = 0

                    elif event.key == pygame.K_UP :
                        multi_mobile_robot[c].moving = True
                        multi_mobile_robot[c].dy = -multi_mobile_robot[c].velocity
                        multi_mobile_robot[c].dx = 0

                    elif event.key == pygame.K_DOWN :
                        multi_mobile_robot[c].moving = True
                        multi_mobile_robot[c].dy = multi_mobile_robot[c].velocity
                        multi_mobile_robot[c].dx = 0
                    
                    elif event.key == pygame.K_s :
                        for c in list_of_tag :
                            src = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                            if point[c] == 0 :
                                dest = [all_object[c].pos[0], all_object[c].pos[1]]
                            elif point[c] == 1 :
                                dest = [all_target[c].pos[0], all_target[c].pos[1]]
                            a[c] = algoritm.main(grid, src, dest, tile_size)
                            limit[c] = len(a[c])-1
                            count = 1
                            j[c] = 0
                    
                    elif event.key == pygame.K_w :
                        count = 0
                        
                
                elif event.type == pygame.KEYUP :
                    multi_mobile_robot[c].moving = False
                    multi_mobile_robot[c].dy = 0
                    multi_mobile_robot[c].dx = 0
                
                
                # Manualy Adds
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    x = int(pygame.mouse.get_pos()[0]/tile_size)
                    y = int(pygame.mouse.get_pos()[1]/tile_size)
                    print(x, y)
            
            # Using algorithm to find path (A*)
            for c in list_of_tag :
                """
                # Path Finding
                if [multi_mobile_robot[c].x, multi_mobile_robot[c].y] not in storage:
                    storage.append([multi_mobile_robot[c].x, multi_mobile_robot[c].y])
                    for i in storage :
                        if i != all_object[c].pos and i != all_target[c].pos:
                            path = Paths(i[0], i[1], WHITE)
                            path_group.add(path)
                        elif i == all_object[c].pos :
                            path = Paths(i[0], i[1], all_object[c].color)
                        elif i == all_target[c].pos :
                            path = Paths(i[0], i[1], all_target[c].color)
                """
                
                if j[c] <= limit[c] and count == 1:
                    multi_mobile_robot[c].moving = True
                    path = a[c][j[c]]
                    multi_mobile_robot[c].x = path[0]
                    multi_mobile_robot[c].y = path[1]
                    j[c] += 1
                elif  j[c] > limit[c] and count == 1:
                    if target1.rect.colliderect(multi_mobile_robot[c].rect) and point[c] == 1 :
                        point[c] = 0
                        all_object[c] = Object_Position(RED)
                        all_target[c] = Target_Position(def_col)
                        quantities += 1
                    elif object1.rect.colliderect(multi_mobile_robot[c].rect) :
                        point[c] = 1
                    j[c] = 0
                    src = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                    if point[c] == 0 :
                        dest = [all_object[c].pos[0], all_object[c].pos[1]]
                    elif point[c] == 1 :
                        dest = [all_target[c].pos[0], all_target[c].pos[1]]
                    a[c] = algoritm.main(grid, src, dest, tile_size)
                    limit[c] = len(a[c]) - 1

            pygame.display.update()


    pygame.quit()

if __name__ == '__main__':
    main()