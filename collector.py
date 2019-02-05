# HN67 Collector Game programmed with Tkinter in Python

# Import modules
import tkinter as Tk

# Tile data holder class
class Tile:
    
    def __init__(self, resource: str, stage: int = 0):
        
        self.resource = resource
        self.stage = stage

# Abstract overhead game data class
class Game:

    # Constructor
    def __init__(self, size: int,
                 maxTileLevel: int = 3,
                 upgradeCosts: list = [{"metal":5},
                                       {"metal":10},
                                       {"metal":20}],
                 startingResources: dict = {"metal": 0,
                                            "crystal": 0,
                                            "fuel": 0}
                ):

        # Create tiles
        self.tiles = {}

        for x in range(size):
            for y in range(size):
                self.tiles[(x,y)] = Tile("metal")

        # Define resource stockpile stuff
        self.resources = startingResources

# Game controller class
class Controller:

    # Constructor to get reference
    def __init__(self, game: Game):
        
        self.game = game

    # Increments game state
    def tick(self):
        pass

    def upgrade_tile(self, x, y):
        pass

    def downgrade_tile(self, x, y):
        pass

# Main app class
class Main:

    def __init__(self):
        
        # Create root
        self.root = Tk.Tk()

