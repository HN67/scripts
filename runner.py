"""Sidescrolling runner game"""

# Import core modules
import os
import typing
import random

# Import pygame
import pygame

# Define path function that turns a relative path into an absolute path based on file location
def path(local: str) -> str:
    """Returns the absolute path of local path, based on this file location"""
    return os.path.join(os.path.dirname(__file__), local)

# Init pygame
pygame.init()

class Block(pygame.sprite.Sprite):
    """General block that is run past"""

    def __init__(self, position: typing.Tuple[int, int], image: pygame.Surface):

        # Call super initator to be able to interact with pygame sprite tools
        super().__init__()

        # Reference image
        self.image = image

        # Create rect
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        """Moves the block by the given speed"""
        self.rect.x -= 5

        # Delete at edge
        if self.rect.right <= 0:
            self.kill()

# Create clock
clock = pygame.time.Clock()

# Define viewbox
viewbox = pygame.Rect(0, 0, 500, 500)

# Setup window
# TODO should create and use config values
screen = pygame.display.set_mode(viewbox.size)
pygame.display.set_caption("Runner")
tps = 60

# Load images
images = {
    "block": pygame.image.load(path("block.png")).convert()
}

# Initiate block group
blocks = pygame.sprite.Group()

# Main loop
running = True
tick = 0
while running:

    # Dump event queue into reference
    events = pygame.event.get()

    # Check for interesting events
    for event in events:

        # QUIT event comes from closing the window, etc
        if event.type == pygame.QUIT:
            running = False

    # Skips the rest of the loop if the program is quitting
    if running:

        # Create new block every other space based on width ticks
        if tick % 20 == 0:
            blocks.add(Block((500, random.randint(0, 9)*50), images["block"]))

        # Update blocks
        blocks.update()

        screen.fill((100, 100, 100))
        blocks.draw(screen)

        # Flip display
        pygame.display.flip()

        # Increment tick
        tick = (tick + 1)# % cycle_length
        # Limit to determined tps
        clock.tick(tps)
