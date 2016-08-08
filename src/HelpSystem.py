"""
Creates a class called HelpWindow to display html help pages created by SphinxDoc
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class HelpWindow(QDialog):

    def __init__(self, parent=None):

        super(HelpWindow, self).__init__(parent)

        self.setSizeGripEnabled(True)
        self.setWindowTitle("Cryptogram Solver Help")
        self.setMinimumSize(300, 200)
        self.resize(600, 400)
        self.setWindowModality(Qt.NonModal)

        self.textArea = QTextBrowser()
        self.textArea.setStyleSheet("QTextEdit { background: ivory }")
        self.textArea.setText("This is test text.")
        self.textArea.setReadOnly(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.textArea)
        self.setLayout(layout)

        if not self.load("../docs/_build/html/index.html"):
            QMessageBox.warning(self, "Help Error", "Can't find help's index.html file.\n\nHelp will be unusable.")

        print('self.textArea.searchPaths() = ', self.textArea.searchPaths())

        program = "assistant"
        arguments = ["-collectionFile", "../docs/_build/qthelp/CryptogramSolver.qhc"]
        helpProcess = QProcess(self)
        helpProcess.start(program, arguments)

        self.show()

    def load(self, f):          # based on the Qt example program textedit.py
        if not QFile.exists(f):
            return False

        fh = QFile(f)
        if not fh.open(QFile.ReadOnly):
            return False

        #self.textArea.setSource(QUrl(f))

        data = fh.readAll()
        codec = QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        self.textArea.setPlainText(unistr)
        return True



