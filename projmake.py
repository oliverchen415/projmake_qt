import sys
import os
from pathlib import Path
from datetime import date
from PySide6.QtWidgets import QApplication, QCheckBox, QFileDialog, QGroupBox, QHBoxLayout, QLineEdit, QMessageBox, QRadioButton, QVBoxLayout, QWidget, QPushButton
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
        self.fileSearchButton.setToolTip("Search for a directory for your project")

        self.goProj = QRadioButton("Go Project")
        self.goProj.setToolTip("You will still need a go.mod file")
        self.pyProj = QRadioButton("Python Project")
        self.versionControlFiles = QCheckBox("Create README.md and .gitignore?")
        self.versionControlFiles.setToolTip("Creates the files used in online version control, such as Github")
        self.pyProj.setChecked(True)
        self.versionControlFiles.setChecked(True)

        projSelect = QGroupBox("Project Selection")
        projectOptions = QVBoxLayout()
        projectOptions.addWidget(self.pyProj)
        projectOptions.addWidget(self.goProj)
        projectOptions.addWidget(self.versionControlFiles)
        projectOptions.stretch(1)
        projSelect.setLayout(projectOptions)

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
        fileSearch = QFileDialog.getExistingDirectory(self, "Select a Directory...", "C:/Users")
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
            if self.versionControlFiles.isChecked():
                open("README.md", "a").close()
                open(".gitignore", "a").close()

if __name__ == "__main__":
    app = QApplication([])
    maker = Maker()
    maker.resize(400, 100)
    maker.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())