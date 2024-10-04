import pygame, random
from pygame.sprite import Group
import algoritm
import create_map
import MAIN_VALUE
import asyncio
import websockets
import json
import threading

# GAME WINDOW
pygame.init()
SCREEN_WIDTH_SETTING = MAIN_VALUE.SCREEN_SETTING_size()[0]
SCREEN_HEIGHT_SETTING = MAIN_VALUE.SCREEN_SETTING_size()[1]
SCREEN_WIDTH = MAIN_VALUE.SCREEN_SETTING_size()[0] #600
SCREEN_HIGHT = MAIN_VALUE.SCREEN_SETTING_size()[1] #600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH_SETTING, SCREEN_HEIGHT_SETTING))
pygame.display.set_caption('Escaping Maze')

# Clock object
clock = pygame.time.Clock()
FPS = 10

# GAME VARIABLES
tile_size = MAIN_VALUE.tile_size()
number_grid_width = (SCREEN_WIDTH//tile_size) - 2
number_grid_height = (SCREEN_HIGHT//tile_size) - 2

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
    for x in range(tile_size, SCREEN_WIDTH_SETTING, tile_size) :
        pygame.draw.line(SCREEN, GREY, (x, 0), (x, SCREEN_HEIGHT_SETTING))

    # Draw horizontal lines
    for y in range(tile_size, SCREEN_HEIGHT_SETTING, tile_size) :
        pygame.draw.line(SCREEN, GREY, (0, y), (SCREEN_WIDTH_SETTING, y))

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
    pos = [random.randint(1, number_grid_width), random.randint(1, number_grid_height)]
    position_robot = []
    for robot in multi_mobile_robot :
        position_robot.append([robot.x, robot.y])
    while pos in position_robot or pos in walls :
        pos = [random.randint(1, number_grid_width), random.randint(1, number_grid_height)]
    return pos

def new_target_position() :
    #generate random collectable position
    pos = [random.randint(1, number_grid_width), random.randint(1, number_grid_height)]
    position_robot = []
    for robot in multi_mobile_robot :
        position_robot.append([robot.x, robot.y])
    position_object = []
    for object in all_object :
        position_object.append([object.x, object.y])
    while pos in position_robot or pos in position_object or pos in walls :
        pos = [random.randint(1, number_grid_width), random.randint(1, number_grid_height)]

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

def mini_robot(number) :
    #generate multi robot
    list_mini_robot = []
    spawn_position = [0,0]
    for i in range(0, number):
        mobile_robot = Mobile_Robot(spawn_position[0], spawn_position[1], all_object[i].color)
        list_mini_robot.append(mobile_robot)
    return list_mini_robot

def multi_object(number) :
    #generate random collectable position
    list_object = []
    for i in range(0, number):
        object = Object_Position(RED)
        while object.pos in [list_object[j].pos for j in range(0, len(list_object))] or object.pos in [[multi_mobile_robot[j].x, multi_mobile_robot[j].y] for j in range(0, len(multi_mobile_robot))]:
            object = Object_Position(RED)
        list_object.append(object)
    return list_object

def multi_target(number) :
    #generate random collectable position
    list_target = []
    for i in range(0, number):
        target = Target_Position(def_col)
        while target.pos in [list_target[j].pos for j in range(0, len(list_target))] or target.pos in [[multi_mobile_robot[j].x, multi_mobile_robot[j].y] for j in range(0, len(multi_mobile_robot))] or target.pos in [all_object[j].pos for j in range(0, len(all_object))]:
            target = Target_Position(def_col)
        list_target.append(target)
    return list_target

# CLASSES

class Mobile_Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, color) :
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load("duck_with_knife_ver2.png").convert_alpha(), (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hitbox_rect = self.rect.inflate(-76, -36)
        self.rect.center = self.hitbox_rect.center
        self.rotate = 0

        # Attributes for moving
        self.moving = False
        self.velocity = 1
        self.dx = 0
        self.dy = 0

        # Carry object
        self.Maximum_capacity = 1
        self.capacity = self.Maximum_capacity

    def update(self) :
        
        # Original Position
        self.orinal_position = self.rect
        
        # Keep position of snake inside of tiles
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

        # Draw the robot on the screen
        SCREEN.blit(self.image, self.rect)
    
    def mini_update(self) :

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
    
    def manual_move(self, keys) :
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
    
    def collision_with_walls(self) :
        # Check for collision with walls
        for wall in wall_group :
            if wall.x == self.x + self.dx and wall.y == self.y + self.dy :
                return True
        return False

    def carry(self) :
        # Check for carrying object
        if self.capacity > 0 :
            return True
        else :
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
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self) :
        SCREEN.blit(self.image, self.rect)

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = target.rect.centerx - SCREEN_WIDTH_SETTING // 2
        y = target.rect.centery - SCREEN_HEIGHT_SETTING // 2

        # Keep the camera within the bounds of the level
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH_SETTING), x)
        y = max(-(self.height - SCREEN_HEIGHT_SETTING), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)


