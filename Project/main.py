import pygame, random
from pygame.sprite import Group
import algoritm
import create_map
import MAIN_VALUE
import asyncio
import json
import websocket
import threading
import time
from PIL import Image
import io
import base64
# GAME WINDOW
pygame.init()
SCREEN_WIDTH_SETTING = MAIN_VALUE.SCREEN_WIDTH
SCREEN_HEIGHT_SETTING = MAIN_VALUE.SCREEN_HIGHT
SCREEN_WIDTH = MAIN_VALUE.SCREEN_SETTING_size()[0] #600
SCREEN_HIGHT = MAIN_VALUE.SCREEN_SETTING_size()[1] #600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH_SETTING, SCREEN_HEIGHT_SETTING))
pygame.display.set_caption('Escaping Maze')

# Clock object
clock = pygame.time.Clock()
FPS = 10
# Shared variable to store game stats
variable = {
    'quantitys': 0,
    'time_spent': 0,
    'time_when_end': 0
}
quantities = 0
timer = 0
total = 0
timeRef = 0
endtime = 0

def send_game_stats():
    uri = "ws://localhost:8000/ws/game_stats"
    while True:
        try:
            ws = websocket.WebSocket()
            ws.connect(uri)
            print("Connected to the server")
            while True:
                # Update the variable dictionary before sending
                variable['ObjectC'] = amount_object
                variable['RobotC'] = amount_robot
                variable['TargetC'] = amount_target
                variable['quantitys'] = quantities
                variable['time_spent'] = timer
                variable['time_when_end'] = endtime
                variable['Robot1C'] = task[0]
                variable['Robot2C'] = task[1]
                variable['Robot3C'] = task[2]
                variable['Robot4C'] = task[3]
                variable['Robot5C'] = task[4]
                variable['Robot6C'] = task[5]
                variable['Robot7C'] = task[6]
                variable['Robot8C'] = task[7]
                variable['Robot9C'] = task[8]
                variable['Robot10C'] = task[9]
                variable['Robot1P'] = sum(Distance[0])
                variable['Robot2P'] = sum(Distance[1])
                variable['Robot3P'] = sum(Distance[2])
                variable['Robot4P'] = sum(Distance[3])
                variable['Robot5P'] = sum(Distance[4])
                variable['Robot6P'] = sum(Distance[5])
                variable['Robot7P'] = sum(Distance[6])
                variable['Robot8P'] = sum(Distance[7])
                variable['Robot9P'] = sum(Distance[8])
                variable['Robot10P'] = sum(Distance[9])
                variable['target1'] = Object_in_target[0]
                variable['target2'] = Object_in_target[1]
                # Get the current frame image
                image_data = get_frame_image()
                # Create a data packet
                data_packet = {
                    'stats': variable,
                    'frame': image_data,
                }
                ws.send(json.dumps(data_packet))
                time.sleep(0.1)  # Adjust the sleep time as needed
        except Exception as e:
            print(f"Connection error: {e}") 
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)  # Wait before trying to reconnect



# Convert the NumPy array to an image
def get_frame_image():
    frame_surface = pygame.display.get_surface()
    frame_str = pygame.image.tostring(frame_surface, 'RGB')
    image = Image.frombytes('RGB', frame_surface.get_size(), frame_str)
    
    # Increase image size
    image = image.resize((720, 360))
    
    buffer = io.BytesIO()
    # Increase image quality
    image.save(buffer, format='JPEG', quality=50)
    image_data = buffer.getvalue()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image


# Start the WebSocket client in a separate thread
threading.Thread(target=send_game_stats, daemon=True).start()
# GAME VARIABLES
tile_size = MAIN_VALUE.tile_size()
number_grid_width = (SCREEN_WIDTH//tile_size) - 2
number_grid_height = (SCREEN_HIGHT//tile_size) - 2

# Create the walls of the level
world_data = []

# Create wall group
wall_group = pygame.sprite.Group()

# Create path group
path_group = pygame.sprite.Group()

# Create button group
button_group = pygame.sprite.Group()

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
DARKBLUE = (0, 0, 129)
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

def shift_list_forward(lst):
    if len(lst) > 1:
        # Move the first element to the last position and shift others forward
        lst = lst[1:] + [lst[0]]
    return lst

# CLASSES

class Mobile_Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, color) :
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load("mobile_robot_mark1.png").convert_alpha(), (tile_size * 2, tile_size * 2))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect_demo = self.image.get_rect(topleft=(self.x, self.y))
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
        self.rect_demo.x = (self.x * tile_size) - (tile_size//2) - 1 
        self.rect_demo.y = (self.y * tile_size) - (tile_size//2) - 1

        self.rect.x = (self.x * tile_size)
        self.rect.y = (self.y * tile_size)

        # Draw the robot on the screen
        SCREEN.blit(self.image, self.rect_demo)
    
    def mini_update(self) :

        # Fill the robot with color
        self.image = pygame.Surface((tile_size, tile_size))
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
        print
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

class Home_Position() :
    def __init__(self, color) :
        self.pos = [multi_mobile_robot[-1].x, multi_mobile_robot[-1].y]
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

class Button(pygame.sprite.Sprite) :
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

    #def push_add(self, x, y) :

class Cell_Button(pygame.sprite.Sprite) :
    def __init__(self, x, y, scale, color) :
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tile_size * scale[0], tile_size * scale[1]))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

    def draw(self) :
        SCREEN.blit(self.image, self.rect)

