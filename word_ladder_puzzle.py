# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwxyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle.
    === Private attributes ===
    @type _words: list[str]
        List of allowed English words
    @type _start: str
        Initial state of puzzle
    @type _target: target 
        Goal state of puzzle
    @type _hist : tuple
        Past words seen before 'start'    
    
    """
    def __init__(self, start, target, hist):
        """Create a new word ladder puzzle with given start and target words.

        Note: you may add OPTIONAL arguments to this constructor,
        but you may not change the purpose of <start> and <target>.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('wordsEn.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())
        self._start = start
        self._target = target
        self._hist = hist
        self._current = start

        # TODO: Complete the constructor.

    def __str__(self):
        """Please do not change this
        """
        return ' '.join(self._hist)

    def is_solved(self):
        return self._current == self._target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        total = []
        for index in range(len(self._current)):
            for char in CHARS:
                cur = list(self._current)
                cur[index] = char
                new = "".join(cur)
                if (new in self._words) and (new not in self._hist):
                    new_state = WordLadderPuzzle(new, self._target, self._hist)
                    total.append(new_state)
        return total


    def move(self, new_word):
        possible_states = self.extensions()
        new_state = WordLadderPuzzle(new_word, self._target, self._hist)
        if new_state not in possible_states: return False
        return new_state





