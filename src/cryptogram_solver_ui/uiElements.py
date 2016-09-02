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


class AddCollection(QDialog):

    """
    Invoke this class without parameters when creating a new collection,
    invoke it with at least name set to edit the current collection
    """

    def __init__(self, currentCollection=None):
        super(AddCollection, self).__init__()       # you removed parent from the .__init__(parent)
        self._currentCollection = currentCollection
        self._name = ""
        self._author = ""

        if self._currentCollection:     # collection present means edit mode, otherwise we are adding a new collection
            self._mode = "Edit"
        else:
            self._mode = "New"
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
class AddEditPuzzle(QDialog):

    def __init__(self, collection=None, currentPuzzleIndex=None, parent=None):
        print('Initializing AddEditPuzzle')
        super(AddEditPuzzle, self).__init__(parent)

        self._collection = collection
        self._currentPuzzleIndex = currentPuzzleIndex
        print('About to go into setupUI')
        self.setupUI()

    def collection(self):
        return self._collection

    def currentPuzzleIndex(self):
        return self._currentPuzzleIndex

    def title(self):
        return self._title

    def puzzleCode(self):
        return self._puzzleCode

    def citationCode(self):
        return self._citationCode

    def puzzleSolution(self):
        return self._puzzleSolution

    def citationSolution(self):
        return self._citationSolution

    def hints(self):
        return self._hints

    def setupUI(self):

        print('in setupUI')
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

    def updateUI(self):
        """
        Displays the current collection in the dialog box, if any, and
        enables the corresponding controls
        :return: None
        """
        print("updateUI self.currentCollection(): ", self.currentCollection())
        if self._mode == "Edit":
            currentCollection = self.currentCollection()
            self.collectionNameEdit.setText(currentCollection.name())
            self.authorEdit.setText(currentCollection.author())
            self.addPuzzleButton.setEnabled(True)
            # ToDo
            """correct this routine so that it handles all cases:
                --  when adding a new collection
                --  when adding a puzzle to an existing collection
                --  when editing an old collection
            """
            print("currentCollection.puzzles(): ", currentCollection.puzzles())
            print("self.currentPuzzleIndex(): ", self.currentPuzzleIndex())
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
        else:
            pass

#        dialogButtonBox = QDialogButtonBox()

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

    def deletePuzzle(self):
        print("Got to deletePuzzle")


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
        # self._currentPuzzleIndex = self.puzzleSelector.currentIndex()
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

