"""Drawing toolkit based on PyGame to mostly visualize mathematical models"""

# Imports
from __future__ import annotations

import math
import typing
import logging

import pygame

# Config dictionary
config = {
    "screen": {
        "dimensions": (400, 400),
        "color": pygame.Color("white"),
        "name": "Model",
    },
    "app": {
        "tps": 60,
    },
    "logging": {
        "level": logging.WARNING,
    },
}

# Set logging level
logging.getLogger().setLevel(config["logging"]["level"])

Pair = typing.Tuple[float, float]

class Point:
    """Object representing two dimensional point\n
        Can be constructed with two numerical parameters, or a single two-element numerical tuple
    """

    def __init__(self, x: typing.Union[Pair, float], y: float = None):
        if y is None:
            # Take single parameter as component pair
            self.position = (x[0], x[1])
        else:
            self.position = (x, y)

    @property
    def x(self):
        """First component of the Point position"""
        return self.position[0]

    @property
    def y(self):
        """Second component of the Point position"""
        return self.position[1]

    def __getitem__(self, key: int):
        """Returns a component of the Point"""
        return self.position[key]

    def __add__(self, other: typing.Union[Point, Pair]):
        """Adds each component of the point independently
            (x1, y1) + (x2, y2) => (x1 + x2, y1 + y2)
        """
        # Allow interacting with tuple
        if isinstance(other, (Point, tuple)):
            return Point(self.position[0] + other[0], self.position[1] + other[1])

        # Invalid type
        return NotImplemented

    def __radd__(self, other: typing.Union[Point, Pair]):
        return self.__add__(other)

    def __sub__(self, other: typing.Union[Point, Pair]):
        """Subtracts each component of the point independently
            (x1, y1) - (x2, y2) => (x1 - x2, y1 - y2)
        """
        # Allow interacting with tuple
        if isinstance(other, (Point, tuple)):
            return Point(self.position[0] - other[0], self.position[1] - other[1])

        # Invalid type
        return NotImplemented

    def __rsub__(self, other: typing.Union[Point, Pair]):
        return self.__sub__(other)

    def __neg__(self):
        """Negates each component of the point
            (x, y) => (-x, -y)
        """
        return Point(-self.position[0], -self.position[1]) #pylint: disable=invalid-unary-operand-type

    def __mul__(self, other: float):
        """Multiplies each component by a scalar
            (x, y) * c => (x*c, y*c)
        """
        return Point(-self.position[0] * other, self.position[1] * other)

    def __rmul__(self, other: float):
        return self.__mul__(other)

    def __truediv__(self, other: float):
        """Divides each component by a scalar
            (x, y) / c => (x/c, y/c)
        """
        return Point(-self.position[0] / other, self.position[1] / other)

    def __rtruediv__(self, other: float):
        return self.__truediv__(other)

class Panel:
    """Surface wrapper to provide additional functionality and abstractness
        All drawing methods are relative to the given origin based on orientation
    """

    def __init__(self, surface, origin: typing.Union[Point, Pair] = Point(0, 0),
                 orientation: typing.Union[Pair, Point] = Point(1, 1)):

        # Get surface to wrap from passed argument
        self.surface = surface

        # Reference origin
        self.origin = Point(origin)

        # Reference orientation
        self.orientation = Point(orientation)

    def convert(self, point: Point):
        """Converts a theoretical Point into the position to be drawn on the pygame Surface\n
            Based on Panel origin and orientation
        """
        return self.origin + Point(point.x * self.orientation.x, point.y * self.orientation.y)

    def clear(self, color: pygame.Color = pygame.Color(0, 0, 0)):
        """Clears the Panel to a specified blank color"""
        self.surface.fill(color)

    def draw_line(self, start: typing.Union[Point, Pair], end: typing.Union[Point, Pair],
                  color: pygame.Color = pygame.Color(255, 255, 255)):
        """Provides an easier but limited interface to pygame.draw.line(self.surface, ...)"""
        pygame.draw.line(
            self.surface, color,
            self.convert(start).position, self.convert(end).position
        )

    def display(self, surface: pygame.Surface, position: typing.Tuple[int, int]):
        """Displays the panel on a surface by blitting it"""
        surface.blit(self.surface, position)

