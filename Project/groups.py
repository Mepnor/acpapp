import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Camera Example")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Robot class
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(400, 300))
        self.speed = 5

    def update(self, keys):
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Move the entity's position by the negative camera position
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        # Center the camera on the target (robot)
        x = target.rect.centerx - SCREEN_WIDTH // 2
        y = target.rect.centery - SCREEN_HEIGHT // 2

        # Keep the camera within the bounds of the level
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Main function
def main():
    clock = pygame.time.Clock()
    
    # Create a robot instance
    robot = Robot()
    robot_group = pygame.sprite.Group(robot)

    # Create a camera
    camera = Camera(1600, 1200)  # Assuming a level size of 1600x1200

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        robot.update(keys)
        camera.update(robot)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the robot
        for sprite in robot_group:
            screen.blit(sprite.image, camera.apply(sprite))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
