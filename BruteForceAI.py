"""Module containing classes and functions to train an AI through Brute Force on simple games"""
# Brute Force AI
# Author: HN67

# Import native libraries
# For the AI to choose randomly
import random
# For saving and loading AI histories
import pickle
import os

# Set current directory to where this file is located
os.chdir(os.path.dirname(__file__))

class TTTBoard:
    """Class for holding and manipulating a TicTacToe board"""

    def __init__(self, size):

        # Reference board size
        self.size = size

        # Create board
        self.reset()

    def reset(self):
        """Resets the board"""
        # Create board
        self.board = {}
        self.filled = {}

        # Populate the dictionaries with (row, column) tuples
        for row in range(self.size):
            for column in range(self.size):
                self.board[row, column] = " "
                self.filled[row, column] = False

    def place(self, position: tuple, symbol: str):
        """Place a symbol at the specificed position (given as an x,y tuple)"""

        self.board[position] = symbol
        self.filled[position] = True

    def get_available(self):
        """Returns a set of tuples of free spaces"""

        return set(space for space in self.filled if not self.filled[space])

    def __str__(self):

        return "\n".join((
            " ".join(self.board[0, x] for x in range(3)),
            " ".join(self.board[1, x] for x in range(3)),
            " ".join(self.board[2, x] for x in range(3)),
        ))

    def check_wins(self):
        """Returns a set of which symbols form a solid line on the board"""
        wins = set()
        # Check each row
        for row in range(self.size):
            if all_same(self.board[row, column] for column in range(self.size)):
                wins.add(self.board[row, 0])
        # Check each column
        for column in range(self.size):
            if all_same(self.board[row, column] for row in range(self.size)):
                wins.add(self.board[0, column])
        # Check each diagonal
        # Topleft to bottomright
        if all_same(self.board[spot, spot] for spot in range(self.size)):
            wins.add(self.board[0, 0])
        # Bottomleft to topright
        if all_same(self.board[self.size - 1 - spot, spot] for spot in range(self.size)):
            wins.add(self.board[self.size - 1, 0])
        # Return
        if " " in wins:
            wins.remove(" ")
        return wins

    def tuple_form(self):
        """Returns a two dimensional tuple representing the board
        (dict[row, column] -> tuple[row][column])
        """

        return tuple(
            tuple(self.board[row, column] for column in range(self.size))
            for row in range(self.size)
        )


def all_same(container):
    """Checks if all the elements of the container are identical"""
    return len(set(container)) <= 1

class TTTAI:
    """AI to learn TicTacToe, should be extended to more general"""

    def __init__(self, symbol):

        self.symbol = symbol

        self.history = {}

        self.gameHistory = []

    def play(self, tttBoard: TTTBoard):
        """Plays a possible move based on game state"""

        # Reference the current board state
        currentState = tttBoard.tuple_form()

        # If the board state has not been encountered before:
        # Add it to history with a set of possible moves (generated) that will be improved
        if currentState not in self.history:
            self.history[currentState] = tttBoard.get_available()

        # Make sure there is valid moves to prevent runtime error
        try:
            # Play one of the possible moves
            move = random.choice(list(self.history[currentState]))

            # Place the move
            tttBoard.place(move, self.symbol)

            # Save the move made this turn
            self.gameHistory.append({"state": currentState, "move": move})
        except IndexError:
            pass #?

    def evaluate(self, tttBoard: TTTBoard):
        """Makes the AI evaluate the game state and learn, returns True if game is over"""

        # Find last move on what state
        last = self.gameHistory[-1]

        # Reference the current board state
        currentState = tttBoard.tuple_form()

        # If the board state has not been encountered before:
        # Add it to history with a set of possible moves (generated) that will be improved
        if currentState not in self.history:
            self.history[currentState] = tttBoard.get_available()

        # Check for victory, if so then always make last move
        if self.symbol in tttBoard.check_wins():
            self.history[last["state"]] = {last["move"]}
            # Signal end of game
            return True

        # Check if the AI has lost
        elif (
                # Actual loss (another symbol that isnt the AI's won)
                (len(tttBoard.check_wins()) > 0 and self.symbol not in tttBoard.check_wins())
                # No possible good moves (all cause a loss) and not a full board stalemate
                or (len(self.history[currentState]) < 1 and len(tttBoard.get_available()) > 0)
            ):
            # Remove the losing move
            self.history[last["state"]].remove(last["move"])
            # Signal end of game
            return True

        # Check if it was a tie
        elif len(tttBoard.get_available()) == 0:
            return True

        # Didnt lose or win, game not over
        return False

    def reset(self):
        """Resets the AI's knowledge of the current game (i.e. game history)"""
        self.gameHistory = []

board = TTTBoard(3)

print(board.get_available())
print(board.tuple_form())

# Load the first AI x, or create new if it doesnt exist
try:
  with open("ai1.pickle", "rb") as f:
    ai1 = pickle.load(f)
except FileNotFoundError:
  ai1 = TTTAI("x")

# Load the second AI o, or create new if it doesnt exist
try:
  with open("ai2.pickle", "rb") as f:
    ai2 = pickle.load(f)
except FileNotFoundError:
  ai2 = TTTAI("o")

# Teach the AIs
def teach(first: TTTAI, second: TTTAI, moves: int=1000):

  for i in range(moves):

    # Play and evaluate AI 1
    ai1.play(board)
    #print(board, end="\n\n")
    done1 = ai1.evaluate(board)

    # Let player 2 go if game isnt already over
    if not done1:
        ai2.play(board)
        #print(board, end="\n\n") 

    # Recheck both evaluations
    done1 = ai1.evaluate(board)
    done2 = ai2.evaluate(board)

    # Reset if game over
    if done1 or done2:
        #print("VICTORY", board.check_wins())
        ai1.reset()
        ai2.reset()
        board.reset()

      # Pause
      #input(":")

  # Save the AIs
  with open("ai1.pickle", "wb") as f:
      pickle.dump(ai1, f)

  with open("ai2.pickle", "wb") as f:
      pickle.dump(ai2, f)

# User Interface

# Start the main loop
userInput = ""
while True:

    userInput = input("Which AI do you want to check (or enter 'teach' to run a learning session): ")
    if userInput == "x":
        ai = ai1
    elif userInput == "o":
        ai = ai2
    elif userInput == "teach":
        try:
            amount = int(input("How many moves? "))
        except ValueError:
            print("Invalid number")
            continue
        teach(ai1, ai2, amount)
        continue
    elif userInput == "break":
        break
    else:
        print("Invalid input: Expected ['x', 'o', 'break']")
        continue
    
    userInput = input("Enter a board state to check: ")
    
    try:
        state = (tuple(userInput[:3]), tuple(userInput[3:6]), tuple(userInput[6:9]))
        print(ai.history[state])
    except (IndexError, KeyError):
        print("Invalid input: Expected 9*['x', 'o', ' '] or AI has no knowledge of that board yet")
        continue