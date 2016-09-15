from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import string, unicodedata

import data_structures

alphabet = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class LetterUnit(QWidget):

    def __init__(self, codeLetter=" ", guessLetter=" ", xpos=0, ypos=0, size = QSize(20, 60), parent=None, enabled=False):
        super(LetterUnit, self).__init__(parent)
        self._codeLetter = codeLetter
        self._guessLetter = guessLetter
        self._xpos = xpos
        self._ypos = ypos
        self._size = size
        self._enabled = enabled
        self._letterFont = self.setLetterFont(self._size.width())
        self._active = False
        self._timer = QTimer()

        self.setAppearance()
        self.move(self._xpos, self._ypos)

    def setAppearance(self):
        self.resize(self.size().width(), self._size.height())

        self.guessLabel = QLabel(self._guessLetter)
        self.guessLabel.setFont(self._letterFont)
        self.guessLabel.setStyleSheet("QLabel { background-color : white; }")
        self.guessLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.guessLabel.setLineWidth(1)
        self.guessLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if self.codeLetter() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.guessLabel.setStyleSheet("QLabel { background-color : white; }")
        else:
            self.guessLabel.setStyleSheet("QLabel { background-color : rgb(240, 240, 240); }")

            self.codeLabel = QLabel(self.codeLetter())
            self.codeLabel.setFont(self._letterFont)
            self.codeLabel.setStyleSheet("QLabel { background-color : ivory; }")
            self.codeLabel.setFrameStyle(QFrame.WinPanel | QFrame.Sunken)
            self.codeLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.guessLabel)
        layout.addWidget(self.codeLabel)

    def codeLetter(self):
        """
        Returns the code letter as a string
        :return: QString
        """
        return self._codeLetter

    def setCodeLetter(self, letter):
        """
        Sets the letter in the code section of the box
        :param letter:
        :return: None
        """
        if letter == ' ':
            displayLetter = 'space'
        else:
            displayLetter = letter
        print("Got to setCodeLetter with: ", displayLetter)
        self._codeLetter = letter
        print("self._codeLetter = ", self._codeLetter)
        self.updateAppearance()

    def moveToCodeLetter(self, letter):
        """
        Changes the code letter one step at a time until it comes to letter
        :param letter:
        :return: None
        """
        print("Got to moveToCodeLetter with letter: ", letter)
        self.setCodeLetter(letter)      # for now, until you get around to implementing something fancier

    # def setMode(self, letter):
    #     if letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    #         self.codeLabel.setEnabled(False)
    #         set.guessLabel.setEnabled(False)
    #     else:
    #         self.codeLabel.setEnabled(True)
    #         self.guessLabel.setEnabled(True)

    def size(self):
        """
        Returns the current size of the LetterUnit
        :return: QSize
        """
        return self._size

    def setSize(self, width, height):
        """
        Sets the size of the LetterUnit and adjusts the font size accordingly
        :param width: int
        :param height: int
        :return: QFont
        """
        self._size = QSize(width, height)
        return self.setFontSize(width)

    def setLetterFont(self, width):
        """
        Sets the fontSize of the LetterUnit according to the width of the unit itself
        :param width: int
        :return: QFont
        """
        if width <= 15:
            fontSize = 10
        elif width <= 20:
            fontSize = 12
        else:
            fontSize = 14
        return QFont("Arial", fontSize)

    def updateAppearance(self):

        print("uA A")
        self.guessLabel.setText(self._guessLetter)
        print("uA B")
        self.codeLabel.setText(self._codeLetter)
        print("ua C")
        if self._codeLetter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            print("it's in the alphabet")
            self.guessLabel.setStyleSheet("QLabel { background-color : rgb(240, 240, 240); }")
        else:
            print("it's a space")
            self.guessLabel.setStyleSheet("QLabel { background-color : white; }")
        print("uA D")


