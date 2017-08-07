# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete

class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        # TODO: Add to this method to handle different actions.
        if action == ':EXIT':
            return ('', True)
        elif action == ":SOLVE":
            solution = solve(self._puzzle)
            return (str(solution), True)
        elif action == ":SOLVE-ALL":
            solution = solve_complete(self._puzzle)
            solution2 = [str(x) for x in solution]
            with_new = list(map(lambda x: x+"\n", solution2))
            final = "".join(with_new)
            return (final, True)
        elif isinstance(action, str):
            valid_move = self._puzzle.move(action)
            if not valid_move: return "This move is invalid."
            self._puzzle = valid_move
            if valid_move.is_solved():
                return (valid_move, True)
            return (valid_move, False)
        else:
            return (self.state(), False)


if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle

    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])
    c = Controller(s)
