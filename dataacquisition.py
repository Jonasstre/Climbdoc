import time
import serial
import csv
import os

data = {}                                                                   # creates global variables
averages = []
newdata = [[1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0]]

anf = False
com_port = "COM4"                                                           # saves the serial port


def data_recording():
    global anf
    try:                                # tries to connect the serial port is available
        serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    except serial.serialutil.SerialException:
        print("Arduino not Found")
        anf = True
    if not anf:
        ot = time.time()                                    # saves the time at the beginning of recording
        while 1:
            if serialPort.in_waiting > 0:
                serialString = serialPort.readline().decode('Ascii', 'ignore').strip()
                serial_input = serialString.split(",")                  # reads the serial port
                if len(serial_input) < 9:
                    for i in range(0, 9-len(serial_input)):
                        serial_input.append("0.0")                      # fills up the array, if no data was found
                data[time.time()] = ",".join(serial_input)
                if time.time() - ot > 12:                               # stops recording after 12 seconds
                    break
        serialPort.close()                                              # closes the serial port


def data_writing(initials):
    with open(os.path.join(os.path.dirname(__file__), initials+'.csv'), 'w', newline='') as file:
        data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in data.keys():
            row = [key]
            row.extend(data[key])
            data_writer.writerow(row)                   # writes the recorded data to a csv file


def data_processing(initials):                                                    # function for processing the raw data
    global newdata
    averages.clear()
    newdata = [[1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0]]
    with open(os.path.join(os.path.dirname(__file__), initials+'.csv'), 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            for i in range(0, 9):
                try:
                    print(row)
                    newdata[i].append(float(row[i]))
                except ValueError:
                    newdata[i].append(0.0)
                    continue                        # adds all data to a matrix
                                                    # if empty strings are detected inserts a 0
    for i in range(0, 9):
        newdata[i] = newdata[i][1:-5]               # cuts the first and last values of

    averagestot = []
    for i in range(1, 9):                           # calculates the averages for the data
        average = sum(newdata[i]) / len(newdata[i])
        averagestot.append(average)
    tot = sum(averagestot)
    for average in averagestot:                     # if the average is 0, appends 0
        if average == 0.0:
            averages.append(average)
        else:                                       # if the average is not zero, converts to percentage
            averages.append(round(((average/tot)*100), 2))

    with open(os.path.join(os.path.dirname(__file__), initials+"_averages"+'.csv'), 'w', newline='') as file:
        data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(averages)              # writes the averages to a csv file

    return newdata                                  # returns the data