class AddCollection(QDialog):

    """
    Invoke this class without parameters when creating a new collection,
    invoke it with at least name set to edit the current collection
    """

    def __init__(self, currentCollection=None):
        super(AddCollection, self).__init__()       # you removed parent from the .__init__(parent)

        # Turn off the context help button (The ? in the title bar.)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._currentCollection = currentCollection
        self._name = ""
        self._author = ""

        if self._currentCollection:     # collection present means edit mode, otherwise we are adding a new collection
            self._mode = "Edit"
            self.setWindowIcon(QIcon("../images/editpuzzleicon-2.png"))
            self.setWindowTitle("Edit Collection")
        else:
            self._mode = "New"
            self.setWindowIcon(QIcon("../images/addCollectionIcon.png"))
            self.setWindowTitle("Create New Collection")
        self.setupUI()

    def currentCollection(self):
        return self._currentCollection

    def name(self):
        return self._name

    def author(self):
        return self._author

    def setupUI(self):
        """
        Creates the user interface elements for the AddCollectionDialog box
        The Add Puzzles button is disabed until the new collection has been saved,
        or if this dialog box is in edit mode
        :return: None
        """
        print("Got to AddCollectionDialog's setupUI")

        collectionNameLabel = QLabel("Collection Name:")
        self.collectionNameEdit = QLineEdit()
        self.collectionNameEdit.textEdited.connect(self.check_for_name)
        self.collectionNameEdit.editingFinished.connect(self.name_edit_lose_focus)

        authorLabel = QLabel("Author of this Collection:")
        self.authorEdit = QLineEdit()

        addCollectionButtonBox = QDialogButtonBox()

        self.acceptCollectionButton = addCollectionButtonBox.addButton("Create Collection", QDialogButtonBox.AcceptRole)
        self.acceptCollectionButton.setEnabled(False)

        self.cancelButton = addCollectionButtonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        addCollectionButtonBox.accepted.connect(self.acceptCollection)
        addCollectionButtonBox.rejected.connect(self.rejectCollection)

        collectionGrid = QGridLayout()
        collectionGrid.addWidget(collectionNameLabel, 0, 0, Qt.AlignRight)
        collectionGrid.addWidget(self.collectionNameEdit, 0, 1)
        collectionGrid.addWidget(authorLabel, 1, 0, Qt.AlignRight)
        collectionGrid.addWidget(self.authorEdit, 1, 1)

        collectionLayout = QVBoxLayout()
        collectionLayout.addLayout(collectionGrid)
        collectionLayout.addWidget(addCollectionButtonBox)

        dialogLayout = QVBoxLayout(self)
        dialogLayout.addLayout(collectionLayout)

    def check_for_name(self):
        """
        deactivates the Save button when the collectionNameEdit box is empty
        :return:
        """
        if self.collectionNameEdit.text() == "":
            self.acceptCollectionButton.setEnabled(False)

    def name_edit_lose_focus(self):
        """
        A collection is considered "Available" (to have puzzles added and to be saved) when it has a name.
        When the collectionNameEdit lineEdit loses focus, this method checks to see if it contains a collection name,
        if so, it updates the AddEditCollection dialog box's buttons accordingly and sets the focus to
        the self.authorEdit box.
        :return: None
        """
        if self.collectionNameEdit.text() != "":
            # self.addPuzzlesButton.setEnabled(True)
            self.acceptCollectionButton.setEnabled(True)
            self.authorEdit.setFocus()

    def acceptCollection(self):
        """
        Accepts the collection as entered and checks for errors
        """
        class NoNameError(Exception):pass

        class BadNameError(Exception):pass

        name = self.collectionNameEdit.text()
        author = self.authorEdit.text()
        filename = self.createFilename(name)

        try:
            if len(name.strip()) == 0:
                raise NoNameError("You must at least enter a name for the Collection.")
            if len(filename) == 0:
                filename = "Temporary_Filename.col"
                msg = "Could not convert " + name + " into a valid filename.  "
                msg += "The filename will be " + filename + " "
                msg += "but you should use your operating system to rename it to something more useful."
                raise BadNameError(msg)

            successMessage = "This collection will be saved under the filaname of " + filename + ".col.  "
            successMessage += "You may change it if you wish by using the methods supplied by "
            successMessage += "your computer's operating system."
            QMessageBox.information(self, "Filename Information", successMessage)

        except NoNameError as e:
            QMessageBox.warning(self, "Name Error", str(e))
            self.collectionNameEdit.selectAll()
            self.collectionNameEdit.setFocus()
            return

        except BadNameError as e:
            QMessageBox.warning(self, "Filename Notice", str(e))
            return

        self._name = name
        self._author = author
        QDialog.accept(self)

    def createFilename(self, name):
        """
        Converts name to a valid filename if possible, otherwise returns the empty string

        This method is based on one from
            http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python/634023
        I removed the byte encoding since this is to be used on Windows and removed the space ' ' as a valid
        character because I felt like it

        :param name:
        :return: a string prepared to be used as a filename
        """
        validFilenameChars = "-_.()%s%s" % (string.ascii_letters, string.digits)
        cleanedFilename = unicodedata.normalize('NFKD', name)
        return ''.join(c for c in cleanedFilename if c in validFilenameChars)

    def rejectCollection(self):
        QDialog.reject(self)

