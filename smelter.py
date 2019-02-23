# HN67 Collector Game programmed with Tkinter in Python

# Import modules
import tkinter as Tk
from dataclasses import dataclass

# Resources data class
# Can be attached to tile, game, etc
@dataclass
class Resource:

    name: str # Maybe create an enum of some sort instead of strings?
    amount: int # Int makes sense, though maybe float?


# System data class (temperature and contents)
# Should it be hardcoded or made up of 'Resource's?
@dataclass
class System:

    temperature: int #or float?



# Should a list of resources be a) a list, b) a set <- most likely, or c) a custom class?
# One Issue with set is the neccesity to check for keys all the time
# A class could creat unneccesary rigor if not done properly

# Tile data holder class
class Tile:
    
    def __init__(self, systems: set = None):
        
        self.systems = systems

# Abstract overhead game data class
class Game:

    # Constructor
    def __init__(self, size: int):

        # Create tiles
        self.tiles = {}

        for x in range(size):
            for y in range(size):
                self.tiles[(x,y)] = Tile()


# Game controller class
class Controller:

    # Constructor to get reference
    def __init__(self, game: Game):
        
        self.game = game

    # Increments game state
    def tick(self):
        pass


# Main app class
class Main:

    def __init__(self):
        
        # Create root
        self.root = Tk.Tk()