def radial(length: float, angle: float) -> Point:
    """Returns a Point representing the position reached\n
       by travelling the given distance at the given angle in radians.\n
       Assumes clockwise rotation from eastward vector in a v> positive plane
    """
    # Standard vector calculations for horizontal and vertical
    return Point(length * math.cos(angle), length * math.sin(angle))

class Model:
    """Abstrac Class representing a mathematical model, designed to be represented on a Panel"""

    def update(self):
        """Updates the model to the next stage, if the model is dynamic"""
        return

    def visual(self) -> Panel:
        """Returns a Panel containing a visual representation of the Model"""
        raise NotImplementedError

class Manager:
    """Abstract Class that gets pygame events and screen and manages a Model on it"""

    def __init__(self, model: Model, screen: pygame.Surface):

        # Reference model and screen for later use
        self.model = model
        self.screen = screen

    def update(self, events, keyboard):
        """Updates the Manager with the given events and keyboard press state
        The manager should use the events to update the model,
        and then redraw the updated model
        """
        raise NotImplementedError

class Stargon(Model):
    """Represents the concave form of an 'order' sided polygon"""

    def __init__(self, radius, order):
        # Reference parameters
        self.radius = radius
        self.order = order

    def visual(self):
        # Create a panel 2x the radius, and give it a central origin and standard orientation
        drawing = Panel(
            pygame.Surface((self.radius*2, self.radius*2)),
            origin=Point(self.radius, self.radius), orientation=(1, -1)
        )
        # Draw each line of the stargon, reaching from a point to the second next point
        for i in range(self.order):
            drawing.draw_line(
                radial(self.radius, i*2*math.pi/self.order + math.pi/2),
                radial(self.radius, (i+2)*2*math.pi/self.order + math.pi/2)
            )
        # Return the panel
        return drawing

class StargonManager(Manager):
    """Manager Class for the Stargon Model"""

    def update(self, events, keyboard):
        """UP/DOWN arrowkeys change order, Holding LEFT/RIGHT change size"""

        # Search for UP/DOWN
        for event in events:

            # Check KEYDOWN events
            if event.type == pygame.KEYDOWN:

                # Match against Up and Down constants
                if event.key == pygame.K_UP:
                    self.model.order += 1
                elif event.key == pygame.K_DOWN:
                    self.model.order -= 1

        # Search for held LEFT/RIGHT keys
        if keyboard[pygame.K_LEFT]:
            self.model.radius -= 1
        if keyboard[pygame.K_RIGHT]:
            self.model.radius += 1

        # Refresh the display
        image = self.model.visual()
        # Find blit coordinate to place in the middle
        # Reference both rects to manipulate them
        screenRect = self.screen.get_rect()
        imageRect = image.surface.get_rect()
        # Center imageRect on screenRect
        imageRect.center = screenRect.center
        # Draw the image, which should be centered
        image.display(self.screen, (imageRect.x, imageRect.y))

def main():
    """Main function to start the script"""

    # Initialize pygame
    pygame.init()

    # Reference output screen
    screen = pygame.display.set_mode(config["screen"]["dimensions"])
    pygame.display.set_caption(config["screen"]["name"])

    # Create clock
    clock = pygame.time.Clock()

    # Set the background color
    screen.fill(config["screen"]["color"])

    # Create a Stargon Manager
    manager = StargonManager(Stargon(200, 9), screen)

    # Event loop
    running = True
    while running:

        # Retrieve pygame event queue to allow multiple viewings
        # (since pygame.event.get() will clear the queue whenever used)
        events = pygame.event.get()

        # Show information around events
        if events:
            logging.info(events)

        # Iterate through events on top-level for specific situations
        # such as QUIT
        for event in events:

            # Allow window closure by ending main while loop
            if event.type == pygame.QUIT:
                running = False

        # Only continue if program hasnt been terminated
        if running:

            # Clear the background
            screen.fill(config["screen"]["color"])

            # Update manager to allow for interactive input
            manager.update(events, pygame.key.get_pressed())

            # Flip pygame display to actually show changes
            pygame.display.flip()

            # Limit the speed of ticks
            clock.tick(config["app"]["tps"])

if __name__ == "__main__":
    main()
