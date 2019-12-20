# Text Renamer

Conceptual renaming tool using the free flow concept of a text editor for file renaming.

It is particularly useful to operate on many file at once to do similar changes.

## How to use

Operation is very simple and should be rather intuative.

In the ***left panel*** one selects a folder, the content of this folder is displayed in the ***center panel***.

The ***right panel*** show the file names in an editable text filed, it can be manipulated as plain text or copied any other text based tool for manipulation (pro tip).

Clicking the **Rename** button renames the files according to the text in the ***right panel***.


## Features

Has the ability to hide file extensions.


## Notes

* Selecting another folder will discard any not comitted changes in the text field.
* If a file could not be renamed it will simply skip it and go to the next one.
* Cannot resolve circular dependencies, ie. switching the names two files does not work. *(Will be fixed soon)*
* Filtering does not work yet. *(Will be added soon)*
* The file view is automatically updated if changes happens to the filesystem (if a file is added or removed), this will trigger an update of the text box and reset its content. This will be fixed in a later version when I figured the right way for how to deal with file system changes.


## Screenshot

![Text Renamer Screenshot][screenshot]


[screenshot]: screenshot.png "Screenshot of Text Renamer"


## Prerequisites:

The application is built in **Python 3** and **Qt5** through **PyQt5**.

Requred python modules is **pyqt5**

    pip install pyqt5
    
Run the application

    python textRenamer.py
