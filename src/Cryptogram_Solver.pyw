import data_structures
import file_handler
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from src.cryptogram_solver_ui import uiElements, SetupUI


class MainWindow(QMainWindow, SetupUI.UserInterfaceSetup):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self._collection = data_structures.Collection("Jim's Fake Collection", "Jim Morris")
        self.uiSetup(self)      # this is located in the file SetupUI.py
        self._currentPuzzleIndex = None

    def collection(self):
        return self._collection

    def setCollection(self, collection):
        self._collection = collection

    # File Menu Implementation Section
    #-------------------------------------------------------------------------------------------------------------------

    def enrollNewPlayer(self):
        print("Got to enrollNew Player")

    def login(self):
        print("Got to login")

    def openCollection(self):
        # open a file dialog box and select a .col file from the Collections directory
        fileInfo = QFileDialog.getOpenFileName(self, "Open Collection",
                                               "../Collections", "Collections (*.col)")
        filename = fileInfo[0]
        self.setCollection(file_handler.readCollection(filename))
        self.updatePuzzleSelector(self._collection.puzzles())
        self.updateGameInfo(self.panel)

    def saveProgress(self):
        print('Got to saveProgress')

    def exitGame(self):
        self.close()  # sends control to self.closeEvent which does all necessary checking

    def closeEvent(self, Event):
        print("Got to closeEvent")

    # Puzzle Menu Implementation Section
    #-------------------------------------------------------------------------------------------------------------------

    def selectPuzzle(self):
        print("Got to selectPuzzle")


    def previousPuzzle(self):
        print("Got to previousPuzzle.")

    def puzzleSelectorIndexChanged(self):
        print("Got to puzzleSelectorIndexChanged")
        self._currentPuzzleIndex = self.puzzleSelector.currentIndex()
        print("A")
        code = self.collection().puzzles()[self._currentPuzzleIndex].puzzleCode()
        print("B code = ", code)
        codeLength = len(code)
        print("C codeLength = ", codeLength)
        count = 0
        print("D count = ", count)
        for unit in self.letterUnits:
            if count < codeLength:
                unit.setCodeLetter(code[count])
            else:
                unit.setCodeLetter(' ')
            count += 1
        for unit in self.letterUnits:
            print(unit.codeLetter())


    def nextPuzzle(self, direction=None):
        print("Got to nextPuzzle.")


    def giveHint(self, direction=None):
        print("Got to giveHint.")


    def clearPuzzle(self, direction=None):
        print("Got to clearPuzzle.")


    def giveUp(self):
        print("Got to giveUp.")


    def checkSolution(self):
        print("Got to checkSolution")

    # Admin Menu Implementation Section
    #-------------------------------------------------------------------------------------------------------------------

    def createCollection(self):

        dialog = uiElements.AddCollection()
        if dialog.exec():
            collection = data_structures.Collection(dialog.name(), dialog.author(), dialog.puzzles())
            self.setCollection(collection)
            file_handler.saveCollection(collection)
            #self.updatePuzzleSelector(collection.puzzles())
            self.updateGameInfo(self.panel)

    def editCollection(self):
        if self.collection():
            dialog = uiElements.AddEditCollection(self._collection, self._currentPuzzleIndex)
            if dialog.exec():
                collection = data_structures.Collection(dialog.name(), dialog.author(), dialog.puzzles())
                self.setCollection(collection)
                file_handler.saveCollection(collection)
                self.updatePuzzleSelector(collection.puzzles())
                self.updateGameInfo(self.panel)

    def deleteCollection(self):
        print("Got to deleteCollection")

    def saveSolution(self):
        print("Got to saveSolution")

    def setAdminVisibility(self, setting=False):
        self.adminAction.setVisible(setting)
        self.adminSeparator.setVisible(setting)
        self.createAction.setVisible(setting)
        self.editAction.setVisible(setting)
        self.deleteAction.setVisible(setting)
        self.saveSolutionAction.setVisible(setting)

    # Help Menu Implementation Section
    #-------------------------------------------------------------------------------------------------------------------

    def startHelp(self):
        if not self.displayHelp():
            QMessageBox.warning(self, "Help Error", "Help process timed out.  Help system currently unavailable.")


    def displayHelp(self):
        program = "assistant"
        arguments = ["-collectionFile",
                     "../docs/_build/qthelp/CryptogramSolver.qhc",
                     "-enableRemoteControl", ]
        helpProcess = QProcess(self)
        helpProcess.start(program, arguments)
        if not helpProcess.waitForStarted():
            return False
        print("About to send a message to helpProcess")
        ba = QByteArray()
        ba.append("setSource introduction.html\n;")
        ba.append("expandToc 1")
        helpProcess.write(ba)
        return True


    def displayAbout(self):
        print('Got to displayAbout')

    def updateGameInfo(self, panel):
        self.collectionLabel.setText(self.collection().name())
        self.collectionLabel.resize(self.largeMetrics.width(self.collectionLabel.text()), self.largeMetrics.height())

        if self.collection().author():
            self.authorLabel.setText("by " + self.collection().author())
        self.authorLabel.resize(self.largeItalicMetrics.width(self.authorLabel.text()), self.largeItalicMetrics.height())
        self.authorLabel.move(2 * self.MARGIN + self.collectionLabel.width(), 0)

        puzzleCount = len(self.collection().puzzles())
        if puzzleCount == 0:
            countText = "There are no puzzles in this collection.  An administrator needs to add some."
            self.puzzleSelector.setEnabled(False)
        elif puzzleCount == 1:
            countText = "There is " + str(puzzleCount) + " puzzle in the collection."
            self.puzzleSelector.setEnabled(True)
        else:
            countText = "There are " + str(puzzleCount) + " puzzles in the collection."
            self.puzzleSelector.setEnabled(True)

        self.puzzleCountLabel.setText(countText)
        self.puzzleCountLabel.resize(self.smallMetrics.width(self.puzzleCountLabel.text()), self.smallMetrics.height())
        self.puzzleCountLabel.move(self.MARGIN, self.MARGIN + self.smallMetrics.height())

        self.playerLabel.setText("Current Player: " + "Jim")
        self.playerLabel.resize(self.smallMetrics.width(self.playerLabel.text()), self.smallMetrics.height())
        self.playerLabel.move(panel.width() - self.smallMetrics.width(self.playerLabel.text()) - self.MARGIN, 0)

        solved = 3          # Eventually this information will be held in player files
        started = 1
        infoText = ""
        if solved == 1:
            infoText += str(solved) + " Puzzle Solved"
        elif solved > 1:
            infoText += str(solved) + " Puzzles Solved"
        if started == 1:
            infoText += ", " + str(started) + " Puzzle Started"
        elif started > 1:
            infoText += ", " + str(solved) + " Puzzles Started"
        self.infoLabel.setText(infoText)
        self.infoLabel.resize(self.smallMetrics.width(self.infoLabel.text()), self.smallMetrics.height())
        self.infoLabel.move(panel.width() - self.smallMetrics.width(self.infoLabel.text()) - self.MARGIN,
                            self.MARGIN + self.playerLabel.height())

    def updatePuzzleSelector(self, puzzles):

        self.puzzleSelector.clear()
        for puzzle in puzzles:
            self.puzzleSelector.addItem(puzzle.puzzleTitle())


if __name__ == "__main__":
    import sys
    print(sys.argv)
    app = QApplication(sys.argv)
    app.setApplicationName('Cryptogram Solver')
    app.setWindowIcon(QIcon("..\images\sherlock.png"))
    form = MainWindow()
    form.show()
    app.exec()


