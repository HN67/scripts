"""Sidescrolling runner game"""

# Import core modules
import os
import typing
import random

# Import pygame
import pygame

# Define config
config = {
    "windowWidth": 512,
    "windowHeight": 512,
    "tps": 60,
    "name": "Runner",
    "blockSize": 32,
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
        """Updates the block"""
        # TODO maybe make blocks deload away from screen or something

    @property
    def hitbox(self) -> pygame.Rect:
        """Allow access of .rect under the name of .hitbox"""
        return self.rect

class Player(pygame.sprite.Sprite):
    """Main controllable character of the game
    Player(image: Surface, hitbox: Rect, keyConfig: dict)
    keyConfig is a {str: int} dictionary that maps names to keycodes
    Currently requires "jump", "left", "right" keyConfigs
    Use Player.keyDictionary to automatically generate a compatible dictionary
    """

    @classmethod
    def keyDictionary(cls, jump: int, left: int, right: int) -> typing.Dict[str, int]:
        """Automatically produces a keyConfig in the format expected by the constructor"""
        return {"jump": jump, "left": left, "right": right}

    def __init__(self, image: pygame.Surface,
                 hitbox: pygame.Rect, keyConfig: typing.Dict[str, int]
                ):

        # Reference image
        self.image = image

        # Reference hitbox
        self.hitbox = hitbox

        # Generate rect from hitbox, starting centered on the hitbox
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center

        # Reference keyConfig
        self.keyConfig = keyConfig

    def update(self):
        """Updates the player"""

        # Align visual rect with actual hitbox
        self.rect.center = self.hitbox.center

def hitboxCollided(sprite: pygame.sprite.Sprite, other: pygame.sprite.Sprite) -> bool:
    """Collides sprites based on their .hitbox attribute instead of .rect"""
    return sprite.hitbox.colliderect(other.hitbox)

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
tps = config["tps"]

# Load images
images = ("block", "player")
# Convert loaded surfaces to screen format
images = {name: pygame.image.load(path(name+".png")).convert() for name in images}

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
            blocks.add(Block(
                (
                    random.randint(
                        0, config["windowWidth"]//config["blockSize"] - 1
                    )*config["blockSize"],
                    random.randint(
                        0, config["windowHeight"]//config["blockSize"] - 1
                    )*config["blockSize"]
                ),
                images["block"]))

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
