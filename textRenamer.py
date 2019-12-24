#!/usr/bin/env python3

import os
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QDir, QTimer
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel


class TextRenamer(QtWidgets.QMainWindow):
    ui = None
    
    currentFullNames = None
    currentExtensions = None
    path = None
    currentIndex = None
    
    showExtension = False

    def __init__(self):

        # init user interface:
        super(TextRenamer, self).__init__()
        self.show()
        scriptPath = os.path.dirname(os.path.abspath(__file__))     # Fails if the script is executed by exec()
        
        self.ui = uic.loadUi(scriptPath + '/' + 'textRenamer.ui', self)

        # TODO: remember last used path
        self.path = QDir.rootPath() 

        # Set up files and folder views
        self.foldersModel = QFileSystemModel()
        self.foldersModel.setRootPath(self.path)
        self.foldersModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.filesModel = QFileSystemModel()
        self.filesModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)

        self.ui.folderView.setModel(self.foldersModel)
        self.ui.filesView.setModel(self.filesModel)

        # Remove all columns but the folder name
        self.ui.folderView.setRootIndex(self.foldersModel.index(self.path))
        self.ui.folderView.hideColumn(1);
        self.ui.folderView.hideColumn(2);
        self.ui.folderView.hideColumn(3);

        # Set path for start
        self.ui.filesView.setRootIndex(self.filesModel.index(self.path))

        # Event handlers:
        self.ui.renameButton.clicked.connect(self.renameFiles)
        self.ui.folderView.clicked.connect(self.openFolder)
        self.filesModel.directoryLoaded.connect(self.loadedFolder)
        self.ui.extensionCheckbox.stateChanged.connect(self.extensionCheckboxChanged)


    def extensionCheckboxChanged(self, state):
        if state == 0:
            self.showExtension = False
        else:
            self.showExtension = True
        self.readCurrentNames()


    def loadedFolder(self, path):
        # Delay reading to get correct file order
        QTimer.singleShot(100, self.readCurrentNames)


    def readCurrentNames(self):
        # Reset
        self.currentFullNames = []

        for i in range(self.filesModel.rowCount(self.currentIndex)):
            self.currentFullNames.append(self.currentIndex.child(i,0).data())

        self.currentNames = [os.path.splitext(x)[0] for x in self.currentFullNames]
        self.currentExtensions = [os.path.splitext(x)[1] for x in self.currentFullNames]

        if self.showExtension:
            fileListText = '\n'.join(self.currentFullNames)
        else:
            fileListText = '\n'.join(self.currentNames)
        
        self.ui.newText.setPlainText(fileListText)

        # Only enable the rename button once everything is loaded
        self.ui.renameButton.setEnabled(True)


    def openFolder(self, index):
        self.path = self.foldersModel.fileInfo(index).absoluteFilePath()
        self.currentIndex = self.filesModel.setRootPath(self.path)
        self.ui.filesView.setRootIndex(self.currentIndex)
        # Clear info text
        self.ui.errorLabel.setText("")


    def renameFiles(self):
        # Read new names (only use as many rows as we have currentFullNames):
        newNames = self.ui.newText.toPlainText().split('\n')[:len(self.currentFullNames)]
        
        if self.showExtension:
            self.newFullNames = newNames
        else:
            # Add extension
            self.newFullNames = [i + j for i, j in zip(newNames, self.currentExtensions)]

        # TODO: Add temporary filenames for cases where a new name conflicts with a name that has not yet been renamed

        # Sanity checkes:
        enoughNames = False
        allNamesHaveCharacters = False
        allNamesUnique = False
        
        # Sanity check: All new names have characters
        if len(self.newFullNames) >= len(self.currentFullNames):
            enoughNames = True
        else:
            self.ui.errorLabel.setText("Error: Not enough names given")
        
        # Sanity chcek: All names have characters
        allNamesHaveCharacters = True
        for newName in self.newFullNames:
            if newName == "":
                allNamesHaveCharacters = False
                self.ui.errorLabel.setText("Error: Blank new name")
                break
        
        # Sanity chcek: All names unique
        if self.allUnique(self.newFullNames):
            allNamesUnique = True
        else:
            self.ui.errorLabel.setText("Error: All names have to be unique")

        renamedCount = 0
        notChangedCount = 0
        errorCount = 0
        # Rename
        if enoughNames and allNamesHaveCharacters and allNamesUnique:
            for currentName, newName in zip(self.currentFullNames, self.newFullNames):
                print(self.path + "/" + currentName + " > " + newName)

                # Dont rename needlessly
                if not currentName == newName:
                    currentFile = os.path.join(self.path, currentName).replace(os.sep, '/')
                    newFileName = os.path.join(self.path, newName).replace(os.sep, '/')
                    # Only rename if the current file exists
                    if os.path.exists(currentFile):
                        renamedOk = QtCore.QFile.rename(currentFile, newFileName)
                        if not renamedOk:
                            errorCount += 1
                        renamedCount += 1
                    else:
                        notChangedCoint += 1
                else:
                    notChangedCount += 1
            labelText = "Renamed: " + str(renamedCount) + " files"
            if notChangedCount > 0:
                labelText += ", No change: " + str(notChangedCount)
            if errorCount > 0:
                labelText += ", Error: " + str(errorCount)
            
            # Set info text
            self.ui.errorLabel.setText(labelText)


    # Early exit uniqueness checker, returns true if all items in x are unique
    def allUnique(self, x):
        seen = set()
        return not any(i in seen or seen.add(i) for i in x)


def startApplication():
    app = QtWidgets.QApplication(sys.argv)
    window = TextRenamer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    startApplication()
