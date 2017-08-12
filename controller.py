# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth

# class Node:
#     def __init__(self, puzzle = None, user_input = None, parent = None):
#         self._value = (puzzle, user_input)
#         self._parent = None
#     def set_parent(self, node):
#         self._parent = node
#
class Tree:
    def __init__(self, puzzle=None, user_input=None, parent=None):
        self._root = (puzzle, user_input)
        self._subtrees = []
        self._parent = parent

    def is_empty(self):
        return not self._root

    def set_root(self, puzzle):
        self._root = puzzle

    def show_puzzle(self):
        return self._root[0]

    def add_move(self, puzzle, user_input, parent):
        new_tree = Tree(puzzle, user_input, parent)
        for tree in self._subtrees:
            if str(new_tree._root[0]) == str(tree._root[0]) and new_tree._root[1] == tree._root[1]:
                return tree
        new_tree._parent = self
        self._subtrees.append(new_tree)
        return new_tree

    def undo(self):
        if not self._parent:
            return "This is where you started! Can't undo from here."
        return self._parent

    def attempts(self):
        if not self._subtrees: return "You have made no attempts from this stage."
        attempts = []
        for tree in self._subtrees:
            string = "STATE: \n"
            string += "MOVE: ".join((str(tree._root[0]), tree._root[1]))
            attempts.append(string)
        return attempts











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
        self._current = Tree(puzzle, "")
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
            return str(solution), True
        elif action == ":SOLVE-ALL":
            solution = solve_complete(self._puzzle)
            solution2 = [str(x) for x in solution]
            with_new = list(map(lambda x: x+"\n", solution2))
            final = "".join(with_new)
            return final, True
        elif action == ":UNDO":
            result = self._current.undo()
            if isinstance(result, str): return result, False
            self._current = result
            self._puzzle = result.show_puzzle()
            return self.state(), False
        elif action == ":ATTEMPTS":
            attempts = self._current.attempts()
            if attempts[:3] == "You": return (attempts, False)
            total = "\n".join(attempts)
            return (total, False)
        elif ":HINT" in action and int(action.rstrip()[-1]) >= 1:
            return hint_by_depth(self._puzzle, int(action.rstrip()[-1])), False
        elif isinstance(action, str) and action != "":
            valid_move = self._puzzle.move(action)
            if not valid_move: return "This move is invalid.", False
            self._current = self._current.add_move(valid_move, action, self._current)
            self._puzzle = self._current.show_puzzle()
            if valid_move.is_solved():
                return valid_move, True
            return valid_move, False
        else:
            return self.state(), False


if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle

    s = SudokuPuzzle(
        [['E', 'C', '', '', 'G', '', '', '', ''],
         ['F', '', '', 'A', 'I', 'E', '', '', ''],
         ['', 'I', 'H', '', '', '', '', 'F', ''],
         ['H', '', '', '', 'F', '', '', '', 'C'],
         ['D', '', '', 'H', '', 'C', '', '', 'A'],
         ['G', '', '', '', 'B', '', '', '', 'F'],
         ['', 'F', '', '', '', '', 'B', 'H', ''],
         ['', '', '', 'D', 'A', 'I', '', '', 'E'],
         ['', '', '', '', 'H', '', '', 'G', 'I']]
    )
    c = Controller(s)
