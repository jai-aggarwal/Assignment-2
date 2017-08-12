# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    all_states = []
    next_states = puzzle.extensions()
    final = None
    for state in next_states:
        if final: return final
        all_states.append(state)
        if state.is_solved():
            if verbose:
                final = all_states
                return final
            final = all_states[-1]
            return final
        else:
            final = solve(state, verbose)
    if verbose:
        for i in all_states:
            print(i)
    return final

def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """
    all_solutions = []
    all_states = []
    next_states = puzzle.extensions()
    for state in next_states:
        all_states.append(state)
        if state.is_solved():
            all_solutions.append(state)
        else:
            all_solutions.extend(solve_complete(state, verbose))
    return all_solutions

def _helper_hint_by_depth(puzzle, n):
    """ Return True if there is a soultion within or at n steps

    Precondition: n >= 1.

    @type puzzle: Puzzle
    @type n: int
    @rtype: bool
    """
    found = False
    if n >= 1:
        for i in puzzle.extensions():
            if i.is_solved():
                found = True
            else:
                found = hint_by_depth(i, n - 1)
    # else n < 1 and solutions beyond n !!
    return found


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string ’Already at a solution!’
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string ’No possible extensions!’

    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    elif not solve(puzzle):
        return 'No possible extensions!'
    else:
        x = puzzle.extensions()
        for i in x:
            if _helper_hint_by_depth(i, n - 1):
                return str(i)
        return str(x[0])



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

    solution = solve_complete(s)
    print(solution)
    for i in solution:
        print(i)
    """

    from word_ladder_puzzle import WordLadderPuzzle
    w = WordLadderPuzzle("make", "cure")
    solution = solve(w)
    print(solution)"""
