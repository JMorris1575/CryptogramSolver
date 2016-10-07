from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.cryptogram_solver_ui import uiElements


class UserInterfaceSetup(object):

    def uiSetup(self):

        self.resize(800, 600)
        menuBar = self.menuBar()
        toolBar = QToolBar(self)
        self.addToolBar(toolBar)

        self.panel = QWidget()
        self.setCentralWidget(self.panel)
        self.setupBars(menuBar, toolBar)
        self.panel.resize(self.width(), self.height() - menuBar.height() - toolBar.height())
        self._keys = []
        self._rows = 5
        self._columns = 40
        self._currentLetterBox = -1
        self._activeUnits = []
        self.setupPlayPanel(self.panel)

    def setupBars(self, menuBar, toolBar):
        self.createFileControls(menuBar, toolBar)
        self.createPuzzleControls(menuBar, toolBar)
        self.createAdminControls(menuBar, toolBar)
        self.createHelpControls(menuBar, toolBar)

    def setActiveUnits(self, unitList):
        self._activeUnits = unitList

    # File Controls Section
    # ------------------------------------------------------------------------------------------------------------------

    def createFileControls(self, menuBar, toolBar):
        fileMenu = QMenu("&File", self)
        fileMenu.setToolTipsVisible(True)
        menuBar.addMenu(fileMenu)

        newPlayerAction = QAction(QIcon("images/detectiveHat.png"), "&New Player...", self)
        newPlayerAction.setShortcuts(QKeySequence.New)
        newPlayerAction.setToolTip("Enroll as a new player.")
        newPlayerAction.triggered.connect(self.enrollNewPlayer)
        fileMenu.addAction(newPlayerAction)
        toolBar.addAction(newPlayerAction)

        loginAction = QAction(QIcon("images/fingerprint.png"), "&Login...", self)
        loginAction.setToolTip("Login to play.")
        loginAction.triggered.connect(self.login)
        fileMenu.addAction(loginAction)
        toolBar.addAction(loginAction)

        fileMenu.addSeparator()

        openAction = QAction(QIcon("images/OpenCollection.png"), "&Open Collection...", self)
        openAction.setShortcut(QKeySequence.Open)
        openAction.setToolTip("Open a set of puzzles to solve.")
        openAction.triggered.connect(self.openCollection)
        fileMenu.addAction(openAction)
        toolBar.addAction(openAction)

        saveAction = QAction(QIcon("images/SaveIcon.png"), "&Save Progress", self)
        saveAction.setShortcut(QKeySequence.Save)
        saveAction.setToolTip("Save your current puzzle solving progress.")
        saveAction.triggered.connect(self.saveProgress)
        fileMenu.addAction(saveAction)
        toolBar.addAction(saveAction)

        fileMenu.addSeparator()

        exitAction = QAction(QIcon("images/underConstruction.png"), "E&xit", self)
        exitAction.setToolTip("Exit this program.")
        exitAction.triggered.connect(self.exitGame)
        fileMenu.addAction(exitAction)

        toolBar.addSeparator()

    # Puzzle Controls Section
    # ------------------------------------------------------------------------------------------------------------------

    def createPuzzleControls(self, menuBar, toolBar):
        puzzleMenu = QMenu("&Puzzle", self)
        puzzleMenu.setToolTipsVisible(True)
        menuBar.addMenu(puzzleMenu)

        selectAction = QAction(QIcon("images/underConstruction.png"), "&Select Puzzle...", self)
        selectAction.triggered.connect(self.selectPuzzle)
        puzzleMenu.addAction(selectAction)

        self.previousAction = QAction(QIcon("images/PreviousIcon.png"), "&Previous Puzzle", self)
        self.previousAction.setShortcut(QKeySequence.MoveToPreviousPage)
        self.previousAction.setToolTip("Go to the previous puzzle in the collection.")
        self.previousAction.triggered.connect(self.previousPuzzle)
        puzzleMenu.addAction(self.previousAction)
        toolBar.addAction(self.previousAction)

        self.puzzleSelector = QComboBox()
        self.puzzleSelector.setMinimumWidth(100)
        self.puzzleSelector.currentIndexChanged.connect(self.puzzleSelectorIndexChanged)
        toolBar.addWidget(self.puzzleSelector)

        self.nextAction = QAction(QIcon("images/NextIcon.png"), "&Next Puzzle", self)
        self.nextAction.setShortcut(QKeySequence.MoveToNextPage)
        self.nextAction.setToolTip("Go to the next puzzle in the collection.")
        self.nextAction.triggered.connect(self.nextPuzzle)
        puzzleMenu.addAction(self.nextAction)
        toolBar.addAction(self.nextAction)

        puzzleMenu.addSeparator()
        toolBar.addSeparator()

        hintAction = QAction(QIcon("images/underConstruction.png"), "Get &Hint", self)
        hintAction.setToolTip("Get a hint for this puzzle.")
        hintAction.triggered.connect(self.giveHint)
        puzzleMenu.addAction(hintAction)
        toolBar.addAction(hintAction)

        clearAction = QAction(QIcon("images/EraserIcon.png"), "&Clear Puzzle", self)
        clearAction.setToolTip("Clear your current solution and start over.")
        clearAction.triggered.connect(self.clearPuzzle)
        puzzleMenu.addAction(clearAction)
        toolBar.addAction(clearAction)

        giveUpAction = QAction(QIcon("images/Give-upIcon.png"), "&Give Up", self)
        giveUpAction.setToolTip("Give up on this puzzle and see the solution.")
        giveUpAction.triggered.connect(self.giveUp)
        puzzleMenu.addAction(giveUpAction)
        toolBar.addAction(giveUpAction)

        puzzleMenu.addSeparator()

        checkAction = QAction(QIcon("images/underConstruction.png"), "&Check Solution", self)
        checkAction.setToolTip("Check your answer to see if you are right.")
        checkAction.triggered.connect(self.checkSolution)
        puzzleMenu.addAction(checkAction)
        toolBar.addAction(checkAction)

        self.adminSeparator = toolBar.addSeparator()

    # Admin Controls Section
    # ------------------------------------------------------------------------------------------------------------------

    def createAdminControls(self, menuBar, toolBar):
        adminMenu = QMenu("&Admin", self)
        adminMenu.setToolTipsVisible(True)
        self.adminAction = menuBar.addMenu(adminMenu)
        self.adminAction.setToolTip("Add or edit puzzles and collections of puzzles.")

        self.createAction = QAction(QIcon("images/addCollectionIcon.png"), "&Create Collection...", self)
        self.createAction.setShortcut(QKeySequence("Alt+Ctrl+C"))
        self.createAction.setShortcutContext(Qt.WidgetShortcut)
        self.createAction.setToolTip("Create and edit a new puzzle collection.")
        self.createAction.triggered.connect(self.createCollection)
        adminMenu.addAction(self.createAction)
        toolBar.addAction(self.createAction)

        self.editAction = QAction(QIcon("images/editpuzzleicon-2.png"), "Add/&Edit Puzzles...", self)
        self.editAction.setShortcut(QKeySequence("Alt+Ctrl+E"))
        self.editAction.setShortcutContext(Qt.WidgetShortcut)
        self.editAction.setToolTip("Add, edit or delete puzzles in the current collection.")
        self.editAction.triggered.connect(self.addEditPuzzles)
        adminMenu.addAction(self.editAction)
        toolBar.addAction(self.editAction)

        self.deleteAction = QAction(QIcon("images/underConstruction.png"), "&Delete Collection...", self)
        self.deleteAction.setShortcut(QKeySequence("Alt+Ctrl+X"))
        self.deleteAction.setShortcutContext(Qt.WidgetShortcut)
        self.deleteAction.setToolTip("Delete the current collection.")
        self.deleteAction.triggered.connect(self.deleteCollection)
        adminMenu.addAction(self.deleteAction)
        toolBar.addAction(self.deleteAction)

        self.saveSolutionAction = QAction(QIcon("images/underConstruction.png"), "&Save Solution", self)
        self.saveSolutionAction.setShortcut(QKeySequence("Alt+Ctrl+S"))
        self.saveSolutionAction.setShortcutContext(Qt.WidgetShortcut)
        self.saveSolutionAction.setToolTip("Save the current solution as the correct solution of this puzzle.")
        self.saveSolutionAction.triggered.connect(self.saveSolution)
        adminMenu.addAction(self.saveSolutionAction)
        toolBar.addAction(self.saveSolutionAction)

        self.setAdminVisibility(True)       # set this to true only during development

    # Help Controls Section
    # ------------------------------------------------------------------------------------------------------------------

    def createHelpControls(self, menuBar, toolBar):
        helpMenu = QMenu("&Help", self)
        helpMenu.setToolTipsVisible(True)
        menuBar.addMenu(helpMenu)

        toolBar.addSeparator()

        helpAction = QAction(QIcon("images/helpicon512.png"), "&Help", self)
        helpAction.setShortcuts(QKeySequence.HelpContents)
        helpAction.setToolTip("Display help for Cryptogram Solver")
        helpAction.triggered.connect(self.startHelp)
        helpMenu.addAction(helpAction)
        toolBar.addAction(helpAction)

        helpMenu.addSeparator()

        aboutAction = QAction(QIcon("images/underConstruction.png"), "&About", self)
        aboutAction.triggered.connect(self.displayAbout)
        helpMenu.addAction(aboutAction)


    def setupPlayPanel(self, panel):

        self.drawGameInfoPanel(panel)
        self.createPuzzleArea(panel)
        self.drawKeyboard(panel)

    def drawGameInfoPanel(self, panel):

        self.MARGIN = 5

        self.largeFont = QFont("Times New Roman", 14)
        self.largeMetrics = QFontMetrics(self.largeFont)
        self.largeItalicFont = QFont("Times New Roman", 14)
        self.largeItalicFont.setItalic(True)
        self.largeItalicMetrics = QFontMetrics(self.largeItalicFont)
        self.smallFont = QFont("Arial", 10)
        self.smallMetrics = QFontMetrics(self.smallFont)

        self.collectionLabel = QLabel(panel)
        self.collectionLabel.setFont(self.largeFont)
        self.collectionLabel.setStyleSheet("QLabel { color: green }")
        self.collectionLabel.move(self.MARGIN, 0)

        self.authorLabel = QLabel(panel)
        self.authorLabel.setFont(self.largeItalicFont)
        self.authorLabel.setStyleSheet("QLabel { color: green }")
        self.authorLabel.move(2 * self.MARGIN + self.collectionLabel.width(), 0)

        self.puzzleCountLabel = QLabel(panel)
        self.puzzleCountLabel.setFont(self.smallFont)
        self.puzzleCountLabel.move(self.MARGIN, self.MARGIN + self.smallMetrics.height())

        self.playerLabel = QLabel(panel)
        self.playerLabel.setFont(self.smallFont)
        self.playerLabel.move(panel.width() - self.smallMetrics.width(self.playerLabel.text()) - self.MARGIN, 0)

        self.infoLabel = QLabel(panel)
        self.infoLabel.setFont(self.smallFont)
        self.infoLabel.move(panel.width() - self.smallMetrics.width(self.infoLabel.text()) - self.MARGIN,
                            self.MARGIN + self.playerLabel.height())

        topLine = QFrame(panel)
        topLine.setFrameStyle((QFrame.HLine | QFrame.Sunken))
        topLine.resize(800,3)
        topLine.move(0, 40)

        self.updateGameInfo(self.panel)

    def createPuzzleArea(self, panel):

        xbase = 20
        ybase = 50
        letterWidth = 15
        letterHeight = 3 * letterWidth
        self.letterUnits = []
        for row in range(self._rows):
            for column in range(self._columns):
                xpos = xbase + column * (letterWidth + 4)
                ypos = ybase + row * (letterHeight + letterHeight/2)
                letterUnit = uiElements.LetterUnit(' ', ' ', xpos, ypos,
                                                   QSize(letterWidth, letterHeight), panel)
                letterUnit.clicked.connect(self.letterUnitClicked)
                # letterUnit.setIndex(len(self.letterUnits))   # the current length of self.letterUnits will be the index
                self.letterUnits.append(letterUnit)
        # self.moveTo(self.letterUnits[0])
        # # self.letterUnits[0].setRedFrame(True)
        # self._currentLetterBox = 0

    def drawKeyboard(self, panel):

        keyboardLineOne = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        keyboardLineTwo = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
        keyboardLineThree = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']

        keySize = 40
        keyGap = 5
        xbase = (panel.width() - (10 * keySize + 9 * keyGap))/2
        xposition = xbase
        yposition = 400
        for key in keyboardLineOne:
            button = self.makeKeyButton(key, keySize, xposition, yposition, panel)
            button.clicked.connect(self.keyButtonClicked)
            xposition += keySize + keyGap
        yposition += keySize + keyGap
        xposition = xbase + keySize/2
        for key in keyboardLineTwo:
            button = self.makeKeyButton(key, keySize, xposition, yposition, panel)
            button.clicked.connect(self.keyButtonClicked)
            xposition += keySize + keyGap
        yposition += keySize + keyGap
        xposition = xbase + keySize + 2
        for key in keyboardLineThree:
            button = self.makeKeyButton(key, keySize, xposition, yposition, panel)
            button.clicked.connect(self.keyButtonClicked)
            xposition += keySize + keyGap

    def makeKeyButton(self, key, keySize, xpos, ypos, parent):
        button = QPushButton(key, parent)
        button.resize(keySize, keySize)
        button.move(xpos, ypos)
        button.setFont(QFont("Arial", 14))
        return button




