from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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


class AddEditCollection(QDialog):

    """
    Invoke this class without parameters when creating a new collection,
    invoke it with at least name set to edit the current collection
    """

    def __init__(self, currentCollection=None, currentPuzzleIndex=None):
        super(AddEditCollection, self).__init__()       # you removed parent from the .__init__(parent)
        self._currentCollection = currentCollection
        self._currentPuzzleIndex = currentPuzzleIndex
        self.setupUI()
        self.updateUI()

    # def clearCurrentPuzzle(self):
    #         self._puzzleTitle = None
    #         self._puzzleCode = None
    #         self._citationCode = None
    #         self._puzzleSolution = None
    #         self._citationSolution = None
    #         self._hints = None
    #
    # def readFromCurrentPuzzle(self):
    #     self._puzzleTitle = self._puzzles[self._currentPuzzleIndex].puzzleTitle()
    #     self._puzzleCode = self._puzzles[self._currentPuzzleIndex].puzzleCode()
    #     self._citationCode = self._puzzles[self._currentPuzzleIndex].citationCode()
    #     self._puzzleSolution = self._puzzles[self._currentPuzzleIndex].puzzleSolution()
    #     self._citationSolution = self._puzzles[self._currentPuzzleIndex].citationSolution()
    #     self._hints = self._puzzles[self._currentPuzzleIndex].hints()

    def currentCollection(self):
        return self._currentCollection

    def currentPuzzleIndex(self):
        return self._currentPuzzleIndex

    def storePuzzle(self, puzzle):
        self._puzzles.append(puzzle)


    class CodeTextEdit(QTextEdit):

        """
        A helper class creating a QTextEdit that converts characters to upper case
        and potentially converts Returns or Enter key presses to tabs
        """

        def __init__(self):
            super(CodeTextEdit, self).__init__()

        def keyPressEvent(self, e):
            newEvent = QKeyEvent(QEvent.KeyPress, e.key(), e.modifiers(), text=e.text().upper())
            return super(CodeTextEdit, self).keyPressEvent(newEvent)


    class CodeLineEdit(QLineEdit):

        """
        A helper class creating a QLineEdit that converts characters to upper case
        and potentially converts Returns or Enter key presses to tabs
        """

        def __init__(self):
            super(CodeLineEdit, self).__init__()

        def keyPressEvent(self, e):
            newEvent = QKeyEvent(QEvent.KeyPress, e.key(), e.modifiers(), text=e.text().upper())
            return super(CodeLineEdit, self).keyPressEvent(newEvent)


    def setupUI(self):
        """
        Creates the user interface elements for the AddEditDialog box
        The puzzle edit controls are disabed leaving the selective
        enabling to be done as needed by other routines
        :return: None
        """
        print("Got to AddEditDialog's setupUI")

        collectionNameLabel = QLabel("Collection Name:")
        self.collectionNameEdit = QLineEdit()
        self.collectionNameEdit.editingFinished.connect(self.name_edit_lose_focus)

        authorLabel = QLabel("Author of this Collection:")
        self.authorEdit = QLineEdit()

        addPuzzleButtonBox = QDialogButtonBox()
        self.addPuzzleButton = addPuzzleButtonBox.addButton("Add New Puzzle", QDialogButtonBox.ActionRole)
        self.addPuzzleButton.setEnabled(False)
        self.addPuzzleButton.clicked.connect(self.addNewPuzzle)

        collectionGrid = QGridLayout()
        collectionGrid.addWidget(collectionNameLabel, 0, 0, Qt.AlignRight)
        collectionGrid.addWidget(self.collectionNameEdit, 0, 1)
        collectionGrid.addWidget(authorLabel, 1, 0, Qt.AlignRight)
        collectionGrid.addWidget(self.authorEdit, 1, 1)

        collectionLayout = QVBoxLayout()
        collectionLayout.addLayout(collectionGrid)
        collectionLayout.addWidget(addPuzzleButtonBox)

        puzzleSelectorLabel = QLabel("Puzzle Selector:")
        self.puzzleSelector = QComboBox()
        self.puzzleSelector.currentIndexChanged.connect(self.addEditPuzzleSelectorChanged)

        puzzleTitleLabel = QLabel("Puzzle Name:")
        self.puzzleTitleEdit = QLineEdit()

        puzzleCodeLabel = QLabel("Puzzle Code:")
        self.puzzleCodeEdit = CodeTextEdit()
        self.puzzleCodeEdit.setTabChangesFocus(True)
        self.puzzleCodeEdit.setMaximumHeight(60)

        citationCodeLabel = QLabel("Citation Code (if any):")
        self.citationCodeEdit = CodeLineEdit()

        puzzleSolutionLabel = QLabel("Puzzle Solution (if any):")
        self.puzzleSolutionEdit = CodeTextEdit()
        self.puzzleSolutionEdit.setTabChangesFocus(True)
        self.puzzleSolutionEdit.setMaximumHeight(60)

        citationSolutionLabel = QLabel("Citation Solution (if any):")
        self.citationSolutionEdit = CodeLineEdit()

        hintLabel = QLabel("Hints (if any):")
        self.hintEdit = CodeLineEdit()

        puzzleButtonBox = QDialogButtonBox()
        puzzleButtonBox.addButton("Store Puzzle", QDialogButtonBox.AcceptRole)
        deletePuzzleButton = puzzleButtonBox.addButton("Delete", QDialogButtonBox.ActionRole)
        puzzleButtonBox.accepted.connect(self.acceptPuzzle)
        deletePuzzleButton.clicked.connect(self.deletePuzzle)

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
        puzzleEditLayout.addLayout(puzzleGrid)
        puzzleEditLayout.addWidget(puzzleButtonBox)

        self.puzzleEditControls = QGroupBox("Add or Edit Puzzles")
        self.puzzleEditControls.setEnabled(False)
        self.puzzleEditControls.setLayout(puzzleEditLayout)

        dialogButtonBox = QDialogButtonBox()
        self.acceptCollectionButton = dialogButtonBox.addButton("Store Collection", QDialogButtonBox.AcceptRole)
        self.acceptCollectionButton.setEnabled(False)

        dialogButtonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        dialogButtonBox.accepted.connect(self.acceptCollection)
        dialogButtonBox.rejected.connect(self.rejectCollection)

        dialogLayout = QVBoxLayout(self)
        dialogLayout.addLayout(collectionLayout)
        dialogLayout.addWidget(self.puzzleEditControls)
        dialogLayout.addWidget(dialogButtonBox)

    def updateUI(self):
        """
        Displays the current collection in the dialog box, if any, and
        enables the corresponding controls
        :return: None
        """
        if self.currentCollection():
            currentCollection = self.currentCollection()
            self.collectionNameEdit.setText(currentCollection.name())
            self.authorEdit.setText(currentCollection.author())
            if currentCollection.puzzles() and self.currentPuzzleIndex() != None:
                self.puzzleEditControls.setEnabled(True)
                self.puzzleSelector.blockSignals(True)
                self.puzzleSelector.clear()
                for puzzle in currentCollection.puzzles():
                    self.puzzleSelector.addItem(puzzle.puzzleTitle())
                self.puzzleSelector.setCurrentIndex(self.currentPuzzleIndex())
                self.puzzleSelector.blockSignals(False)
                currentPuzzle = currentCollection.puzzles()[self.currentPuzzleIndex()]
                self.puzzleTitleEdit.setText(currentPuzzle.puzzleTitle())
                self.puzzleCodeEdit.setText(currentPuzzle.puzzleCode())
                self.citationCodeEdit.setText(currentPuzzle.citationCode())
                self.puzzleSolutionEdit.setText(currentPuzzle.puzzleSolution())
                self.citationSolutionEdit.setText(currentPuzzle.citationSolution())
                hintText = ""
                for hint in currentPuzzle.hints():
                    hintText += hint + "; "
                self.hintEdit.setText(hintText)

    def name_edit_lose_focus(self):
        """
        A collection is considered "Available" (to have puzzles added and to be saved) when it has a name.
        When the collectionNameEdit lineEdit loses focus, this method checks to see if it contains a collection name,
        if so, it updates the AddEditCollection dialog box's buttons accordingly and sets the focus to
        the self.authorEdit box.
        :return: None
        """
        if self.collectionNameEdit.text() != "":
            self.addPuzzleButton.setEnabled(True)
            self.acceptCollectionButton.setEnabled(True)
            self.authorEdit.setFocus()

    def addEditPuzzleSelectorChanged(self):
        print("Got to addEditPuzzleSelectorChanged")
        self._currentPuzzleIndex = self.puzzleSelector.currentIndex()
        # self.populatePuzzleEditor()

    def populatePuzzleEditor(self, index=0):
        """
        When there is a current puzzle, this method is called to populate the widgets of the puzzle editor group
        with the values of the current puzzle
        :return: None
        """
        #self._currentPuzzleIndex = self.puzzleSelector.currentIndex()
        # self.puzzleSelector.blockSignals(True)
        # self.puzzleSelector.clear()
        # for puzzle in self._puzzles:
        #     self.puzzleSelector.addItem(puzzle.puzzleTitle())
        # if index != -1:
        #     self.puzzleSelector.setCurrentIndex(self._currentPuzzleIndex)
        # self.puzzleSelector.blockSignals(False)
        # self.readFromCurrentPuzzle()        # reads the values of the instance variables from the current puzzle
        # self.puzzleTitleEdit.setText(self._puzzleTitle)
        # self.puzzleCodeEdit.setText(self._puzzleCode)
        # self.citationCodeEdit.setText(self._citationCode)
        # self.puzzleSolutionEdit.setText(self._puzzleSolution)
        # self.citationSolutionEdit.setText(self._citationSolution)
        # hintText = ""
        # for hint in self._hints:
        #     hintText += hint + "; "
        # self.hintEdit.setText(hintText)

    def acceptPuzzle(self):
        print("Got to acceptPuzzle")

    def acceptCollection(self):
        """
        Accepts the collection as entered and checks for errors
        """
        # class NameError(Exception):pass
        #
        print("Got to AddEditCollection.accept()")
        # print("AddEditCollection's puzzle count: ", len(self.puzzles()))
        # name = self.nameEdit.text()
        # author = self.authorEdit.text()
        #
        # try:
        #     if len(name.strip()) == 0:
        #         raise NameError("You must at least enter a name for the Collection.")
        #
        # except NameError as e:
        #     QMessageBox.warning(self, "Name Error", str(e))
        #     self.nameEdit.selectAll()
        #     self.nameEdit.setFocus()
        #     return
        #
        # self._name = name
        # self._author = author
        #QDialog.accept(self)  turn it off until the calling routine in Cryptogram_Solver.pyw is ready for it

    def rejectCollection(self):
        QDialog.reject(self)

    def addNewPuzzle(self):
        self.puzzleEditControls.setEnabled(True)
        print("Got to addNewPuzzle")
        if self.puzzleTitleEdit.text():     # if a puzzle has been loaded, get rid of it
            print("there is a title")
            self.clearCurrentPuzzle()
            self.populatePuzzleEditor(-1)

    def deletePuzzle(self):
        print("Got to deletePuzzle")


