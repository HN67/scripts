"""Sidescrolling runner game"""

# Import core modules
import os
import typing
import random

# Import pygame
import pygame

# Define config
config = {
    "windowWidth": 500,
    "windowHeight": 500,
    "name": "Runner",
}

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
        # TODO maybe make blocks deload away from screen or something
# Define viewbox
class Viewbox:
    """Represents the view of the game, mainly for displacement"""

    def __init__(self, rect: pygame.Rect):

        # Reference rect
        self.rect = rect

        # Create surface
        self.image = pygame.Surface(self.rect.size)

    def render(self, sprites: pygame.sprite.Group) -> None:
        """Draws the given sprites (as a Group) onto the surface
        Adjusts position based on viewbox offset
        """
        # Access each sprite individually for offsetting
        for sprite in sprites:
            # Moves the sprites the opposite direction of viewbox location,
            # so as the viewbox "moves", the sprites are moved onto it
            # e.g. viewbox offset: (5, 5) will make a sprite at (5, 5) be drawn at (0, 0)
            self.image.blit(sprite.image, sprite.rect.move(-self.rect.x, -self.rect.y))

# Create viewbox
viewbox = Viewbox(pygame.Rect(0, 0, config["windowWidth"], config["windowHeight"]))

# Create clock
clock = pygame.time.Clock()

# Setup window
screen = pygame.display.set_mode(viewbox.rect.size)
pygame.display.set_caption(config["name"])
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

    # Check other sources of input, e.g. the keyboard
    held_keys = pygame.key.get_pressed()

    # Control the viewbox from out here for now
    if held_keys[pygame.K_UP]:
        viewbox.rect.y -= 5
    if held_keys[pygame.K_DOWN]:
        viewbox.rect.y += 5
    if held_keys[pygame.K_LEFT]:
        viewbox.rect.x -= 5
    if held_keys[pygame.K_RIGHT]:
        viewbox.rect.x += 5

    # Skips the rest of the loop if the program is quitting
    if running:

        # Create new block every other space based on width ticks
        if tick % 200 == 0:
            blocks.add(Block((random.randint(0, 9)*50, random.randint(0, 9)*50), images["block"]))

        # Update blocks
        blocks.update()

        # Refresh the viewbox
        # Fill over old image
        viewbox.image.fill((100, 100, 100))
        # Render the blocks into the viewbox
        viewbox.render(blocks)

        # Slap the viewbox onto the screen
        screen.blit(viewbox.image, (0, 0))

        # Flip display
        pygame.display.flip()

        # Increment tick
        tick = (tick + 1)# % cycle_length
        # Limit to determined tps
        clock.tick(tps)
