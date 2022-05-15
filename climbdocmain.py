# link solution: https://stackoverflow.com/questions/55842776/how-to-change-ui-in-same-window-using-pyqt5
import csv
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import serial
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import threading
import dataacquisition
import UiWindows

arduino_not_found = False

serialString = ""

com_port = "COM4"
dataacquisition.com_port = com_port
try:
    serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
except serial.serialutil.SerialException:
    print("Arduino not Found")
    arduino_not_found = True
state = "menu"
data = {}
initials = "NoInitialsGiven"
averages = []
newdata = []
dataacquisition.initials = initials

if arduino_not_found:
    state = "anfError"

app = QtWidgets.QApplication(sys.argv)


def set_graphics_view(scene):
    figure = Figure()
    axes = figure.gca()
    axes.set_title("My Plot")
    seconds = []
    for element in newdata[0]:
        seconds.append(round((element - newdata[0][0]), 3))
    x = np.linspace(seconds)
    y = []
    for i in range (1, 8):
        y.append(np.linespace(newdata[i]))
    axes.plot(x, y[0], "-k", label="first one")
    axes.plot(x, y[1], "-b", label="second one")
    axes.plot(x, y[2], "-b", label="third one")
    axes.plot(x, y[3], "-b", label="fourth one")
    axes.plot(x, y[4], "-b", label="fifth one")
    axes.plot(x, y[5], "-b", label="sixth one")
    axes.plot(x, y[6], "-b", label="seventh one")
    axes.plot(x, y[7], "-b", label="eighth one")
    axes.legend()
    axes.grid(True)

    canvas = FigureCanvas(figure)
    proxy_widget = scene.addWidget(canvas)


def measure():
    wait_for_load()


    window.w.setCurrentIndex(3)

    if __name__ == "__main__":
        x = threading.Thread(target=dataacquisition.data_recording)
        y = threading.Thread(target=window.measurement_window.countdown)
        y.start()
        x.start()
        x.join()
    dataacquisition.data_writing()
    global newdata
    newdata = dataacquisition.data_processing()
    time.sleep(2)
    print("I'm done!")



def wait_for_load():
    no_zero = False
    read = []
    for i in range(0, 8):
        read.append(0.0)
    while not no_zero:
        if serialPort.in_waiting > 0:
            readstrings = serialPort.readline().decode('Ascii').split(",")
            for i in range(0, 8):
                if read[i] != '':
                    read[i] = float(readstrings[i])
        for i in read:
            if i != 0.0:
                no_zero = True
            if i == 0.0:
                no_zero = False
    serialPort.close()


def measure_once_start():           #function linked to the measure once button in the main menu
    window.w.setCurrentIndex(4)
    app.processEvents()
    measure()
    prep_data_repr(window.datarepr_window)
    window.w.setCurrentIndex(5)
    serialPort.open()


def prep_data_repr(datarpr):   # function for inserting the data into the data representation window
    global averages
    with open(initials + '_averages.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            averages = row
    print(averages)
    datarpr.pushButton_lk.setText(averages[0] + "%")
    datarpr.pushButton_lr.setText(averages[1] + "%")
    datarpr.pushButton_lm.setText(averages[2] + "%")
    datarpr.pushButton_lz.setText(averages[3] + "%")
    datarpr.pushButton_rz.setText(averages[4] + "%")
    datarpr.pushButton_rm.setText(averages[5] + "%")
    datarpr.pushButton_rr.setText(averages[6] + "%")
    datarpr.pushButton_rk.setText(averages[7] + "%")
    set_graphics_view(window.datarepr_window.scene)


class WindowCreator:
    def __init__(self):
        self.w = QtWidgets.QStackedWidget()
        self.main_window = UiWindows.MainWindow()
        self.ard_not_found_window = UiWindows.ArdNotFound()
        self.initials_window = UiWindows.Initials()
        self.measurement_window = UiWindows.Measurement(app)
        self.between_window = UiWindows.Between()
        self.datarepr_window = UiWindows.DataRepr()
        self.results_window = UiWindows.Results()
        self.w.addWidget(self.main_window)
        self.w.addWidget(self.ard_not_found_window)
        self.w.addWidget(self.initials_window)
        self.w.addWidget(self.measurement_window)
        self.w.addWidget(self.between_window)
        self.w.addWidget(self.datarepr_window)
        self.w.addWidget(self.results_window)
        self.w.resize(1280, 800)
        self.push_button_connect()
        self.w.show()
        self.w.setWindowTitle("ClimbDoc")
        if arduino_not_found:
            self.w.setCurrentIndex(1)

    def push_button_connect(self):
        self.main_window.pushButton_2.clicked.connect(measure_once_start)
        self.main_window.pushButton_3.clicked.connect(lambda: self.w.setCurrentIndex(2))
        self.main_window.pushButton_4.clicked.connect(lambda: self.w.setCurrentIndex(2))
        self.main_window.pushButton.clicked.connect(lambda: sys.exit(app.exec_()))
        self.datarepr_window.pushButton.clicked.connect(lambda: self.w.setCurrentIndex(6))
        self.results_window.pushButton.clicked.connect(lambda: self.w.setCurrentIndex(0))


window = WindowCreator()

sys.exit(app.exec_())
