# link solution: https://stackoverflow.com/questions/55842776/how-to-change-ui-in-same-window-using-pyqt5


import csv                                                                      # imports the necessary packages
import os
from qtpy import QtCore, QtGui, QtWidgets, uic
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import serial
import time
import threading
import dataacquisition
import UiWindows

arduino_not_found = False                                  # creates arduinonotfound variable, sets it to false

serialString = ""                                           # creates empty string

com_port = "/dev/ttyACM0"                                   # sets the variable for the port the arduino is connected to
dataacquisition.com_port = com_port                         # sets the com_port variable in the dataacquisition file
try:                                                        # tries to connect to the arduino
    serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
except serial.serialutil.SerialException:                   # catches exception for when no arduino is found
    print("Arduino not Found")
    arduino_not_found = True


app = QtWidgets.QApplication(sys.argv)                      # initialises a QApplication using sys


def set_graphics_view(scene, newdata):                      # function for creating a graph out of the recorded data for
    figure = Figure()                                       # the datarpr window
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
    canvas.resize(1170, 515)
    proxy_widget = scene.addWidget(canvas)


def measure(initials):                          # framework function for measuring
    wait_for_load()

    window.w.setCurrentIndex(3)

    if __name__ == "__main__":                      # uses threading to run the ui and data recording concurrently
        x = threading.Thread(target=dataacquisition.data_recording)
        y = threading.Thread(target=window.measurement_window.countdown)
        x.start()
        y.start()
        x.join()
    dataacquisition.data_writing(initials)
    newdata = dataacquisition.data_processing(initials)
    time.sleep(2)                                                   # waits for data processing to finish
    return newdata


def wait_for_load():                                                # function that holds the program until all sensors
    no_zero = False                                                 # output a value greater than 0
    read = []
    while not no_zero:                                              # loop runs until all values /= 0
        if serialPort.in_waiting > 0:
            readstrings = serialPort.readline().decode('Ascii', 'ignore').strip().split(",")    # reads the serialport
            for element in readstrings:                                                         # and adds it to a list
                try:
                    read.append(float(element))
                except ValueError:
                    read.append(0.0)
                    continue
        read = read[:-1]
        if not read:                                                                # skips loop if read list is empty
            continue
        for i in range(0, 8):                                                       # iterates through read list and
            if read[i] != 0.0:                                                      # outputs wether or not there's a 0
                no_zero = True
            if read[i] == 0.0:
                no_zero = False
                break
        read.clear()                                                                # empties read list
    serialPort.close()                                                              # closes the serial port


