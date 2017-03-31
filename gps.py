# -*- coding:utf-8 -*-
import sys
import time
import serial
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer

qtCreatorFile = "gps.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
ser = serial.Serial('/dev/ttyUSB0',9600)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    mode = 0  # 0显示开始采集，1显示停止采集
    interval = 1.0  # 采集间隔
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.startButton.clicked.connect(self.timerControl)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.collection)
        self.clearButton.clicked.connect(self.removeFile)
        #self.mapButton1.clicked.connect(self.map)
        self.intervalValue.valueChanged.connect(self.changeInterval)
        self.pointButton1.clicked.connect(self.getPoint1)
        self.pointButton2.clicked.connect(self.getPoint2)
        #self.mapButton2.clicked.connect(self.map)

    def writedata(self, gps_str):
        file_write_object = open('GPS.txt', 'a')
        content_list = gps_str.split('\n')
        record_list = []
        for content_line in content_list:
            if content_line[0:6] == "$GNRMC" and len(content_line) >18 and content_line[17:18] == 'A':
                split_line = content_line.split(',')
                if len(split_line) > 9:
                    gpstime = split_line[1]
                    lat = split_line[3]
                    lng = split_line[5]
                    date = split_line[9]

                    # 时间
                    hour = gpstime[0:2]
                    minute = gpstime[2:4]
                    second = gpstime[4:6]
                    time_str = hour + ':' + minute + ':' + second

                    # 经纬度
                    lat_degree = lat[0:2]
                    lat_minute = float(lat[2:]) / 60

                    lng_degree = lng[0:3]
                    lng_minute = float(lng[3:]) / 60

                    lat_str = str(float(lat_degree) + lat_minute)
                    lng_str = str(float(lng_degree) + lng_minute)

                    # 其他要素
                    speed = str(float(split_line[7]) * 1.852)  # 已转换为公里每小时
                    if split_line[8] != '':
                        direction = split_line[8]
                    else:
                        direction = '-255.0'
                    day = date[0:2]
                    month = date[2:4]
                    year = '20' + date[4:6]
                    date_str = year + '-' + month + '-' + day

                    # 生成记录并写文件
                    # 格式：经度，纬度，速度，方向，时间，日期
                    record_string = lng_str + ',' + lat_str + ',' + speed + ',' + direction + ',' + time_str + ',' + date_str + '\n'
                    record_list.append(record_string)
        if len(record_list) > 0:
            file_write_object.writelines(record_list[-1])
        file_write_object.close()

    def timerControl(self):
        if self.mode == 0:
            self.mode = 1
            self.startButton.setText('停止采集')
            self.timer.start(self.interval*1000)
        else:
            self.mode = 0
            dropdata = ser.read(ser.inWaiting())
            self.startButton.setText('开始采集')
            self.timer.stop()
                     
    def collection(self):
        gps_str = ser.read(ser.inWaiting())
        print gps_str
        self.writedata(gps_str)
        
    def changeInterval(self):
        self.interval = self.intervalValue.value()

    def removeFile(self):
        if os.path.exists('GPS.txt'):
            os.remove('GPS.txt')

    def recordPoint(self, gps_str, tagtext):
        file_write_object = open('Point.txt', 'a')
        content_list = gps_str.split('\n')
        record_list = []
        for content_line in content_list:
            if content_line[0:6] == "$GNRMC" and len(content_line) >18 and content_line[17:18] == 'A':
                split_line = content_line.split(',')
                if len(split_line) > 9:
                    gpstime = split_line[1]
                    lat = split_line[3]
                    lng = split_line[5]
                    date = split_line[9]

                    # 时间
                    hour = gpstime[0:2]
                    minute = gpstime[2:4]
                    second = gpstime[4:6]
                    time_str = hour + ':' + minute + ':' + second

                    # 经纬度
                    lat_degree = lat[0:2]
                    lat_minute = float(lat[2:]) / 60

                    lng_degree = lng[0:3]
                    lng_minute = float(lng[3:]) / 60

                    lat_str = str(float(lat_degree) + lat_minute)
                    lng_str = str(float(lng_degree) + lng_minute)

                    # 其他要素
                    speed = str(float(split_line[7]) * 1.852)  # 已转换为公里每小时
                    if split_line[8] != '':
                        direction = split_line[8]
                    else:
                        direction = '-255.0'
                    day = date[0:2]
                    month = date[2:4]
                    year = '20' + date[4:6]
                    date_str = year + '-' + month + '-' + day

                    # 生成记录并写文件
                    # 格式：经度，纬度，速度，方向，时间，日期
                    record_string = lng_str + ',' + lat_str + ',' + speed + ',' + direction + ',' + time_str + ',' + date_str + ',' + tagtext + '\n'
                    record_list.append(record_string)
        if len(record_list) > 0:
            file_write_object.writelines(record_list[-1])
        file_write_object.close()

    def getPoint1(self):
        gps_str = ser.read(ser.inWaiting())
        tagtext = '我只是个萌萌的栗子'
        self.recordPoint(gps_str, tagtext)

    def getPoint2(self):
        gps_str = ser.read(ser.inWaiting())
        tagtext = '酱油采集处'
        self.recordPoint(gps_str, tagtext)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