#======================================================================================================================

#ToDo: Create a means of editing existing collections by changing name and/or author.  Create corresponding help file.

#======================================================================================================================

class CodeTextEdit(QTextEdit):

    def __init__(self):
        super(CodeTextEdit, self).__init__()

    def keyPressEvent(self, e):
        newEvent = QKeyEvent(QEvent.KeyPress, e.key(), e.modifiers(), text=e.text().upper())
        return super(CodeTextEdit, self).keyPressEvent(newEvent)


class CodeLineEdit(QLineEdit):

    def __init__(self):
        super(CodeLineEdit, self).__init__()

    def keyPressEvent(self, e):
        newEvent = QKeyEvent(QEvent.KeyPress, e.key(), e.modifiers(), text=e.text().upper())
        return super(CodeLineEdit, self).keyPressEvent(newEvent)


class HintLineEdit(CodeLineEdit):
    def __init__(self):
        super(HintLineEdit, self).__init__()

    def keyPressEvent(self, e):
        if e.text().upper() not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ=; " and e.key() != Qt.Key_Backspace:
            return
        else:
            return super(HintLineEdit, self).keyPressEvent(e)


class AddEditPuzzle(QDialog):

    def __init__(self, collection=None, currentPuzzleIndex=-1, parent=None):
        print('Initializing AddEditPuzzle')
        super(AddEditPuzzle, self).__init__(parent)

        # Turn off the context help button (The ? in the title bar.)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._collection = collection
        self._currentPuzzleIndex = currentPuzzleIndex
        self._puzzles = collection.puzzles()

        self.setupUI()
        if self._currentPuzzleIndex >= 0:
            self.setPuzzleSelector(self._currentPuzzleIndex)
            self._mode = "Edit"
        else:
            self._mode = None
        self._puzzleEdited = False
        self.updateUI()

    def collection(self):
        return self._collection

    def currentPuzzleIndex(self):
        return self._currentPuzzleIndex

    def setCurrentPuzzleIndex(self, index):
        self._currentPuzzleIndex = index

    def puzzles(self):
        return self._puzzles

    def setPuzzles(self, puzzles):
        self._puzzles = puzzles

    def addPuzzle(self, puzzle):
        self._puzzles.append(puzzle)

    def insertPuzzle(self, index, puzzle):
        self._puzzles.insert(index, puzzle)
        # this function has not yet been used in the code below
        # ToDo: Alter the code to use insertPuzzle when needed


    def setupUI(self):

        print('in setupUI')

        self.setWindowIcon(QIcon("../images/editpuzzleicon-2.png"))
        self.setWindowTitle("Add or Edit Puzzles")

        self.addPuzzleButton = QPushButton("Add New Puzzle")
        self.addPuzzleButton.clicked.connect(self.createNewPuzzle)
        addButtonLayout = QHBoxLayout()
        addButtonLayout.addSpacing(220)
        addButtonLayout.addWidget(self.addPuzzleButton)

        errorLabel = QLabel("Error Display")
        self.errorDisplayWindow = QLabel('')
        self.errorDisplayWindow.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.errorDisplayWindow.setMinimumHeight(50)
        self.errorDisplayWindow.setStyleSheet("QLabel { background-color : QColor(240, 240, 240; }")
        self.errorDisplayWindow.setEnabled(False)

        errorDisplayLayout = QVBoxLayout()
        errorDisplayLayout.addWidget(errorLabel)
        errorDisplayLayout.addWidget(self.errorDisplayWindow)

        puzzleSelectorLabel = QLabel("Puzzle Selector:")
        self.puzzleSelector = QComboBox()
        self.puzzleSelector.currentIndexChanged.connect(self.addEditPuzzleSelectorChanged)

        puzzleTitleLabel = QLabel("Puzzle Name:")
        self.puzzleTitleEdit = QLineEdit()
        self.puzzleTitleEdit.textChanged.connect(self.editBoxChanged)

        puzzleCodeLabel = QLabel("Puzzle Code:")
        self.puzzleCodeEdit = CodeTextEdit()
        self.puzzleCodeEdit.setTabChangesFocus(True)
        self.puzzleCodeEdit.setMaximumHeight(60)
        self.puzzleCodeEdit.textChanged.connect(self.editBoxChanged)

        citationCodeLabel = QLabel("Citation Code (if any):")
        self.citationCodeEdit = CodeLineEdit()
        self.citationCodeEdit.textChanged.connect(self.editBoxChanged)

        puzzleSolutionLabel = QLabel("Puzzle Solution (if any):")
        self.puzzleSolutionEdit = CodeTextEdit()
        self.puzzleSolutionEdit.setTabChangesFocus(True)
        self.puzzleSolutionEdit.setMaximumHeight(60)
        self.puzzleSolutionEdit.textChanged.connect(self.editBoxChanged)

        citationSolutionLabel = QLabel("Citation Solution (if any):")
        self.citationSolutionEdit = CodeLineEdit()
        self.citationSolutionEdit.textChanged.connect(self.editBoxChanged)

        hintLabel = QLabel("Hints (if any):")
        self.hintEdit = HintLineEdit()
        self.hintEdit.textChanged.connect(self.editBoxChanged)

        puzzleButtonBox = QDialogButtonBox()
        self.storePuzzleButton = puzzleButtonBox.addButton("Store Puzzle", QDialogButtonBox.ActionRole)
        self.deleteButton = puzzleButtonBox.addButton("Delete", QDialogButtonBox.DestructiveRole)
        self.clearButton = puzzleButtonBox.addButton("Clear", QDialogButtonBox.ActionRole)
        self.cancelPuzzleButton = puzzleButtonBox.addButton("Cancel New Puzzle", QDialogButtonBox.RejectRole)

        self.storePuzzleButton.clicked.connect(self.storePuzzle)
        self.deleteButton.clicked.connect(self.deletePuzzle)
        self.clearButton.clicked.connect(self.clearPuzzle)
        self.cancelPuzzleButton.clicked.connect(self.cancelPuzzle)

        puzzleGrid = QGridLayout()
        puzzleGrid.addWidget(puzzleSelectorLabel, 0, 0, Qt.AlignRight)
        puzzleGrid.addWidget(self.puzzleSelector, 0, 1)
        puzzleGrid.addWidget(puzzleTitleLabel, 1, 0, Qt.AlignRight)
        puzzleGrid.addWidget(self.puzzleTitleEdit, 1, 1)
        puzzleGrid.addWidget(puzzleCodeLabel, 2, 0, Qt.AlignRight | Qt.AlignTop)
        puzzleGrid.addWidget(self.puzzleCodeEdit, 2, 1)
        puzzleGrid.addWidget(citationCodeLabel, 3, 0, Qt.AlignRight)
        puzzleGrid.addWidget(self.citationCodeEdit, 3, 1)
        puzzleGrid.addWidget(puzzleSolutionLabel, 4, 0, Qt.AlignRight | Qt.AlignTop)
        puzzleGrid.addWidget(self.puzzleSolutionEdit, 4, 1)
        puzzleGrid.addWidget(citationSolutionLabel, 5, 0)
        puzzleGrid.addWidget(self.citationSolutionEdit, 5, 1)
        puzzleGrid.addWidget(hintLabel, 6, 0, Qt.AlignRight)
        puzzleGrid.addWidget(self.hintEdit, 6, 1)

        puzzleEditLayout = QVBoxLayout()
        puzzleEditLayout.addLayout(errorDisplayLayout)
        puzzleEditLayout.addLayout(puzzleGrid)
        puzzleEditLayout.addWidget(puzzleButtonBox)

        self.puzzleEditControls = QGroupBox("Puzzle Editor")
        self.puzzleEditControls.setEnabled(False)
        self.puzzleEditControls.setLayout(puzzleEditLayout)

        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelDialog)

        self.acceptButton = QPushButton("Accept Changes")
        self.acceptButton.setEnabled(False)
        self.acceptButton.clicked.connect(self.accept)

        dialogButtonLayout = QHBoxLayout()
        dialogButtonLayout.addSpacing(220)
        dialogButtonLayout.addWidget(self.acceptButton)
        dialogButtonLayout.addWidget(cancelButton)

        dialogLayout = QVBoxLayout(self)
        dialogLayout.addLayout(addButtonLayout)
        dialogLayout.addWidget(self.puzzleEditControls)
        dialogLayout.addLayout(dialogButtonLayout)

    def setPuzzleSelector(self, index):
        """
        Adds all the puzzles in the current collection to the puzzleSelector and sets the selector to the given index
        :return: None
        """
        # ToDo: Make sure puzzleSelector is properly set upon entry under all circumstances
        print("In setPuzzleSelector")
        currentCollection = self.collection()
        self.puzzleEditControls.setEnabled(True)
        self.cancelPuzzleButton.setEnabled(False)
        self.storePuzzleButton.setEnabled(False)
        self.puzzleSelector.blockSignals(True)
        self.puzzleSelector.clear()
        for puzzle in currentCollection.puzzles():
            self.puzzleSelector.addItem(puzzle.puzzleTitle())
        print("self.puzzleSelector.currentIndex() = ", self.puzzleSelector.currentIndex(), " just before being set to ", index)
        self.puzzleSelector.blockSignals(False)
        self.puzzleSelector.setCurrentIndex(self.currentPuzzleIndex())
        self.displayPuzzle(index)

    def displayPuzzle(self, index):
        """
        When there is a current puzzle, this method is called to populate the widgets of the puzzle editor group
        with the values of the current puzzle
        :return: None
        """
        print("Got to displayPuzzle")
        # index = self.currentPuzzleIndex()
        # self.setCurrentPuzzleIndex(index)
        currentPuzzle = self._puzzles[index]
        self.puzzleTitleEdit.setText(currentPuzzle.puzzleTitle())
        self.puzzleCodeEdit.setText(currentPuzzle.puzzleCode())
        self.citationCodeEdit.setText(currentPuzzle.citationCode())
        self.puzzleSolutionEdit.setText(currentPuzzle.puzzleSolution())
        self.citationSolutionEdit.setText(currentPuzzle.citationSolution())
        hintText = ""
        for hint in currentPuzzle.hints():
            hintText += hint + "; "
        self.hintEdit.setText(hintText)

    def updateUI(self):
        """
        Sets the availability of the dialog box's controls according to its present state
        :return: None
        """
        if self._puzzleEdited:
            self.storePuzzleButton.setEnabled(True)
        else:
            self.storePuzzleButton.setEnabled(False)

    def createNewPuzzle(self):
        """
        If a puzzle is present (as indicated by a non-negative value of self.puzzleSelector.index)
        The contents of the input boxes are cleared and a suggested title, "Puzzle n", where n is an integer
        indicating the next available number, is placed in the puzzleTitleEdit control.
        :return: None
        """

        print("Got to createNewPuzzle")
        self.puzzleEditControls.setEnabled(True)
        self.addPuzzleButton.setEnabled(False)
        self.puzzleSelector.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.cancelPuzzleButton.setEnabled(True)
        self.clearPuzzle()
        nextNumber = len(self._puzzles) + 1
        self._oldPuzzleIndex = self._currentPuzzleIndex
        self._currentPuzzleIndex = nextNumber - 1
        self.puzzleTitleEdit.setText("Puzzle " + str(nextNumber))
        self.puzzleCodeEdit.setFocus()
        self._mode = "Add"

    def addEditPuzzleSelectorChanged(self):
        print("Got to addEditPuzzleSelectorChanged")
        self._currentPuzzleIndex = self.puzzleSelector.currentIndex()
        self.displayPuzzle(self._currentPuzzleIndex)
        self._mode = "Edit"

    def deletePuzzle(self):
        print("Got to deletePuzzle")

    def clearPuzzle(self):
        print("Got to clearPuzzle")
        self.puzzleTitleEdit.setText("")
        self.puzzleCodeEdit.setText("")
        self.citationCodeEdit.setText("")
        self.puzzleSolutionEdit.setText("")
        self.citationSolutionEdit.setText("")
        self.hintEdit.setText("")

    def cancelPuzzle(self):
        """
        If the user clicks this button he or she has decided NOT to add a new puzzle, but doesn't want to leave
        the dialog box entirely.  Perhaps to edit an existing puzzle.
        :return: None
        """
        print("Got to cancelPuzzle")
        self.addPuzzleButton.setEnabled(True)
        self.clearPuzzle()
        if self._oldPuzzleIndex >= 0:
            self.setPuzzleSelector(self._oldPuzzleIndex)
            self.puzzleSelector.setEnabled(True)
        else:
            self.puzzleEditControls.setEnabled(False)

    def storePuzzle(self):
        """
        Checks the edited puzzle for errors and, if there are none stores the puzzle in the collection and updates
        the user interface according to whether the puzzle was a new one being added or an old one being edited.
        If there are errors, prints an error message and returns focus to its best guess as to where the problem is.
        :return: None
        """
        print("Got to storePuzzle")

        class LengthMismatchError(Exception):pass
        class InconsistentCodeError(Exception):pass
        class BadHintFormatError(Exception):pass
        class BadHintError(Exception):pass

        title = self.puzzleTitleEdit.text()
        puzzleTitle = self.puzzleTitleEdit.text()
        puzzleCode = self.puzzleCodeEdit.toPlainText().upper()
        citationCode = self.citationCodeEdit.text().upper()
        puzzleSolution = self.puzzleSolutionEdit.toPlainText().upper()
        citationSolution = self.citationSolutionEdit.text().upper()
        hints = self.cleanHints(self.hintEdit.text())
        # ToDo: Find ways to help the user find the errors: characteer position counts, character highlighting, etc.
        try:
            results = self.lengthMismatchErrorTests(puzzleCode, puzzleSolution, citationCode, citationSolution)
            if not results[0]:
                raise LengthMismatchError(results[1])

            # InconsistentCodeError tests
            if puzzleSolution != "":
                codeDict = {}
                solutionDict = {}
                solutionIndex = 0
                for codeChar in puzzleCode:
                    solutionChar = puzzleSolution[solutionIndex]
                    if codeChar in codeDict.keys():
                        if codeDict[codeChar] != solutionChar:
                            msg = "The code letter, " + codeChar + " in the puzzle code, cannot represent both "
                            msg += codeDict[codeChar] + " and " + solutionChar + " in the solution.\n\n"
                            msg += "Check position " + str(solutionIndex + 1) + "."
                            raise InconsistentCodeError(msg)
                        else:
                            solutionIndex += 1
                    elif solutionChar in solutionDict.keys():
                        if solutionDict[solutionChar] != codeChar:
                            msg = "The solution letter, " + solutionChar + " in the puzzle solution,"
                            msg += " cannot be represented by both " + solutionDict[solutionChar] + " and "
                            msg += codeChar + " in the puzzle code.\n\n"
                            msg += "Check position " + str(solutionIndex+1) + "."
                            raise InconsistentCodeError(msg)
                        else:
                            solutionIndex += 1
                    else:
                        codeDict[codeChar] = solutionChar
                        solutionDict[solutionChar] = codeChar
                        solutionIndex += 1
                solutionIndex = 0
                for codeChar in citationCode:
                    solutionChar = citationSolution[solutionIndex]
                    if codeChar in codeDict.keys():
                        if codeDict[codeChar] != solutionChar:
                            msg = "The letter, " + codeChar + " in the citation code, cannot represent both "
                            msg += codeDict[codeChar] + " and " + solutionChar + " in the solution.\n\n"
                            msg += "Check position " + str(solutionIndex + 1) + "."
                            raise InconsistentCodeError(msg)
                        else:
                            solutionIndex += 1
                    elif solutionChar in solutionDict.keys():
                        if solutionDict[solutionChar] != codeChar:
                            msg = "The solution letter, " + solutionChar + " in the citation solution, "
                            msg += "cannot be represented by both " + solutionDict[solutionChar] + " and "
                            msg += codeChar + " in the citation code.\n\n"
                            msg += "Check position " + str(solutionIndex + 1) + "."
                            raise InconsistentCodeError(msg)
                        else:
                            solutionIndex += 1
                    else:
                        codeDict[codeChar] = solutionChar
                        solutionDict[solutionChar] = codeChar
                        solutionIndex += 1

            # BadHintFormatError Tests'
            print("hints = ", hints)
            if len(hints) != 0:
                for hint in hints:
                    print(hint)
                    if (len(hint.strip()) != 3) or (hint[1] != '='):
                        msg = "Hints must have the format '(code letter 1)=(solution letter 1); "
                        msg += "(code letter 2) = (solution letter 2)' etc.  For example:  A=C; H=W"
                        msg += "See the help files for further information."
                        raise BadHintFormatError(msg)

                # BadHintError Tests
                print("Got to BadHintError Tests with hints = ", hints)
                parsedHints = self.parseHints(hints)
                print("parsedHints = ", parsedHints)
                for hintpair in parsedHints:
                    print("codeDict: ", codeDict, " solutionDict: ", solutionDict, " hintpair: ", hintpair)
                    if hintpair[0] not in codeDict.keys():
                        print("B")
                        msg = "The hint for letter " + hintpair[0] + " does not help since it is not in the puzzle code."
                        raise BadHintError(msg)
                    elif hintpair[1] not in solutionDict.keys():
                        msg = "The hint that " + hintpair[0] + "=" + hintpair[1] + " makes no sense since " + hintpair[1]
                        msg += " does not appear in the solution."
                        raise BadHintError(msg)
                    elif codeDict[hintpair[0]] != hintpair[1]:
                        msg = "In the puzzle, " + hintpair[0] + " represents " + codeDict[hintpair[0]] + ".  "
                        msg += "The hint says it represents " + hintpair[1] + "."
                        raise BadHintError(msg)

        except LengthMismatchError as e:
            QMessageBox.warning(self, "Length Mismatch Error", str(e))
            if "puzzle" in str(e):
                codeWords = puzzleCode.split()
                solutionWords = puzzleSolution.split()
                if len(codeWords) == len(solutionWords):
                    index = 0
                    for word in codeWords:
                        if len(word) != len(solutionWords[index]):
                            codeWords[index] = '<font color="red">' + word + '</font>'
                            solutionWords[index] = '<font color="red".' + solutionWords[index] + '</font>'
                        index += 1
                    else:
                        # figure out what to do if not the same number of words
                        pass
                    replacement = ""
                    for word in codeWords:
                        replacement += word + " "
                    self.puzzleCodeEdit.setHtml(replacement.strip())
                    replacement = ""
                    for word in solutionWords:
                        replacement += word + " "
                    self.puzzleSolutionEdit.setHtml(replacement.strip())

                self.puzzleCodeEdit.setFocus()
            else:
                self.citationCodeEdit.setFocus()
            return

        except InconsistentCodeError as e:
            QMessageBox.warning(self, "Insonsistent Code Error", str(e))
            if "puzzle" in str(e):
                self.puzzleCodeEdit.setFocus()
            else:
                self.citationCodeEdit.setFocus()
            return

        except BadHintFormatError as e:
            QMessageBox.warning(self, "Bad Hint Format Error", str(e))
            self.hintEdit.setFocus()

        except BadHintError as e:
            QMessageBox.warning(self, "Bad Hint Error", str(e))
            self.hintEdit.setFocus()
            return

        print("Got past the tests.")
        self.acceptButton.setEnabled(True)
        if self._mode == "Add":
            # new puzzle is added to the collection
            newpuzzle = data_structures.Puzzle(puzzleTitle, puzzleCode, citationCode,
                                               puzzleSolution, citationSolution, hints)
            self._collection.addPuzzle(newpuzzle)
            self.setPuzzleSelector(-1)
            self.createNewPuzzle()
            self.storePuzzleButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            # updated puzzle is altered in the collection
            correctedpuzzle = data_structures.Puzzle(puzzleTitle, puzzleCode, citationCode,
                                                     puzzleSolution, citationSolution, hints)
            self._collection.correctPuzzle(correctedpuzzle, self._currentPuzzleIndex)
            self.setPuzzleSelector(self._currentPuzzleIndex)
            # puzzle selector is updated if the puzzle title changed
            self.storePuzzleButton.setEnabled(False)

    def accept(self):
        print("got to accept")
        QDialog.accept(self)

    def lengthMismatchErrorTests(self, puzzleCode, puzzleSolution, citationCode, citationSolution):
        print("Got to lengthMismatchErrorTests")

        if puzzleSolution != "" and len(puzzleCode) != len(puzzleSolution):
            return False, "The puzzle's code and its solution are not the same length."

        if citationSolution != "" and len(citationCode) != len(citationSolution):
            return False, "The citation's code and its solution are not the same length."

        return True, ""

    def cancelDialog(self):
        QDialog.reject(self)

    def editBoxChanged(self):
        """
        Manages the availability of the Save Puzzle button when any of the edit boxes are changed.
        The Save Puzzle button is turned off if either puzzleTitleEdit or puzzleCodeEdit are empty.
        :return: None
        """
        print("Got to editBoxChanged")
        if self.puzzleTitleEdit.text() == "" or self.puzzleCodeEdit.toPlainText() == "":
            self.puzzleSolutionEdit.setEnabled(False)
            self.citationCodeEdit.setEnabled(False)
            self.citationSolutionEdit.setEnabled(False)
            self.hintEdit.setEnabled(False)
            self.storePuzzleButton.setEnabled(False)
        else:
            self.puzzleSolutionEdit.setEnabled(True)
            self.citationCodeEdit.setEnabled(True)
            self.citationSolutionEdit.setEnabled(True)
            self.hintEdit.setEnabled(True)
            self.storePuzzleButton.setEnabled(True)

    def cleanHints(self, hintstring):
        """
        cleans a hint string that may contain extra spaces or a trailing semicolon and converts it to a list of
        untested "hints" that do not contain spaces
        :param hintstring: string
        :return: list of strings
        """
        if hintstring == "":
            return []
        hintstring = hintstring.rstrip(";")
        hintlist = hintstring.split(";")
        newhintlist = []
        for hint in hintlist:
            newhint = ""
            for char in hint:
                if char != " ":
                    newhint += char
            newhintlist.append(newhint)
        return newhintlist

    def parseHints(self, hintlist):
        """
        Takes a list of hints, for instance, ['A=B', 'N=H'] and parses it
        into a list of tuples
        :param hints: list
        :return: list of lists with the format (code letter, solution letter)
        """
        print("Got to self.parseHints with hints = ", hintlist)
        parsed = []
        for hint in hintlist:
            parsed.append(hint.split('='))

        return parsed