def prep_results(initials):                                                 # function for preparing the results window
    performance = []
    signal = [                                                              # adds all signals on results window to list
        window.results_window.label_1,
        window.results_window.label_2,
        window.results_window.label_3,
        window.results_window.label_4,
        window.results_window.label_5,
        window.results_window.label_6,
        window.results_window.label_7,
        window.results_window.label_8
    ]
    with open(os.path.join(os.path.dirname(__file__), initials + '_reference_averages.csv'), 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            averages_reference = row
    with open(os.path.join(os.path.dirname(__file__),initials + '_averages.csv'), 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            averages = row                   # reads both the averages and the reference averages and adds them to lists
    for i in range(0, 8):                   # loop that assigns performance values to each finger
        if float(averages_reference[i]) - float(averages_reference[i]) * 0.1 < float(averages[i]) \
                < float(averages_reference[i]) + float(averages_reference[i]) * 0.1:
            performance.append(0)
        elif float(averages_reference[i]) - float(averages_reference[i]) * 0.2 < float(averages[i]) \
                < float(averages_reference[i]) + float(averages_reference[i]) * 0.2:
            performance.append(1)
        else:
            performance.append(2)
    for i in range(0, 8):                           # loop that colors the signals based on the performances
        if performance[i] == 0:
            signal[i].setStyleSheet("background-color: green")
        elif performance[i] == 1:
            signal[i].setStyleSheet("background-color: yellow")
        elif performance[i] == 2:
            signal[i].setStyleSheet("background-color: red")


def measure_once_start():           # function linked to the measure once button in the main menu
    window.w.setCurrentIndex(4)
    app.processEvents()             # forces the application to wait for the window switch
    newdata = measure("No_initials")            # executes the measurement files with no initials and saves the result
    prep_data_repr(window.datarepr_window, "No_initials", newdata)      # as newdata
    prep_results("No_initials")
    window.datarepr_window.pushButton.clicked.connect(lambda: window.w.setCurrentIndex(6))
    window.w.setCurrentIndex(5)
    serialPort.open()                                       # opens the serial port
    os.remove(os.path.join(os.path.dirname(__file__), "No_initials.csv"))                   # removes the csv files
    os.remove(os.path.join(os.path.dirname(__file__), "No_initials_averages.csv"))


def check_if_free():                              # function for checking if there is a csv file with the given initials
    initials = window.initials_window.textEdit.toPlainText()       # extracts the text from the initials textEdit
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
    # checks if textEdit is empty and wether or not the initials are already in use


def check_if_exists():                            # function for checking if there is data for the given initials
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


def measure_twice_two(initials):          # function for the second measurement of the double measurement functionality
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
    os.remove(os.path.join(os.path.dirname(__file__), initials + "_reference.csv"))
    os.remove(os.path.join(os.path.dirname(__file__), initials + "_reference_averages.csv"))
    os.remove(os.path.join(os.path.dirname(__file__), initials + ".csv"))
    os.remove(os.path.join(os.path.dirname(__file__), initials + "_averages.csv"))


def measure_twice_two_start():                  # function linked to the second measurement button in the main menu
    window.w.setCurrentIndex(2)
    window.initials_window.pushButton.clicked.connect(check_if_exists)


def measure_twice_one(initials):            # function for the first measurement of the double measurement functionality
    window.w.setCurrentIndex(4)
    app.processEvents()
    newdata = measure(initials)
    prep_data_repr(window.datarepr_window, initials, newdata)
    window.datarepr_window.pushButton.clicked.connect(lambda: window.w.setCurrentIndex(0))
    window.w.setCurrentIndex(5)
    serialPort.open()
    window.initials_window.label_2.setVisible(False)
    window.initials_window.textEdit.clear()


def measure_twice_one_start():              # function linked to the second measuremet button in the main menu
    window.w.setCurrentIndex(2)
    window.initials_window.pushButton.clicked.connect(check_if_free)


def prep_data_repr(datarpr, initials, newdata):   # function for inserting the data into the data representation window
    with open(os.path.join(os.path.dirname(__file__), initials + '_averages.csv'), 'r', newline='') as file:
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


def return_to_menu():                           # linked to the menu button in the initials window
    window.initials_window.label_2.setVisible(False)
    window.initials_window.textEdit.clear()
    window.w.setCurrentIndex(0)


class WindowCreator:                                # class that sets up the ui
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
        if arduino_not_found:                       # sets the window to arduino not found if no arduino is found
            self.w.setCurrentIndex(1)

    def push_button_connect(self):                  # connects the buttons to their functions
        self.main_window.pushButton_2.clicked.connect(measure_once_start)
        self.main_window.pushButton_3.clicked.connect(measure_twice_one_start)
        self.main_window.pushButton_4.clicked.connect(measure_twice_two_start)
        self.main_window.pushButton.clicked.connect(lambda: sys.exit(app.exec_()))
        self.initials_window.pushButton_2.clicked.connect(return_to_menu)
        self.datarepr_window.pushButton.clicked.connect(lambda: self.w.setCurrentIndex(6))
        self.results_window.pushButton.clicked.connect(lambda: self.w.setCurrentIndex(0))


window = WindowCreator()                        # creates window object

sys.exit(app.exec_())                           # closes QApplication
