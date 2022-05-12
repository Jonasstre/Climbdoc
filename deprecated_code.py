# dataacquistion:
#  data processing:
# placeholder for code determining the beginning and end of used values
    # beg = 0
    # end = len(newdata[0]) - 1   # e: end of used values
    # begsecs = 0
    # for i in range(1, len(newdata[0])):
    #     if float(newdata[0][i]) - float(newdata[0][1]) > 1:
    #         beg = i                       # b: beginning of used values
    #         begsecs = float(newdata[0][i])      # begsecs safes the seconds at the beginning
    #         break
    # for i in range(beg, len(newdata[0])):
    #     if float(newdata[0][i]) - begsecs > 10:
    #         end = i
    #         break

# for i in range(1, 8):
    #     nums = [[], [], [], [], [], [], [], []]
    #     for num in newdata[i]:
    #         nums[i-1].append(float(num))
    #     print(nums)

# climbdocmain:
#  old window init:
# w = QtWidgets.QStackedWidget()
# main_window = UiWindows.MainWindow(w)
# ard_not_found_window = UiWindows.ArdNotFound()
# initials_window = UiWindows.Initials()
# measurement_window = UiWindows.Measurement()
# w.addWidget(main_window)
# w.addWidget(ard_not_found_window)
# w.addWidget(initials_window)
# w.addWidget(measurement_window)
# w.resize(1280, 800)

#  old data_acquistion
# def data_aquisition():
#     data_recording()
#     data_writing()
#     data_processing()
#
#
# def data_recording():
#     global state
#     ot = time.time()
#     while state == "recording":
#         if serialPort.in_waiting > 0:
#             serialString = serialPort.readline().decode('Ascii')
#             data[time.time()] = serialString.split(",")
#
#             if time.time() - ot > 10:
#                 state = "writing"
#
#
# def data_writing():
#     with open(initials+'.csv', 'w', newline='') as file:
#         data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         for key in data.keys():
#             row = [key]
#             row.extend(data[key])
#             data_writer.writerow(row)
#
#
# def data_processing():                                                            # function for processing the raw data
#
#     newdata = [["timestamp"], ["f1"], ["f2"], ["f3"], ["f4"], ["f5"], ["f6"], ["f7"], ["f8"]]
#     with open(initials+'.csv', 'r', newline='') as file:
#         reader = csv.reader(file, delimiter=',', quotechar='"')
#         for row in reader:
#             for i in range(0, 9):
#                 newdata[i].append(row[i])
#     # placeholder for code determining the beginning and end of used values
#     beg = 0
#     end = len(newdata[0]) - 1   # e: end of used values
#     begsecs = 0
#     for i in range(1, len(newdata[0])):
#         if float(newdata[0][i]) - float(newdata[0][1]) > 1:
#             beg = i                       # b: beginning of used values
#             begsecs = float(newdata[0][i])      # begsecs safes the seconds at the beginning
#             break
#     for i in range(beg, len(newdata[0])):
#         if float(newdata[0][i]) - begsecs > 10:
#             end = i
#             break
#
#     for i in range(0, 9):
#         newdata[i] = newdata[i][1:]
#
#     for i in range(1, 8):
#         nums = [[], [], [], [], [], [], [], []]
#         for num in newdata[i]:
#             nums[i-1].append(float(num))
#         average = sum(nums[i]) / len(newdata[i])
#         averages.append(average)
#
#     print(averages)

#  old dataacquistion call:

# file_globals = runpy.run_path("dataacquisition.py")
    # exec(compile(open('dataacquisition.py').read(), dataacquisition.py, 'exec'))
    # os.system('python dataacquisition.py')
    # run_in_parallel(dataacquisition.data_acquisition, window.measurement_window.countdown)

#  multiprocessing parallel functions:
# def run_in_parallel(*fns):
#     proc = []
#     for fn in fns:
#         p = Process(target=fn)
#         p.start()
#         proc.append(p)
#     for p in proc:
#         p.join()