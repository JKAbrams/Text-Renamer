# Text Renamer

Conceptual renaming tool using the free flow concept of a text editor for file renaming.


## How to use

Operation is very simple and should be rather intuative.
The right panel show the file names as text, it can be manipulated as plain text or copied to another tool for manipulation.
Clicking the Rename button renames the files according to the text to the right.
To the right one selects a folder, the content of this folder is displayed in the center.


## Features

Has the ability to hide file extensions.


### Notes

* Selecting another folder will discard any not comitted changes in the text field.
* If a file could not be renamed it will simply skip it and go to the next one.
* Cannot resolve circular dependancies, ie. switching the names of files A and B. *(Will be fixed soon)*.
* Filtering does not work yet.


## Screenshot

![Text Renamer Screenshot][screenshot]


[screenshot]: screenshot.png "Screenshot of Text Renamer"
