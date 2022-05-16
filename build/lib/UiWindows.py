import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg

ui_folder = os.path.join(os.path.dirname(__file__), "climbdoc")
main_window_ui, _ = uic.loadUiType(os.path.join(ui_folder, "mainwindow.ui"))
ard_not_found_ui, _ = uic.loadUiType(os.path.join(ui_folder, "ardnotfound.ui"))
initials_ui, _ = uic.loadUiType(os.path.join(ui_folder, "initials.ui"))
measurement_ui, _ = uic.loadUiType(os.path.join(ui_folder, "measurement.ui"))
between_ui, _ = uic.loadUiType(os.path.join(ui_folder, "between.ui"))
datarepr_ui, _ = uic.loadUiType(os.path.join(ui_folder, "datarepr.ui"))
results_ui, _ = uic.loadUiType(os.path.join(ui_folder, "results.ui"))


class MainWindow(QtWidgets.QMainWindow, main_window_ui):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class ArdNotFound(QtWidgets.QMainWindow, ard_not_found_ui):
    def __init__(self, parent=None):
        super(ArdNotFound, self).__init__(parent)
        self.setupUi(self)


class Initials(QtWidgets.QMainWindow, initials_ui):
    def __init__(self, parent=None):
        super(Initials, self).__init__(parent)
        self.setupUi(self)
        self.label_2.setVisible(False)

    def already_exist_show_hide(self):
        self.label_2.setVisible(not (self.label_2.isVisible()))

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            print("Enter pressed")
        else:
            super().keyPressEvent(qKeyEvent)


class Measurement(QtWidgets.QMainWindow, measurement_ui):
    def __init__(self, app, parent=None):
        super(Measurement, self).__init__(parent)
        self.setupUi(self)
        self.app = app

    def countdown(self):
        i = 9
        j = 1
        ot = time.time()
        ot2 = time.time()
        while i >= 0:
            if time.time() - ot > 1:
                self.app.processEvents()
                self.lcdNumber.setProperty("intValue", i)
                i -= 1
                ot = time.time()
            if time.time() - ot2 > 0.1:
                self.app.processEvents()
                self.progressBar.setProperty("value", j)
                j += 1
                ot2 = time.time()
        self.progressBar.setProperty("value", 100)


class Between(QtWidgets.QMainWindow, between_ui):
    def __init__(self, parent=None):
        super(Between, self).__init__(parent)
        self.setupUi(self)


class DataRepr(QtWidgets.QMainWindow, datarepr_ui):
    def __init__(self, parent=None):
        super(DataRepr, self).__init__(parent)
        self.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)


class Results(QtWidgets.QMainWindow, results_ui):
    def __init__(self, parent=None):
        super(Results, self).__init__(parent)
        self.setupUi(self)
        self.label_lk.setVisible(False)
        self.label_lr.setVisible(False)
        self.label_lm.setVisible(False)
        self.label_lz.setVisible(False)
        self.label_rz.setVisible(False)
        self.label_rm.setVisible(False)
        self.label_rr.setVisible(False)
        self.label_rk.setVisible(False)
