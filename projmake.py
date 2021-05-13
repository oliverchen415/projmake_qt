import sys
import os
from pathlib import Path
from datetime import date
from PySide6.QtWidgets import QApplication, QFileDialog, QGroupBox, QHBoxLayout, QLineEdit, QMessageBox, QRadioButton, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Slot

class Maker(QWidget):
    def __init__(self, parent=None):
        super(Maker, self).__init__(parent)

        self.setWindowTitle("Project Maker")

        self.userFilepath = QLineEdit()
        self.userFilepath.setPlaceholderText("Your filepath here...")
        self.projName = QLineEdit()
        self.projName.setPlaceholderText("Your project name here...")
        self.makeButton = QPushButton("Create Project")
        self.fileSearchButton = QPushButton("...")

        self.goProj = QRadioButton("Go Project")
        self.pyProj = QRadioButton("Python Project")
        self.pyProj.setChecked(True)

        projSelect = QGroupBox("Project Selection")
        radioButtons = QVBoxLayout()
        radioButtons.addWidget(self.pyProj)
        radioButtons.addWidget(self.goProj)
        radioButtons.stretch(1)
        projSelect.setLayout(radioButtons)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.userFilepath)
        searchLayout.addWidget(self.fileSearchButton)
        searchLayout.stretch(1)

        layout = QVBoxLayout()
        layout.addLayout(searchLayout)
        layout.addWidget(self.projName)
        layout.addWidget(self.makeButton)
        layout.addWidget(self.fileSearchButton)
        layout.addWidget(projSelect)
        self.setLayout(layout)

        self.makeButton.clicked.connect(self.createFiles)
        self.fileSearchButton.clicked.connect(self.onClickFileSearch)

    @Slot()
    def onClickFileSearch(self):
        fileSearch = QFileDialog.getExistingDirectory(self, "...", "C:/Users")
        self.userFilepath.setText(fileSearch)

    @Slot()
    def createFiles(self):
        p = Path(f"{self.userFilepath.text()}/{self.projName.text()}")
        try:
            p.mkdir()
        except FileExistsError as exc:
            msgbox = QMessageBox()
            msgbox.setText(f"{exc}")
            msgbox.exec()
        else:
            os.chdir(f"{self.userFilepath.text()}\\{self.projName.text()}")
            if self.pyProj.isChecked():
                fileType = "py"
            elif self.goProj.isChecked():
                fileType = "go"
            with open (f"{self.projName.text()}.{fileType}", "w") as f:
                f.write(f"# Created on {date.today()}")

if __name__ == "__main__":
    app = QApplication([])
    maker = Maker()
    maker.resize(400, 100)
    maker.show()
    sys.exit(app.exec())