# class AddEditPuzzle(QDialog):
#
#     def __init__(self, title=None, puzzleCode=None, citationCode=None,
#                  puzzleSolution=None, citationSolution=None, hints=[], parent=None):
#         super(AddEditPuzzle, self).__init__(parent)
#
#         self.setupUI()
#
#     def title(self):
#         return self._title
#
#     def puzzleCode(self):
#         return self._puzzleCode
#
#     def citationCode(self):
#         return self._citationCode
#
#     def puzzleSolution(self):
#         return self._puzzleSolution
#
#     def citationSolution(self):
#         return self._citationSolution
#
#     def hints(self):
#         return self._hints
#
#     class puzzleTextEdit(QTextEdit):
#
#         def __init__(self, parent=None):
#             super(AddEditPuzzle.puzzleTextEdit, self).__init__(parent)
#             self.setTabChangesFocus(True)
#
#         def convertText(self):
#             self.setPlainText(self.toPlainText().toUpper())
#
#     def setupUI(self):
#
#
#         buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
#         buttonBox.accepted.connect(self.accept)
#         buttonBox.rejected.connect(self.reject)
#
#         gridLayout = QGridLayout()
#         gridLayout.addWidget(titleLabel, 0, 0, Qt.AlignRight)
#         gridLayout.addWidget(self.titleEdit, 0, 1)
#         gridLayout.addWidget(puzzleCodeLabel, 1, 0, Qt.AlignRight)
#         gridLayout.addWidget(self.puzzleCodeEdit, 1, 1)
#         gridLayout.addWidget(citationCodeLabel, 2, 0, Qt.AlignRight)
#         gridLayout.addWidget(self.citationCodeEdit, 2, 1)
#         gridLayout.addWidget(puzzleSolutionLabel, 3, 0, Qt.AlignRight)
#         gridLayout.addWidget(self.puzzleSolutionEdit, 3, 1)
#         gridLayout.addWidget(citationSolutionLabel, 4, 0, Qt.AlignRight)
#         gridLayout.addWidget(self.citationSolutionEdit, 4, 1)
#         layout = QVBoxLayout(self)
#         layout.addLayout(gridLayout)
#         layout.addWidget(buttonBox)
#
#     def accept(self):
#
#         class TitleError(Exception):pass
#         class CodeError(Exception):pass
#
#         title = self.titleEdit.text()
#         puzzleCode = self.puzzleCodeEdit.toPlainText().upper()
#         citationCode = self.citationCodeEdit.text().upper()
#         puzzleSolution = self.puzzleSolutionEdit.toPlainText().upper()
#         citationSolution = self.citationSolutionEdit.text().upper()
#
#         try:
#             if len(title.strip()) == 0:
#                 raise TitleError("You must enter a title for this Puzzle.")
#
#             if len(puzzleCode.strip()) == 0:
#                 raise CodeError("You must at least enter the puzzle's code.")
#         except TitleError as e:
#             QMessageBox.warning(self, "Title Error", str(e))
#             self.titleEdit.selectAll()
#             self.titleEdit.setFocus()
#             return
#         except CodeError as e:
#             QMessageBox.warning(self, "Code Error", str(e))
#             self.puzzleCodeEdit.selectAll()
#             self.puzzleCodeEdit.setFocus()
#             return
#
#         self._title = title
#         self._puzzleCode = puzzleCode
#         self._citationCode = citationCode
#         self._puzzleSolution = puzzleSolution
#         self._citationSolution = citationSolution
#
#         print("just after setting properties")
#         QDialog.accept(self)
#
#     def reject(self):
#         print("Got to CollectionDialog's reject() routine")
#         QDialog.reject(self)
#
#
#
