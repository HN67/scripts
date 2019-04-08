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

    def empty_tiles(self):
        """Returns all tiles that are empty; in a list with no specific order"""
        return [tile for tile in self.board.values() if tile.value == 0]

    def copy(self):
        """Returns a copy of this Sudoku board"""

        # Create the new, empty board
        new = Sudoku()

        # Copy the value of each tile over
        for position, tile in self.board.items():
            new.set_value(*position, tile.value)

        # Return the copy
        return new

    def solve(self):
        """Attempts to solve this sudoku
        Returns True if sucsesfull, and mutates the board to solved
        Returns False if unsucsesfull, and leaves the board in original state
        """

        # Find all the empty (modifiable) tiles
        spaces = self.empty_tiles()

        # cursor is a pointer to the current space being manipulated
        cursor = 0

        # Solve the sudoku until every space has been solved
        while cursor < len(spaces) or cursor == -1:

            # Increase the value at the cursor
            value = spaces[cursor].value + 1

            # If the value is valid, set it and move on to the next tile
            if value in self.valid_choices(spaces[cursor].row, spaces[cursor].column):
                spaces[cursor].value = value
                cursor += 1
            # If invalid, still set it for now, will be incremented next turn
            else:
                spaces[cursor].value = value

            # Check if the value has overflowed (there were no possible values)
            if value > self.size:
                # Reset (clear) this tile
                spaces[cursor].value = 0
                # Move back
                cursor -= 1

            #print(cursor, value)

        # Check if solving was unsucsessful
        if cursor == -1:
            return False
        else:
            return True

    def __str__(self):
        """Returns a string representation of the board state"""

        # Create a 2d array of lists
        output = []

        # Add the values into the 2d list
        for row in range(self.size):

            # Add horizontal seperator every boxHeight
            if row % self.boxHeight == 0 and row != 0:
                output.append("")

            # Prepare current row
            output.append([])

            for column in range(self.size):

                # Add vertical bar every boxWidth
                if column % self.boxWidth == 0 and column != 0:
                    output[-1].append(" ")

                # Replace 0 with a _
                if self.value(row, column) == 0:
                    output[-1].append("-")
                else:
                    output[-1].append(str(self.value(row, column)))

        # Join each row into a string
        output = [" ".join(row) for row in output]

        # Join all the rows with \n between them
        return "\n".join(output)



def main():
    """Main function for testing"""

    # Create test board
    sudo = Sudoku()

    # Populate test board
    sudo.set_value(3, 3, 5)
    sudo.set_value(5, 5, 6)
    sudo.set_value(0, 8, 1)
    sudo.set_value(8, 0, 7)

    # Show test board
    print(sudo)

    # Solve test board
    sudo.solve()

    # Seperate before/after
    print()
    # Show solved board
    print(sudo)

if __name__ == "__main__":
    main()
