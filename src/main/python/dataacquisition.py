import time
import serial
import csv

data = {}
averages = []
newdata = [[1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0]]

anf = False
com_port = "COM4"


def data_recording():
    global anf
    try:
        serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    except serial.serialutil.SerialException:
        print("Arduino not Found")
        anf = True
    if not anf:
        ot = time.time()
        while 1:
            if serialPort.in_waiting > 0:
                serialString = serialPort.readline().decode('Ascii')
                data[time.time()] = serialString.split(",")

                if time.time() - ot > 12:
                    break
        serialPort.close()


def data_writing(initials):
    with open(initials+'.csv', 'w', newline='') as file:
        data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in data.keys():
            row = [key]
            row.extend(data[key])
            data_writer.writerow(row)


def data_processing(initials):                                                    # function for processing the raw data
    global newdata
    averages.clear()
    newdata = [[1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0]]
    with open(initials+'.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            for i in range(0, 9):
                newdata[i].append(float(row[i]))

    for i in range(0, 9):
        newdata[i] = newdata[i][1:-5]

    averagestot = []
    for i in range(1, 9):
        average = sum(newdata[i]) / len(newdata[i])
        averagestot.append(average)
    tot = sum(averagestot)
    for average in averagestot:
        if average == 0.0:
            averages.append(average)
        else:
            averages.append(round(((average/tot)*100), 2))

    with open(initials+"_averages"+'.csv', 'w', newline='') as file:
        data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(averages)

    return newdata



#data_acquisition()
