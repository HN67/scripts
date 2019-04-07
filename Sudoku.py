"""Contains Sudoku data structures and manipulation methods"""

from dataclasses import dataclass

@dataclass
class Tile:
    """Stores the value and box position of a tile"""
    
    value: int
    row: int
    column: int
    box: int

class Sudoku:
    """Stores a Sudoku board state and can operate on it"""

    def __init__(self):

        # Reference size (static 9 (3x3 boxes) for now)
        self.size = 9
        self.boxWidth = 3
        self.boxHeight = 3

        # Create the board dictionary
        self.board = {}

        # Create specific containers
        self.rows = {}
        self.columns = {}
        self.boxes = {}

        # Populate the board with empty tiles
        for row in range(self.size):
            for column in range(self.size):

                # Determine box number
                box = self.get_box(row, column)

                # Create tile
                tile = Tile(0, row, column, box)

                # Add tile to various containers
                self.board[row, column] = tile

                # Either add or create the row container
                try:
                    self.rows[row].append(tile)
                except KeyError:
                    self.rows[row] = [tile]

                # Either add or create the column container
                try:
                    self.columns[column].append(tile)
                except KeyError:
                    self.columns[column] = [tile]

                # Either add or create the box container
                try:
                    self.boxes[box].append(tile)
                except KeyError:
                    self.boxes[box] = [tile]

    def set_value(self, row, column, value):
        """Set the value at a position"""
        self.board[row, column].value = value

    def value(self, row, column):
        """Return the value at a position"""
        return self.board[row, column].value

    def get_box(self, row, column):
        """Returns the box number of a row,column position"""
        return (column // self.boxWidth) + ((self.size // self.boxWidth) * (row // self.boxHeight))

    def invalid_choices(self, row, column):
        """Returns a set of numbers that would be invalid to place at this position"""

        # Assemble the values that already exist in the box, row and column
        values = set()
        for tile in self.rows[row]:
            values.add(tile.value)
        for tile in self.columns[column]:
            values.add(tile.value)
        for tile in self.boxes[self.get_box(row, column)]:
            values.add(tile.value)

        return values

    def valid_choices(self, row, column):
        """Returns a set of numbers that would be valid to place at this position"""

        # Valid is the set of possible - set of invalid
        # Find the invalid possibilities
        invalid = self.invalid_choices(row, column)

        # possible numbers range from [1, self.size], inclusive (e.g. 1-9 normally)
        possible = set(range(1, self.size + 1))

        # Subtract the sets to find what is valid
        return possible - invalid

def main():

    sudo = Sudoku()

    for tile in sudo.board:
        print(tile, sudo.board[tile].box, sudo.board[tile].value)

    print(sudo.invalid_choices(3, 3))
    print(sudo.valid_choices(3, 3))

if __name__ == "__main__":
    main()