create_map.main()
# Open the level file
with open('test.txt', 'r') as world :
    for line in world :
        world_data.append(line)

amount_robot = 2
amount_object = 20
# Walls drawing
wall_components = draw_wall()
grid = wall_components[0]
wall_group = wall_components[1]

# Collection
walls = wall_components[2]

# Create the mobile robot
spawn_position = random_zero_coordinates(grid)
multi_mobile_robot = multi_robot(amount_robot)
storage = [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot]
a = [0 for i in range(0, amount_robot)]

# Create Object
all_object = multi_object(amount_object)

# Create Target
all_target = multi_target(amount_robot)

# Create the mini-mobile robot
mini_mobile_robot = mini_robot(amount_robot)

# Track the player's quantities
quantities = 0

# MAIN LOOB
point = [0 for i in range(0, amount_robot)]
identify = 0
j = [0 for i in range(0, amount_robot)]
list_of_tag = [i for i in range(0, amount_robot)]
limit = [0 for i in range(0, amount_robot)]
src = [0 for i in range(0, amount_robot)]
dest = [0 for i in range(0, amount_robot)]
all_path = [0 for i in range(0, amount_robot)]
task = [0 for i in range(0, amount_robot)]
count = 0
original_list = [i for i in range(0, len(all_object))]
tag_object = [original_list[i:i + len(all_object)//len(multi_mobile_robot)] for i in range(0, len(original_list), len(all_object)//len(multi_mobile_robot))]
if len(tag_object) != len(multi_mobile_robot) :
    for i in tag_object[-1] :
        tag_object[-2].append(i)
    tag_object.pop(-1)
#camera = Camera(SCREEN_WIDTH_SETTING*2, SCREEN_HEIGHT_SETTING*2)
run = True
while run:
    col_change_breathe(def_col, col_dir)
    # Set frame rate
    clock.tick(FPS)

    # Draw grid
    draw_grid(tile_size)

    # Draw object
    for object in all_object:
        object.draw()

    # Draw target
    for target in all_target:
        target.draw()

    # Draw walls
    wall_group.draw(SCREEN)

    # Draw path
    path_group.draw(SCREEN)
    
    for number in range(0, amount_robot):

        # Draw robot
        multi_mobile_robot[number].update()
        multi_mobile_robot[number].move()

        deleted_object = []

        for number_object in range(0, len(all_object)) :
            
            # Check for collision with object

            if all_object[number_object].rect.colliderect(multi_mobile_robot[number].rect) and multi_mobile_robot[number].carry() : #and number_object == all_path[number][0]
                all_object[number_object].image.fill(BLUE)
                all_object[number_object].rect.x, all_object[number_object].rect.y = [0, 0]
                all_object[number_object].pos = [0, 0]
                multi_mobile_robot[number].capacity -= 1
                point[number] = 1
                break
            else:
                all_object[number_object].image.fill(all_object[number_object].color)

            # Check for collision with target

            if all_target[number].rect.colliderect(multi_mobile_robot[number].rect) and multi_mobile_robot[number].capacity != multi_mobile_robot[number].Maximum_capacity:
                all_target[number].image.fill(multi_mobile_robot[number].color)
                multi_mobile_robot[number].capacity = multi_mobile_robot[number].Maximum_capacity
                quantities += 1
                if point[number] == 1 :
                    #all_target[number] = Target_Position(def_col)
                    point[number] = 0
                    if count == 0 : all_object.pop(number_object)

            else:
                all_target[number].image.fill(all_target[number].color)   

    # timer
    timer = pygame.time.get_ticks() // 1000

    # Display quantities and time
    display_text(f'Time : {start_time + timer} seconds', WHITE, FONT, 5, 5)
    display_text(f'Quantities : {quantities}', WHITE, FONT, 400, 5)

    # Display end game screen
    if len(all_object) > 0:
        end = timer
    if len(all_object) == -1:
        end_journey(quantities, end)

    # Event handler
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            run = False

        # Manually Adds
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x = int(pygame.mouse.get_pos()[0] / tile_size)
            y = int(pygame.mouse.get_pos()[1] / tile_size)
            #wall = Walls(x, y, BLUE)
            #wall_group.add(wall)
            print(x, y)

        c = list_of_tag[identify]
        # Key presses for moving the robot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if identify < amount_robot - 1:
                    identify += 1
                else:
                    identify = 0

            elif event.key == pygame.K_LEFT:
                multi_mobile_robot[c].moving = True
                multi_mobile_robot[c].dx = -multi_mobile_robot[c].velocity
                multi_mobile_robot[c].dy = 0
            
            elif event.key == pygame.K_e :
                x = int(pygame.mouse.get_pos()[0]/tile_size)
                y = int(pygame.mouse.get_pos()[1]/tile_size)
                for wall in wall_group :
                    if wall.x == x and wall.y == y:
                        wall_group.remove(wall)

            elif event.key == pygame.K_RIGHT:
                multi_mobile_robot[c].moving = True
                multi_mobile_robot[c].dx = multi_mobile_robot[c].velocity
                multi_mobile_robot[c].dy = 0

            elif event.key == pygame.K_UP:
                multi_mobile_robot[c].moving = True
                multi_mobile_robot[c].dy = -multi_mobile_robot[c].velocity
                multi_mobile_robot[c].dx = 0

            elif event.key == pygame.K_DOWN:
                multi_mobile_robot[c].moving = True
                multi_mobile_robot[c].dy = multi_mobile_robot[c].velocity
                multi_mobile_robot[c].dx = 0

            elif event.key == pygame.K_s:
                for c in list_of_tag:
                    all_path[c] = algoritm.shortest_way(multi_mobile_robot[c], all_object, grid)
                    if all_path[c-1] != 0 and all_path[c] != 0:
                        i = 0
                        while all_object[all_path[c][0]].pos == all_object[all_path[c-1][0]].pos and i < c:
                            all_path[c][0], all_path[c][1] = all_path[c][1], all_path[c][0]
                            i += 1
                    for number_object in range(0, len(all_object)) :
                        src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                        if point[c] == 0:
                            dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                        elif point[c] == 1:
                            dest[c] = [all_target[c].pos[0], all_target[c].pos[1]]
                        a[c] = algoritm.main(grid, src[c], dest[c])
                        limit[c] = len(a[c]) - 1
                        count = 1
                        j[c] = 0

            elif event.key == pygame.K_w:
                count = 0

        elif event.type == pygame.KEYUP:
            multi_mobile_robot[c].moving = False
            multi_mobile_robot[c].dy = 0
            multi_mobile_robot[c].dx = 0
    
    # Using algorithm to find path (A*)
    for c in list_of_tag:
        if j[c] <= limit[c] and count == 1 and type(a[c]) == list :
            g = [0 for i in range(amount_robot)]
            i = 1
            swaping = 1
            while i <= c and len(all_path[c]) > 1 and len(all_path[c-i]) > 1 and 1 not in point:
                if all_path[c][0] == all_path[c-i][0] :
                    all_path[c][0], all_path[c][swaping] = all_path[c][swaping], all_path[c][0]
                    while all_path[c][0] > len(all_object) :
                        swaping += 1
                        all_path[c][0], all_path[c][swaping] = all_path[c][swaping], all_path[c][0]
                    print(f'all_path[c][0] : {all_path[c][0]}, all_path[c-i] = {all_path[c-i]}')
                    print(f'all_object[all_path[c][0]].pos[0] : {all_object[all_path[c][0]].pos[0]}, all_object[all_path[c][0]].pos[1] = {all_object[all_path[c][0]].pos[1]}')
                    dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                    g[c] = 1
                    swaping += 1
                i += 1
            if g[c] == 1 :
                src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                a[c] = algoritm.main(grid, src[c], dest[c])
                j[c] = 0
                g[c] = 0
                if type(a[c]) == list : 
                    limit[c] = len(a[c]) - 1
            multi_mobile_robot[c].moving = True
            path = a[c][j[c]]
            multi_mobile_robot[c].x = path[0]
            multi_mobile_robot[c].y = path[1]
            if j[c] > 0:
                mini_path = a[c][j[c] - 2]
                mini_mobile_robot[c].moving = True
                mini_mobile_robot[c].x = mini_path[0]
                mini_mobile_robot[c].y = mini_path[1]
            j[c] += 1
        elif (j[c] > limit[c] or point[c] == 1) and count == 1 :
            j[c] = 0
            src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
            if point[c] == 0 and len(all_object) > 0:
                all_path[c] = algoritm.shortest_way(multi_mobile_robot[c], all_object, grid)
                dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                task[c] += 1
            elif point[c] == 1 and len(all_object) > 0:
                for object in all_object :
                    if object.pos == [0, 0] :
                        all_object.remove(object)
                while i <= c and all_path[c][0] < len(all_object) and len(all_path[c]) > 1 and len(all_path[c-i]) > 1 :
                    if all_path[c][0] == all_path[c-i][0] :
                        all_path[c][0], all_path[c][swaping] = all_path[c][swaping], all_path[c][0]
                        while all_path[c][0] > len(all_object) :
                            swaping += 1
                            all_path[c][0], all_path[c][swaping] = all_path[c][swaping], all_path[c][0]
                        print(f'all_path[c][0] : {all_path[c][0]}, all_path[c-i] = {all_path[c-i]}')
                        print(f'all_object[all_path[c][0]].pos[0] : {all_object[all_path[c][0]].pos[0]}, all_object[all_path[c][0]].pos[1] = {all_object[all_path[c][0]].pos[1]}')
                        dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                        g[c] = 1
                        swaping += 1
                    i += 1
                if g[c] == 1 :
                    src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                    a[c] = algoritm.main(grid, src[c], dest[c])
                    j[c] = 0
                    g[c] = 0
                    if type(a[c]) == list : 
                        limit[c] = len(a[c]) - 1
                if len(tag_object[c]) > 0 :
                    tag_object[c].pop(0)
                dest[c] = [all_target[c].pos[0], all_target[c].pos[1]]
            score = 0
            for amout_task in task :
                score += amout_task
            a[c] = algoritm.main(grid, src[c], dest[c])
            if type(a[c]) == list : 
                limit[c] = len(a[c]) - 1
        

        if point[c] == 1 and j[c] > 1:
            mini_mobile_robot[c].mini_update()
            mini_mobile_robot[c].move()


    pygame.display.update()
    pygame.time.delay(100)

variable = {
    'quantitys': quantities,
    'time_spent': timer,
}


async def send_game_stats():
    uri = "ws://localhost:8000/ws/game_stats"
    
    # Attempt to connect to the WebSocket
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                # Send the quantities variable as JSON
                print("Sending data:", variable)
                await websocket.send(json.dumps(variable))
                await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Failed to connect or send data: {e}")

# Start the WebSocket client in the background
asyncio.get_event_loop().run_until_complete(send_game_stats())
