# Climbdoc
This repository contains the python code for an application written for the "Kletterretter" project at the WHS in Bocholt.
## QT
The UI framework used in this application is QT. The python conversion was done using PyQT 5.
The process for UI changes is changing the UI files contained in the "climbdoc" folder using the QT-Creator. After that the build.py file has to be run, which
uses the uic library to compile the UI files to .py files. The new .py file(s) have to be manually moved to the main directory to be used by the program, as the
UIWindows.py file imports from the main directory.
