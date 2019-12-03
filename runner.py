"""Sidescrolling runner game"""

import random

import pygame

# Init pygame
pygame.init()

class Block(pygame.sprite.Sprite):
    """General block that is run past"""

    def __init__(self, rect: pygame.Rect):

        # Call super initator to be able to interact with pygame sprite tools
        super().__init__()

        # Reference rect
        self.rect = rect

        # Create image
        self.image = pygame.Surface(self.rect.size)

        # Background fill the image with white for now
        self.image.fill((255, 255, 255))

    def update(self):
        """Moves the block by the given speed"""
        self.rect.x -= 5

        # Delete at edge
        if self.rect.right <= 0:
            self.kill()

# Create clock
clock = pygame.time.Clock()

# Setup window
# TODO should create and use config values
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Runner")
tps = 60

# Initiate block group
blocks = pygame.sprite.Group()

# The length of a full cycle of game logic in ticks (e.g. producing new blocks)
cycle_length = 60

# Main loop
running = True
tick = -1
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

        # Increment tick
        tick = (tick + 1) % cycle_length

        # Create new block every 10 ticks
        if tick % 5 == 0:
            blocks.add(Block(pygame.Rect(400, random.randint(0, 15)*25, 25, 25)))

        # Update blocks
        blocks.update()

        screen.fill((0, 0, 0))
        blocks.draw(screen)

        # Flip display
        pygame.display.flip()
        # Limit to determined tps
        clock.tick(tps)