class Functional_Button() :
    def __init__(self, x, y, scale, image) :
        super().__init__()

        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (tile_size * scale[0], tile_size * scale[1]))
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

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

amount_robot = 10
amount_object = 50
amount_target = 2
# Walls drawing
wall_components = draw_wall()
grid = wall_components[0]
wall_group = wall_components[1]

# Collection
walls = wall_components[2]

# Create Button
start_w = (((MAIN_VALUE.SCREEN_WIDTH//tile_size) - (MAIN_VALUE.SCREEN_WIDTH_SETTING//tile_size))//2) + (MAIN_VALUE.SCREEN_WIDTH_SETTING//tile_size) - (120//tile_size)
end_w = (((MAIN_VALUE.SCREEN_WIDTH//tile_size) - (MAIN_VALUE.SCREEN_WIDTH_SETTING//tile_size))//2) + (MAIN_VALUE.SCREEN_WIDTH_SETTING//tile_size) + (120//tile_size)
start_h = ((MAIN_VALUE.SCREEN_WIDTH_SETTING//tile_size)//2) - (300//tile_size)
end_h = ((MAIN_VALUE.SCREEN_WIDTH_SETTING//tile_size)//2) + (360//tile_size)
frame_button = [[i for i in range(start_w, end_w)] for i in range(start_h, end_h)]
button_column = [i for i in range(start_w, end_w)]
button_row = [i for i in range(start_h, end_h)]

for i in range(start_h, end_h) :
    for j in range(start_w, end_w) :
        button = Button(j, i, WHITE)
        button_group.add(button)

plus_button = Functional_Button(button_column[2], button_row[2], [4,4], "plus_icon.png")
minus_button = Functional_Button(button_column[-6], button_row[2], [4,4], "minus_icon.png")
robot_button_cell = Cell_Button(button_column[(len(button_column)//2) - 6], button_row[8], [12,5], DARKBLUE)
robot_button = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[9], [3,3], "mobile_robot.png")
object_button_cell = Cell_Button(button_column[(len(button_column)//2) - 6], button_row[14], [12,5], DARKBLUE)
object_button = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[15], [3,3], "object.png")
target_button_cell = Cell_Button(button_column[(len(button_column)//2) - 6], button_row[20], [12,5], DARKBLUE)
target_button = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[21], [3,3], "target.png")
change_position_button_cell = Cell_Button(button_column[(len(button_column)//2) - 6], button_row[26], [12,5], PURPLE)
reset_button_cell = Cell_Button(button_column[(len(button_column)//2) - 6], button_row[32], [12,5], RED)
start_stop = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[38], [5,5], "Start_button.png")

def on_click(col, row, size, color, border_color) :
    outside_on_click_cell = Cell_Button(col, row, [size[0], size[1]], border_color)
    inside_on_click_cell  = Cell_Button(col+1, row, [size[0]-1, size[1]], color)
    return outside_on_click_cell, inside_on_click_cell

onclick_robot_button_cell = on_click(button_column[(len(button_column)//2) - 6], button_row[8], [12,5], DARKBLUE, CYAN)
onclick_object_button_cell = on_click(button_column[(len(button_column)//2) - 6], button_row[14], [12,5], DARKBLUE, CYAN)
onclick_target_button_cell = on_click(button_column[(len(button_column)//2) - 6], button_row[20], [12,5], DARKBLUE, CYAN)
onclick_change_position_button_cell = on_click(button_column[(len(button_column)//2) - 6], button_row[26], [12,5], PURPLE, PINK)


# Create the mobile robot
spawn_position = random_zero_coordinates(grid)
multi_mobile_robot = multi_robot(amount_robot)
original_robot_position = [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot]
a = [0 for i in range(0, amount_robot)]

# Create Object
all_object = multi_object(amount_object)
original_object_pos_position = [[Object.pos[0], Object.pos[1]] for Object in all_object]
original_object_position = [[Object.x, Object.y] for Object in all_object]
original_object_rect_position = [[Object.rect.x, Object.rect.y] for Object in all_object]

# Create Target
all_target = multi_target(amount_target)
original_target_pos_position = [[Target.pos[0], Target.pos[1]] for Target in all_target]
original_target_position = [[Target.x, Target.y] for Target in all_target]
original_target_rect_position = [[Target.rect.x, Target.rect.y] for Target in all_target]

# Create Home
home = Home_Position(WHITE)
original_home_target = home

# Create the mini-mobile robot
mini_mobile_robot = mini_robot(amount_robot)

# Track the player's quantities
quantities = 0

# MAIN LOOB
point = [0 for i in range(0, amount_robot)]
button_type = ["None"]
identify = 0
j = [0 for i in range(0, amount_robot)]
list_of_tag = [i for i in range(0, amount_robot)]
limit = [0 for i in range(0, amount_robot)]
src = [0 for i in range(0, amount_robot)]
dest = [0 for i in range(0, amount_robot)]
all_path = [0 for i in range(0, amount_robot)]
path_to_target = [0 for i in range(0, amount_robot)]
task = [0 for i in range(0, amount_robot)]
original_path = []
count = 0
original_list = [i for i in range(0, len(all_object))]
check = [False for i in range(0, amount_robot)]
mouse_clicked = False  # Flag to track if the mouse was clicked
second_mouse_click = False
change_position_condition = False
start_stop_check = [False for i in range(0, 3)]
start_check = 0
condition = 0

# STATIC
# Time of each robot to done its one task
robot_timer = [0 for i in range(0, amount_robot)]
Operating_time = [[] for i in range(0, amount_robot)]

# The number of objects of each target
Object_in_target = [0 for i in range(0, amount_target)]

# Distance of each robot when they do one task (j values)
half_path = [0 for i in range(0, amount_robot)]
Distance = [[] for i in range(0, amount_robot)]

#camera = Camera(SCREEN_WIDTH_SETTING*2, SCREEN_HEIGHT_SETTING*2)
run = True
while run:
    col_change_breathe(def_col, col_dir)
    # Set frame rate
    clock.tick(FPS)
    if quantities == amount_object:
        timeRef = pygame.time.get_ticks() // 1000
    else:
        timeRef = endtime
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw grid
    draw_grid(tile_size)

    # Draw object
    for object in all_object:
        object.draw()

    # Draw target
    for target in all_target:
        target.draw()

    # Home position
    home.draw()

    # Draw walls
    wall_group.draw(SCREEN)

    # Draw button
    button_group.draw(SCREEN)
    plus_button.draw()
    minus_button.draw()
    robot_button_cell.draw()
    robot_button.draw()
    object_button_cell.draw()
    object_button.draw()
    target_button_cell.draw()
    target_button.draw()
    change_position_button_cell.draw()
    reset_button_cell.draw()
    start_stop.draw()
    if button_type[0] == "Robot" :
        onclick_robot_button_cell[0].draw()
        onclick_robot_button_cell[1].draw()
        robot_button.draw()
    if button_type[0] == "Object" :
        onclick_object_button_cell[0].draw()
        onclick_object_button_cell[1].draw()
        object_button.draw()
    if button_type[0] == "Target" :
        onclick_target_button_cell[0].draw()
        onclick_target_button_cell[1].draw()
        target_button.draw()

    if mouse_clicked or second_mouse_click:
        onclick_change_position_button_cell[0].draw()
        onclick_change_position_button_cell[1].draw()

    # Draw path
    path_group.draw(SCREEN)
    
    for number in range(0, amount_robot):

        # Draw robot
        multi_mobile_robot[number].update()
        multi_mobile_robot[number].move()

        deleted_object = []

        if len(all_object) > 0 :
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

        for number_target in range(0, len(all_target)) :
            # Check for collision with target
            if all_target[number_target].rect.colliderect(multi_mobile_robot[number].rect) and multi_mobile_robot[number].capacity != multi_mobile_robot[number].Maximum_capacity:
                all_target[number_target].image.fill(multi_mobile_robot[number].color)
                multi_mobile_robot[number].capacity = multi_mobile_robot[number].Maximum_capacity
                
                if point[number] == 1 :
                    #all_target[number] = Target_Position(def_col)
                    point[number] = 0
            else:
                all_target[number_target].image.fill(all_target[number_target].color)   

    # timer
    timer = pygame.time.get_ticks() // 1000
    variable['quantitys'] = quantities
    variable['time_spent'] = timer
    variable['time_when_end'] = endtime

    # Display quantities and time
    display_text(f'Time : {start_time + timer} seconds', WHITE, FONT, 775, 5)
    display_text(f'Quantities : {quantities}', WHITE, FONT, 775, 30)
    display_text(f'Number of Robot : {amount_robot}', WHITE, FONT, 1075, 5)
    display_text(f'Number of Object : {amount_object}', WHITE, FONT, 1075, 30)
    display_text(f'Number of Target : {amount_target}', WHITE, FONT, 1075, 55)
    display_text(f'NEW POSITION', WHITE, FONT, button_column[(len(button_column)//2) - 5] * tile_size, button_row[28] * tile_size)
    display_text(f'RESET', WHITE, FONT, button_column[(len(button_column)//2) - 2] * tile_size, button_row[34] * tile_size)

    # Display end game screen
    if len(all_object) > 0:
        end = timer
    if len(all_object) == -1:
        end_journey(quantities, end)

    # Event handler
    for event in pygame.event.get():
        update = False
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
        
        # Robot button
        if robot_button_cell.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Click Robot")
                button_type[0] = "Robot"

        # Object button
        elif object_button_cell.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Click Object")
                button_type[0] = "Object"

        # Target button
        elif target_button_cell.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Click Target")
                button_type[0] = "Target"
        
        # New Position button
        elif change_position_button_cell.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Click New Position")
                mouse_clicked = True
                condition = 0
        
        # Reset button
        elif reset_button_cell.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Click Reset")
                count = 0
                amount_robot = len(original_robot_position)
                amount_object = len(original_object_position)
                amount_target = len(original_target_position)
                multi_mobile_robot = multi_robot(amount_robot)
                all_object = multi_object(amount_object)
                all_target = multi_target(amount_target)
                home = Home_Position(WHITE)
                mini_mobile_robot = mini_robot(amount_robot)
                
                for tag in range(0, len(multi_mobile_robot)) :
                    multi_mobile_robot[tag].x, multi_mobile_robot[tag].y = original_robot_position[tag][0], original_robot_position[tag][1]

                for tag in range(0, len(all_object)) :
                    all_object[tag].pos[0], all_object[tag].pos[1] = original_object_pos_position[tag][0], original_object_pos_position[tag][1]
                    all_object[tag].x, all_object[tag].y = original_object_position[tag][0], original_object_position[tag][1]
                    all_object[tag].rect.x, all_object[tag].rect.y = original_object_rect_position[tag][0], original_object_rect_position[tag][1]

                for tag in range(0, len(all_target)) :
                    all_target[tag].pos[0], all_target[tag].pos[1] = original_target_pos_position[tag][0], original_target_pos_position[tag][1]
                    all_target[tag].x, all_target[tag].y = original_target_position[tag][0], original_target_position[tag][1]
                    all_target[tag].rect.x, all_target[tag].rect.y = original_target_rect_position[tag][0], original_target_rect_position[tag][1]

                home = original_home_target

                # Track the player's quantities
                quantities = 0

                # MAIN LOOB
                point = [0 for i in range(0, amount_robot)]
                button_type = ["None"]
                identify = 0
                j = [0 for i in range(0, amount_robot)]
                list_of_tag = [i for i in range(0, amount_robot)]
                limit = [0 for i in range(0, amount_robot)]
                src = [0 for i in range(0, amount_robot)]
                dest = [0 for i in range(0, amount_robot)]
                all_path = [0 for i in range(0, amount_robot)]
                path_to_target = [0 for i in range(0, amount_robot)]
                task = [0 for i in range(0, amount_robot)]
                original_path = []
                count = 0
                original_list = [i for i in range(0, len(all_object))]
                check = [False for i in range(0, amount_robot)]

                # STATIC
                # Time of each robot to done its one task
                robot_timer = [0 for i in range(0, amount_robot)]
                Operating_time = [[] for i in range(0, amount_robot)]

                # The number of objects of each target
                Object_in_target = [0 for i in range(0, amount_target)]

                # Distance of each robot when they do one task (j values)
                half_path = [0 for i in range(0, amount_robot)]
                Distance = [[] for i in range(0, amount_robot)]

        elif start_stop.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Click Start")
                if start_check == 0 :
                    start_stop_check[0] = True
                    start_stop_check[1] = False 
                    start_stop_check[2] = False
                    start_stop = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[38], [5,5], "Stop_button.png")
                    start_check += 1
                else :
                    if start_check%2 == 1 :
                       start_stop_check[1] = False 
                       start_stop_check[2] = True 
                       start_stop = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[38], [5,5], "Play_button.png")
                       start_check += 1
                    else :
                        start_stop_check[1] = True
                        start_stop_check[2] = False
                        start_stop = Functional_Button(button_column[(len(button_column)//2) - 2], button_row[38], [5,5], "Stop_button.png")
                        start_check += 1
                pygame.time.delay(100)

        # After the event loop, check if the mouse was clicked and process it
        if mouse_clicked and condition > 2:
            if pygame.mouse.get_pressed()[0] and button_type[0] == "Robot" :
                robot_position = [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot]
                x = int(pygame.mouse.get_pos()[0] / tile_size)
                y = int(pygame.mouse.get_pos()[1] / tile_size)

                if [x, y] in robot_position:
                    focused_robot = robot_position.index([x, y])
                    second_mouse_click = True
                    condition = 0
                    mouse_clicked = False  # Reset the flag to avoid repeated clicks
                else:
                    # Display the fading text or handle cases where no robot is clicked
                    text = FONT.render("Error Position", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
                    text_surface = text.convert_alpha()
                    alpha_value = 255 
                    change_position_condition = True
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Object" :
                object_position = [[Object.x // tile_size, Object.y // tile_size] for Object in all_object]
                x = int(pygame.mouse.get_pos()[0] / tile_size)
                y = int(pygame.mouse.get_pos()[1] / tile_size)

                if [x, y] in object_position:
                    focused_robot = object_position.index([x, y])
                    second_mouse_click = True
                    condition = 0
                    mouse_clicked = False  # Reset the flag to avoid repeated clicks
                else:
                    # Display the fading text or handle cases where no robot is clicked
                    text = FONT.render("Error Position", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
                    text_surface = text.convert_alpha()
                    alpha_value = 255 
                    change_position_condition = True
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Target" :
                target_position = [[Target.x // tile_size, Target.y // tile_size] for Target in all_target]
                x = int(pygame.mouse.get_pos()[0] / tile_size)
                y = int(pygame.mouse.get_pos()[1] / tile_size)

                if [x, y] in target_position:
                    focused_robot = target_position.index([x, y])
                    second_mouse_click = True
                    condition = 0
                    mouse_clicked = False  # Reset the flag to avoid repeated clicks
                else:
                    # Display the fading text or handle cases where no robot is clicked
                    text = FONT.render("Error Position", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
                    text_surface = text.convert_alpha()
                    alpha_value = 255 
                    change_position_condition = True
        
        if second_mouse_click and condition > 2 :
            if pygame.mouse.get_pressed()[0] and button_type[0] == "Robot" :
                robot_position = [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot]
                x = int(pygame.mouse.get_pos()[0] / tile_size)
                y = int(pygame.mouse.get_pos()[1] / tile_size)

                if [x, y] not in robot_position and [[Object.x // tile_size, Object.y // tile_size] for Object in all_object] and wall_group and [[Target.x, Target.y] for Target in all_target] :
                    multi_mobile_robot[focused_robot].x, multi_mobile_robot[focused_robot].y = x, y
                    second_mouse_click = False
                else :
                    # Display the fading text or handle cases where no robot is clicked
                    text = FONT.render("Please select again", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
                    text_surface = text.convert_alpha()
                    alpha_value = 255 
                    change_position_condition = True
            
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Object" :
                object_position = [[Object.x // tile_size, Object.y // tile_size] for Object in all_object]
                x = int(pygame.mouse.get_pos()[0] / tile_size)
                y = int(pygame.mouse.get_pos()[1] / tile_size)

                if [x, y] not in object_position and [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot] and wall_group and [[Target.x, Target.y] for Target in all_target] :
                    all_object[focused_robot].pos[0], all_object[focused_robot].pos[1] = x, y
                    all_object[focused_robot].x, all_object[focused_robot].y = x*tile_size, y*tile_size
                    all_object[focused_robot].rect.x, all_object[focused_robot].rect.y = x*tile_size, y*tile_size
                    second_mouse_click = False
                else :
                    # Display the fading text or handle cases where no robot is clicked
                    text = FONT.render("Please select again", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
                    text_surface = text.convert_alpha()
                    alpha_value = 255 
                    change_position_condition = True
            
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Target" :
                target_position = [[Target.x // tile_size, Target.y // tile_size] for Target in all_target]
                x = int(pygame.mouse.get_pos()[0] / tile_size)
                y = int(pygame.mouse.get_pos()[1] / tile_size)

                if [x, y] not in target_position and [[mobile_robot.x, mobile_robot.y] for mobile_robot in multi_mobile_robot] and wall_group and [[Target.x, Target.y] for Target in all_target] :
                    all_target[focused_robot].pos[0], all_target[focused_robot].pos[1] = x, y
                    all_target[focused_robot].x, all_target[focused_robot].y = x*tile_size, y*tile_size
                    all_target[focused_robot].rect.x, all_target[focused_robot].rect.y = x*tile_size, y*tile_size
                    second_mouse_click = False
                else :
                    # Display the fading text or handle cases where no robot is clicked
                    text = FONT.render("Please select again", True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH_SETTING // 2, SCREEN_HEIGHT_SETTING // 2))
                    text_surface = text.convert_alpha()
                    alpha_value = 255 
                    change_position_condition = True
                
        condition += 1

        # Plus button
        if plus_button.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and button_type[0] == "Robot":
                print("Clicked +")
                amount_robot += 1
                update_robot = multi_robot(1)
                multi_mobile_robot.append(update_robot[0])
                pygame.time.delay(100)
                point.append(0)
                j.append(0)
                list_of_tag = [i for i in range(0, amount_robot)]
                limit.append(0)
                src.append(0)
                dest.append(0)
                all_path.append(0)
                path_to_target.append(0)
                task.append(0)
                check.append(False)
                a.append(0)
                mini_mobile_robot = mini_robot(amount_robot)
                robot_timer.append(0)
                Operating_time.append([])
                half_path.append(0)
                Distance.append([])
                count = 0
                update = True
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Object":
                print("Clicked +")
                amount_object += 1
                update_object = multi_object(1)
                all_object.append(update_object[0])
                original_list = [i for i in range(0, len(all_object))]
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Target":
                print("Clicked +")
                amount_target += 1
                update_target = multi_target(1)
                all_target.append(update_target[0])
                Object_in_target.append(0)
        # Minus button
        elif minus_button.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and button_type[0] == "Robot":
                print("Clicked -")
                if amount_robot > 1 :
                    amount_robot -= 1
                    for c in range(list_of_tag[-1], list_of_tag[0] - 1, -1) :
                        if point[c] == 0 :
                            multi_mobile_robot.pop(c-1)
                            point.pop(c-1)
                            j.pop(c-1)
                            list_of_tag = [i for i in range(0, amount_robot)]
                            limit.pop(c-1)
                            src.pop(c-1)
                            dest.pop(c-1)
                            all_path.pop(c-1)
                            path_to_target.pop(c-1)
                            task.pop(c-1)
                            check.pop(c-1)
                            a.pop(c-1)
                            mini_mobile_robot = mini_robot(amount_robot)
                            robot_timer.pop(c-1)
                            Operating_time.pop(c-1)
                            half_path.pop(c-1)
                            Distance.pop(c-1)
                            count = 0
                            break
                    pygame.time.delay(200)
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Object":
                print("Clicked -")
                if amount_object > 1 :
                    amount_object -= 1
                    all_object.pop(-1)
                    original_list = [i for i in range(0, len(all_object))]
            elif pygame.mouse.get_pressed()[0] and button_type[0] == "Target":
                print("Clicked -")
                if amount_target > 1 :
                    amount_target -= 1
                    all_target.pop(-1)
                    Object_in_target.pop(-1)
        
        if update :
            c = -1
            all_path[c] = algoritm.shortest_way(multi_mobile_robot[c], all_object, grid)
            original_path.append(all_path[c][0])
            # Create a new list that excludes the element at index c
            modified_original_path = original_path[:c] + original_path[c+1:]
            if all_path[c-1] != 0 and all_path[c] != 0:
                i = 0
                while all_path[c][0] in modified_original_path and i < c:
                    all_path[c] = shift_list_forward(all_path[c])
                    while all_path[c][0] > len(all_object) :
                        all_path[c] = shift_list_forward(all_path[c])
                    original_path[c] = all_path[c][0]
            # Create a new list that excludes the element at index c
            modified_original_path = original_path[:c] + original_path[c+1:]
            
            src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
            if point[c] == 0:
                dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
            elif point[c] == 1:
                path_to_target[c] = algoritm.shortest_way(multi_mobile_robot[c], all_target, grid)
                dest[c] = [all_target[path_to_target[c][0]].pos[0], all_target[path_to_target[c][0]].pos[1]]
            a[c] = algoritm.main(grid, src[c], dest[c])
            half_path[c] = len(a[c])
            limit[c] = len(a[c]) - 1
            j[c] = 0
            pygame.time.delay(300)
            robot_timer[c] = pygame.time.get_ticks() / 1000

        c = list_of_tag[identify]

        if start_stop_check[0] == True :
            start_stop_check = [False, False, False]
            for c in list_of_tag:
                all_path[c] = algoritm.shortest_way(multi_mobile_robot[c], all_object, grid)
                original_path.append(all_path[c][0])
                # Create a new list that excludes the element at index c
                modified_original_path = original_path[:c] + original_path[c+1:]
                if all_path[c-1] != 0 and all_path[c] != 0:
                    i = 0
                    while all_path[c][0] in modified_original_path and i < c:
                        all_path[c] = shift_list_forward(all_path[c])
                        while all_path[c][0] > len(all_object) :
                            all_path[c] = shift_list_forward(all_path[c])
                        original_path[c] = all_path[c][0]
                # Create a new list that excludes the element at index c
                modified_original_path = original_path[:c] + original_path[c+1:]
                
                src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                if point[c] == 0:
                    dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                elif point[c] == 1:
                    path_to_target[c] = algoritm.shortest_way(multi_mobile_robot[c], all_target, grid)
                    dest[c] = [all_target[path_to_target[c][0]].pos[0], all_target[path_to_target[c][0]].pos[1]]
                a[c] = algoritm.main(grid, src[c], dest[c])
                limit[c] = len(a[c]) - 1
                half_path[c] = len(a[c])
                count = 1
                j[c] = 0
                robot_timer[c] = pygame.time.get_ticks() / 1000

        elif start_stop_check[2] == True :
            count = 0
        
        elif start_stop_check[1] == True :
            count = 1

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
                    original_path.append(all_path[c][0])
                    # Create a new list that excludes the element at index c
                    modified_original_path = original_path[:c] + original_path[c+1:]
                    if all_path[c-1] != 0 and all_path[c] != 0:
                        i = 0
                        while all_path[c][0] in modified_original_path and i < c:
                            all_path[c] = shift_list_forward(all_path[c])
                            while all_path[c][0] > len(all_object) :
                                all_path[c] = shift_list_forward(all_path[c])
                            original_path[c] = all_path[c][0]
                    # Create a new list that excludes the element at index c
                    modified_original_path = original_path[:c] + original_path[c+1:]
                    
                    src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
                    if point[c] == 0:
                        dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                    elif point[c] == 1:
                        path_to_target[c] = algoritm.shortest_way(multi_mobile_robot[c], all_target, grid)
                        dest[c] = [all_target[path_to_target[c][0]].pos[0], all_target[path_to_target[c][0]].pos[1]]
                    a[c] = algoritm.main(grid, src[c], dest[c])
                    limit[c] = len(a[c]) - 1
                    half_path[c] = len(a[c])
                    count = 1
                    j[c] = 0
                    robot_timer[c] = pygame.time.get_ticks() / 1000
                
            elif event.key == pygame.K_w:
                count = 0
            
            elif event.key == pygame.K_p:
                count = 1

        elif event.type == pygame.KEYUP:
            multi_mobile_robot[c].moving = False
            multi_mobile_robot[c].dy = 0
            multi_mobile_robot[c].dx = 0
    
    if change_position_condition == True and alpha_value > 0 :
        # Gradually decrease alpha value to create fade effect
        if alpha_value > 0:
            alpha_value -= 20  # Decrease the alpha value (fades out)
        else:
            alpha_value = 0

        text_surface.set_alpha(alpha_value)
        SCREEN.blit(text_surface, text_rect)

    # Using algorithm to find path (A*)
    for c in list_of_tag: 
        if j[c] <= limit[c] and count == 1 and type(a[c]) == list and check[c] == False:
            # Create a new list that excludes the element at index c
            modified_original_path = original_path[:c] + original_path[c+1:]
            if len(all_path[c]) > 0 and all_path[c][0] in modified_original_path :
                position = original_path.index(all_path[c][0])
                if type(a[position]) == list and len(a[c][j[c]:]) >= len(a[position][j[position]+1:]) :
                    check[c] == True
                    continue
            multi_mobile_robot[c].moving = True
            path = a[c][j[c]]
            past_path = a[c][j[c] - 1]
            if [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [1, 0] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, 1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, 90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [1, 0] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, -1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, -90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [-1, 0] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, 1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, -90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [-1, 0] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, -1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, 90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [0, 1] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, 1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, -90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [0, 1] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, -1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, 90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [0, -1] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, 1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, 90)
            elif [multi_mobile_robot[c].x - past_path[0], multi_mobile_robot[c].y - past_path[1]] == [0, -1] and [path[0] - multi_mobile_robot[c].x, path[1] - multi_mobile_robot[c].y] == [0, -1] :
                multi_mobile_robot[c].image = pygame.transform.rotate(multi_mobile_robot[c].image, -90)

            multi_mobile_robot[c].x = path[0]
            multi_mobile_robot[c].y = path[1]
            if j[c] > 0:
                mini_path = a[c][j[c] - 2]
                mini_mobile_robot[c].moving = True
                mini_mobile_robot[c].x = mini_path[0]
                mini_mobile_robot[c].y = mini_path[1]
            j[c] += 1
        elif (j[c] > limit[c] or check[c] == True) and count == 1 :
            check[c] = False
            j[c] = 0
            src[c] = [multi_mobile_robot[c].x, multi_mobile_robot[c].y]
            if point[c] == 0 and original_path[c] != -1 and [multi_mobile_robot[c].x,multi_mobile_robot[c].y] in original_target_pos_position:
                task[c] += 1
                Operating_time[c].append(robot_timer[c])
                robot_timer[c] = 0
                Object_in_target[path_to_target[c][0]] += 1
                quantities += 1
                robot_timer[c] = pygame.time.get_ticks() / 1000

            if original_path[c] == -1 and point[c] == 0:
                dest[c] = [home.pos[0], home.pos[1]]
            else :
                if point[c] == 0 :
                    all_path[c] = algoritm.shortest_way(multi_mobile_robot[c], all_object, grid)
                    if len(all_path[c]) > 0 :
                        original_path[c] = all_path[c][0]
                        # Create a new list that excludes the element at index c
                        modified_original_path = original_path[:c] + original_path[c+1:]
                        i = 1
                        while all_path[c][0] in modified_original_path and i < len(all_path[c]) :
                            all_path[c] = shift_list_forward(all_path[c])
                            while all_path[c][0] >= len(all_object) :
                                all_path[c] = shift_list_forward(all_path[c])
                            original_path[c] = all_path[c][0]
                            i += 1
                        # Create a new list that excludes the element at index c for checking
                        modified_original_path = original_path[:c] + original_path[c+1:]
                        if all_path[c][0] not in modified_original_path :
                            dest[c] = [all_object[all_path[c][0]].pos[0], all_object[all_path[c][0]].pos[1]]
                            half_path[c] = len(a[c])
                        else :
                            dest[c] = [home.pos[0], home.pos[1]]
                            original_path[c] = -1
                        point[c] = 0
                    else :
                        dest[c] = [home.pos[0], home.pos[1]]
                        original_path[c] = -1
                elif point[c] == 1 :
                    path_to_target[c] = algoritm.shortest_way(multi_mobile_robot[c], all_target, grid)
                    dest[c] = [all_target[path_to_target[c][0]].pos[0], all_target[path_to_target[c][0]].pos[1]]
                    Distance[c].append(half_path[c]+len(a[c]))

            a[c] = algoritm.main(grid, src[c], dest[c])
            if type(a[c]) == list : 
                limit[c] = len(a[c]) - 1

        if point[c] == 1 and j[c] > 2 and j[c] < len(a[c]) - 1:
            mini_mobile_robot[c].mini_update()
            mini_mobile_robot[c].move()

        if quantities == amount_object and endtime == 0:
            endtime = timeRef
            total = 0
    print(Object_in_target)
    print(amount_object)
    print(Operating_time)
    pygame.display.update()
    pygame.time.delay(100)
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
total = 0
for i in range(len(task)):
    print("Robot ", i+1, " : ", task[i])
    total += task[i]
print("Total : ", total)

for i in range(len(Operating_time)):
    print("Robot timer ", i+1, " : ", Operating_time[i], end = " ")
    total_time = 0
    for d in Operating_time[i] :
        total_time += d
    print(f"Total time {i + 1} : {total_time:.3f}", end = "\n") 

for i in range(len(Distance)):
    print("Robot distance ", i+1, " : ", Distance[i], end = " ")
    total_distance = 0
    for d in Distance[i] :
        total_distance += d
    print("Total distance ", i+1, " : ", total_distance, end = "\n")

tag_target = 1
for i in Object_in_target :
    print(f'Target {tag_target} : {i}')
    tag_target += 1
    

pygame.quit()