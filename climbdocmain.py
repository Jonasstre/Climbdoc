# link solution: https://stackoverflow.com/questions/55842776/how-to-change-ui-in-same-window-using-pyqt5
import csv
import os
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
# data = {}
# averages = []
# newdata = []

# if arduino_not_found:
#     state = "anfError"

app = QtWidgets.QApplication(sys.argv)


def set_graphics_view(scene, newdata):
    figure = Figure()
    axes = figure.gca()
    axes.set_title("Finger forces")
    seconds = []
    for element in newdata[0]:
        seconds.append(round((element - newdata[0][0]), 3))
    x = seconds
    y = []
    for i in range(1, 9):
        y.append(newdata[i])
    axes.plot(x, y[0], "-b")
    axes.plot(x, y[1], "-k")
    axes.plot(x, y[2], "-g")
    axes.plot(x, y[3], "-r")
    axes.plot(x, y[4], "-c")
    axes.plot(x, y[5], "-m")
    axes.plot(x, y[6], "-y")
    axes.plot(x, y[7], "-k")
    axes.legend()
    axes.grid(True)

    canvas = FigureCanvas(figure)
    canvas.resize(1170, 540)
    proxy_widget = scene.addWidget(canvas)


def measure(initials):
    wait_for_load()

    window.w.setCurrentIndex(3)

    if __name__ == "__main__":
        x = threading.Thread(target=dataacquisition.data_recording)
        y = threading.Thread(target=window.measurement_window.countdown)
        y.start()
        x.start()
        x.join()
    dataacquisition.data_writing(initials)
    newdata = dataacquisition.data_processing(initials)
    time.sleep(2)
    print("I'm done!")
    return newdata


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


def prep_results(initials):
    performance = []
    signal = [
        window.results_window.label_1,
        window.results_window.label_2,
        window.results_window.label_3,
        window.results_window.label_4,
        window.results_window.label_5,
        window.results_window.label_6,
        window.results_window.label_7,
        window.results_window.label_8
    ]
    with open(initials + '_reference_averages.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            averages_reference = row
    with open(initials + '_averages.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            averages = row
    for i in range(0, 8):
        if float(averages_reference[i]) - float(averages_reference[i]) * 0.1 < float(averages[i]) \
                < float(averages_reference[i]) + float(averages_reference[i]) * 0.1:
            performance.append(0)
        elif float(averages_reference[i]) - float(averages_reference[i]) * 0.2 < float(averages[i]) \
                < float(averages_reference[i]) + float(averages_reference[i]) * 0.2:
            performance.append(1)
        else:
            performance.append(2)
    for i in range(0, 8):
        if performance[i] == 0:
            signal[i].setStyleSheet("background-color: green")
        elif performance[i] == 1:
            signal[i].setStyleSheet("background-color: yellow")
        elif performance[i] == 2:
            signal[i].setStyleSheet("background-color: red")


def measure_once_start():           #function linked to the measure once button in the main menu
    window.w.setCurrentIndex(4)
    app.processEvents()
    newdata = measure("No_initials")
    prep_data_repr(window.datarepr_window, "No_initials", newdata)
    prep_results("No_initials")
    window.datarepr_window.pushButton.clicked.connect(lambda: window.w.setCurrentIndex(6))
    window.w.setCurrentIndex(5)
    serialPort.open()


def check_if_free():
    initials = window.initials_window.textEdit.toPlainText()
    if initials != '' and initials + "_reference.csv" not in os.listdir(os.path.dirname(__file__)):
        measure_twice_one(initials + "_reference")
    elif initials == '':
        window.initials_window.label_2.setText("Please enter initials!")
        window.initials_window.label_2.setVisible(True)
    elif initials + "_reference.csv" in os.listdir(os.path.dirname(__file__)):
        window.initials_window.label_2.setText(
            "Initials already taken! Please add another identifier! (For example a number)"
        )
        window.initials_window.label_2.setVisible(True)


def check_if_exists():
    initials = window.initials_window.textEdit.toPlainText()
    if initials != '' and initials + "_reference.csv" in os.listdir(os.path.dirname(__file__)):
        measure_twice_two(initials)
    elif initials == '':
        window.initials_window.label_2.setText("Please enter initials!")
        window.initials_window.label_2.setVisible(True)
    elif initials + "_reference.csv" not in os.listdir(os.path.dirname(__file__)):
        window.initials_window.label_2.setText(
            "No data found! Please try different initials!"
        )
        window.initials_window.label_2.setVisible(True)


def measure_twice_two(initials):
    window.w.setCurrentIndex(4)
    app.processEvents()
    newdata = measure(initials)
    prep_data_repr(window.datarepr_window, initials, newdata)
    prep_results(initials)
    window.datarepr_window.pushButton.clicked.connect(lambda: window.w.setCurrentIndex(6))
    window.w.setCurrentIndex(5)
    serialPort.open()
    window.initials_window.label_2.setVisible(False)
    window.initials_window.textEdit.clear()


def measure_twice_two_start():
    window.w.setCurrentIndex(2)
    window.initials_window.pushButton.clicked.connect(check_if_exists)


def measure_twice_one(initials):
    window.w.setCurrentIndex(4)
    app.processEvents()
    newdata = measure(initials)
    prep_data_repr(window.datarepr_window, initials, newdata)
    window.datarepr_window.pushButton.clicked.connect(lambda: window.w.setCurrentIndex(0))
    window.w.setCurrentIndex(5)
    serialPort.open()
    window.initials_window.label_2.setVisible(False)
    window.initials_window.textEdit.clear()


def measure_twice_one_start():
    window.w.setCurrentIndex(2)
    window.initials_window.pushButton.clicked.connect(check_if_free)


def prep_data_repr(datarpr, initials, newdata):   # function for inserting the data into the data representation window
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
    set_graphics_view(datarpr.scene, newdata)


# def datarep_test():     # function for testing the data representatin window
#     global newdata
#     newdata = dataacquisition.data_processing()
#     prep_data_repr(window.datarepr_window)
#     window.w.setCurrentIndex(5)


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
        self.main_window.pushButton_3.clicked.connect(measure_twice_one_start)
        self.main_window.pushButton_4.clicked.connect(measure_twice_two_start)
        self.main_window.pushButton.clicked.connect(lambda: sys.exit(app.exec_()))
        self.datarepr_window.pushButton.clicked.connect(lambda: self.w.setCurrentIndex(6))
        self.results_window.pushButton.clicked.connect(lambda: self.w.setCurrentIndex(0))


window = WindowCreator()

sys.exit(app.exec_())
