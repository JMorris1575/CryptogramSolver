class Collection():

    def __init__(self, name="", author="", puzzles=[]):
        self._name = name
        self._author = author
        self._puzzles = puzzles

    def __str__(self):
        return "Collection: " + self._name + ", by " + self._author + " has " + str(len(self._puzzles)) + " puzzles."

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def author(self):
        return self._author

    def setAuthor(self, author):
        self._author = author

    def puzzles(self):
        return self._puzzles

    def setPuzzles(self, puzzles):
        self._puzzles = puzzles

    def addPuzzle(self, puzzle):
        print("Got to Collection.addPuzzle()")
        self._puzzles.append(puzzle)


class Puzzle():

    def __init__(self, puzzleTitle=None, puzzleCode=None, citationCode=None,
                 puzzleSolution=None, citationSolution=None, hints=[]):
        self._puzzleTitle = puzzleTitle
        self._puzzleCode = puzzleCode
        self._citationCode = citationCode
        self._puzzleSolution = puzzleSolution
        self._citationSolution = citationSolution
        self._hints = hints

    def puzzleTitle(self):
        return self._puzzleTitle

    def setPuzzleTitle(self, puzzleTitle):
        self._puzzleTitle = puzzleTitle

    def puzzleCode(self):
        return self._puzzleCode

    def setPuzzleCode(self, puzzleCode):
        self._puzzleCode = puzzleCode

    def citationCode(self):
        return self._citationCode

    def setCitationCode(self, citationCode):
        self._citationCode = citationCode

    def puzzleSolution(self):
        return self._puzzleSolution

    def setPuzzleSolution(self, puzzleSolution):
        self._puzzleSolution = puzzleSolution

    def citationSolution(self):
        return self._citationSolution

    def setCitationSolution(self, citationSolution):
        self._citationSolution = citationSolution

    def hints(self):
        return self._hints

    def setHints(self, hints):
        self._hints = hints

    def checkPuzzle(self):
        """
        This is not necessary -- it is included in the puzzleDialog's accept() method
        I leave this here as notes for eventual completion of that method

        Checks for various errors that might occur when entering a puzzle:
            No_Code_Error:  A name was entered for puzzle but no code is present
            Length_Error:  The code and its solution are not the same length
            Inconsistent_Code_Error:  At least one code letter is assigned to more than one solution letter
            Hint_Count_Error:  The given hint_count does not match the actual number of hints
                       - never mind, no need for hintCount

        :return: a dictionary with the titles above as keys and corresponding error messages.
                when there is an Inconsistent_Code_Error, it's entry is followed by another entry indicating the
                problem(s).  This entry has a key of Code_Letter_Error and its contents explain the error in the
                form:  C cannot equal A and B[ and ...]
        """
        print('Got to checkPuzzle')
