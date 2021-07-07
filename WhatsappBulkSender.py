try:

    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QFileDialog
    import pandas
    import re
    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtWidgets import *
    from PyQt5 import QtCore, QtGui, QtWidgets
    import traceback
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.options import Options
    from urllib.parse import quote
    from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
    from time import sleep
    from itertools import cycle, islice
    import time
    import datetime
    import os
    import argparse
    import platform
    import pandas as pd
    import re
    import threading
    import random
    from itertools import chain
    import shutil
    import os
    import sys
    import uuid
    # from bot_function import *

    # For Api calls Begins
    from itertools import chain
    from datetime import datetime
    import requests
    import socket
    import json

    # base_url = "http://127.0.0.1:8000/"
    # base_url = "http://minerv100.herokuapp.com/"
    #base_url = 'http://165.232.178.222/'
    base_url = "http://botslicense.pythonanywhere.com/"


    def getIpAddress():
        # hostname = socket.gethostname()
        # ip_address = socket.gethostbyname(hostname)
        ip_address = str(hex(uuid.getnode()))
        return ip_address


    def check_ip_auth(token, api):
        if api == 'whatsapp':
            url = base_url + 'IpAPI/whatsapp'
        if api == 'telegram':
            url = base_url + 'IpAPI/telegram'
        if api == 'instagram':
            url = base_url + 'IpAPI/instagram'
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers)
        local_ip = getIpAddress()
        data = list(chain.from_iterable(response.json()))
        print(data)
        if local_ip in data:
            return False
        else:
            return True


    def createIp(token, api):
        local_ip_address = getIpAddress()
        if api == 'whatsapp':
            url = base_url + 'createIP/whatsapp'
        if api == 'telegram':
            url = base_url + 'createIP/telegram'
        if api == 'instagram':
            url = base_url + 'createIP/instagram'
        x = {'ip_address': local_ip_address}
        payload = json.dumps(x)
        headers = {'Authorization': f'Token {token}',
                'Content-Type': 'application/json'}
        requests.request("PUT", url, headers=headers, data=payload)


    def get_today(token):
        url = base_url + 'serverDateAPI/'
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", url)
        data = response.json()
        today = datetime.strptime(data, '%Y-%m-%d').date()
        return today


    def isPaidStatus(token,api):
        url = base_url + f'isPaidStatus/{api}'
        headers = {'Authorization': f'Token {token}','Content-Type': 'application/json'}
        response = requests.request("PUT", url, headers=headers)


    def auth(token, api):
        if api == 'whatsapp':
            url = base_url + 'whatsappAPI/'
        if api == 'telegram':
            url = base_url + 'telegramAPI/'
        if api == 'instagram':
            url = base_url + 'instagramAPI/'

        headers = {'Authorization': f'Token {token}',
                'Content-Type': 'application/json'}
        today = get_today(token)

        response = requests.request("GET", url, headers=headers)
        # print(response.json())
        if response.status_code == 200:
            local_ip_address = getIpAddress()
            json_data = response.json()
            remote_ip_address = json_data['ip_address']
            print('remote_ip_address', remote_ip_address,
                'local_ip_address', local_ip_address)
            if remote_ip_address == None:
                check_ip_response = check_ip_auth(token, api)
                if check_ip_response:
                    createIp(token, api)
                else:
                    print(
                        "Your Ip is already associate with other account Please check your account")
                    return False, 'Your Ip is already associate with other account Please check your account'

            if json_data['isActive']:
                demo_date = datetime.strptime(
                    json_data['DemoDate'], '%Y-%m-%d').date()
                license_expire_date = json_data['licenceExpireDate']
                print(type(today), type(demo_date), type(license_expire_date))
                print("today", today)
                print('demo_date', demo_date)
                print('license_expire_date', license_expire_date,
                    type(license_expire_date))
                if license_expire_date != None:
                    license_expire_date = datetime.strptime(
                        license_expire_date, '%Y-%m-%d').date()
                    print('license_expire_date', license_expire_date)
                    if(license_expire_date >= today):
                        print("allow with license")
                        return True, f'License valid till {license_expire_date}'
                    else:
                        isPaidStatus(token,api)
                        print("Not allowed your License expired")
                        return False, 'Not allowed your License expired'

                elif (demo_date == today):
                    print("allow for demo")
                    return True, f'License valid till {demo_date}'
                else:
                    print('Not allowed Please Activate your account by paying')
                    return False, 'Not allowed Please Activate your account by paying'
            else:
                print("Not allowed your account is deactive")
                return False, 'Not allowed your account is deactive'

        else:
            print('Invalid Token')
            return False, 'Invalid Token'


    def getVariable(api):
        url = base_url + f"variableAPI/{api}"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers)
        data = list(chain.from_iterable(response.json()))
        variable = data[0].split("\n")
        # print(variable)
        return variable


    # API ENDS



    total = []
    value_msg = ''
    bhejna = False
    unique = ""
    message = ""
    chrome_path = "D:\drivers\chromedriver.exe"

    # delay = 15
    #
    # # clipbtn='//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span'
    # clipbtn = '//div[@title = "Attach"]'
    # # media_send_btn='//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span'
    # media_send_btn = '//span[@data-icon="send"]'
    # # file_send_btn='//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'
    # file_send_btn = '//span[@data-icon="send"]'
    # search_boxji = "_2MwRD"
    # main_search_box = "_2_1wd"
    # group_member_extractor = "YmixP"
    # input_media = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
    # input_files = '//input[@accept="*"]'
    # main_send_button = '_1E0Oz'

    # CALL THE API VARIABLE
    variable = getVariable('whatsapp')
    print(variable)
    # clipbtn='//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span'
    # clipbtn='//div[@title = "Attach"]'
    clipbtn = variable[0].strip()

    # media_send_btn='//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span'
    # media_send_btn='//span[@data-icon="send"]'
    media_send_btn = variable[1].strip()

    # file_send_btn='//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'
    # file_send_btn='//span[@data-icon="send"]'
    file_send_btn = variable[2].strip()
    # search_boxji="_2MwRD"
    search_boxji = variable[3].strip()

    # main_search_box="_2_1wd"
    main_search_box = variable[4].strip()

    # group_member_extractor="YmixP"
    group_member_extractor = variable[5].strip()

    # input_media='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
    input_media = variable[6].strip()
    # input_files='//input[@accept="*"]'
    input_files = variable[7].strip()

    # main_send_button='_1E0Oz'
    main_send_button = variable[8].strip()

    delay = int(variable[9])

    class whatsapp_popup0(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(891, 301)
            MainWindow.setMaximumSize(QtCore.QSize(891, 301))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot1.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            MainWindow.setFont(font)
            MainWindow.setStyleSheet("background-color:white;")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(70, 110, 201, 71))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.token_input = QtWidgets.QLineEdit(self.centralwidget)
            self.token_input.setGeometry(QtCore.QRect(310, 130, 551, 31))
            self.token_input.setObjectName("token_input")
            self.token_click = QtWidgets.QPushButton(self.centralwidget)
            self.token_click.setGeometry(QtCore.QRect(240, 200, 121, 41))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.token_click.setFont(font)
            self.token_click.setStyleSheet("color:white;\n"
                                           "background-color: blue;\n"
                                           "")
            self.token_click.setObjectName("token_click")
            self.token_show = QtWidgets.QLabel(self.centralwidget)
            self.token_show.setGeometry(QtCore.QRect(5, 39, 760, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.token_show.setFont(font)
            self.token_show.setStyleSheet("color:red")
            self.token_show.setText("")
            self.token_show.setObjectName("token_show")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 891, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate(
                "MainWindow", "WhatsApp Bulk Sender"))
            self.label.setText(_translate("MainWindow", "Enter the Token Id"))
            self.token_click.setText(_translate("MainWindow", "Submit"))

    class Token_page(QtWidgets.QMainWindow, whatsapp_popup0):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.token_show.setText(message)
            self.token_click.clicked.connect(self.main_page)

        def main_page(self):
            # Anish Write your code
            global message
            token = self.token_input.text()
            print(token)
            path = os.path.join("C:\\", "Token")
            with open(path+'/token.txt', 'w') as f:
                f.write(token)
                f.close()
            cond, mess = auth(token, 'whatsapp')
            if cond:
                print("everything works", mess)
                message = mess
                print("#####", message)
                self.z = MainWindow()
                self.z.show()
                self.hide()
            # sys.exit(app.exec_())
            else:
                print(f'here i am')
                message = mess
                self.token_show.setText(message)

                # message = mess
                # w = Token_page()
                # w.show()
                # w.hide()
                # w.show()
                # sys.exit(app.exec_())

    class whatsapp_popup2(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(540, 627)
            MainWindow.setMinimumSize(QtCore.QSize(540, 627))
            MainWindow.setMaximumSize(QtCore.QSize(540, 627))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot1.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            MainWindow.setStyleSheet("background-color:white;")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(100, 10, 381, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.r1 = QtWidgets.QRadioButton(self.centralwidget)
            self.r1.setGeometry(QtCore.QRect(70, 70, 401, 20))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.r1.setFont(font)
            self.r1.setObjectName("r1")
            self.r2 = QtWidgets.QRadioButton(self.centralwidget)
            self.r2.setGeometry(QtCore.QRect(70, 110, 421, 31))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(False)
            font.setWeight(50)
            self.r2.setFont(font)
            self.r2.setObjectName("r2")
            self.com1 = QtWidgets.QComboBox(self.centralwidget)
            self.com1.setGeometry(QtCore.QRect(110, 170, 301, 22))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.com1.setFont(font)
            self.com1.setObjectName("com1")
            self.r3 = QtWidgets.QRadioButton(self.centralwidget)
            self.r3.setGeometry(QtCore.QRect(70, 230, 421, 20))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.r3.setFont(font)
            self.r3.setObjectName("r3")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(70, 450, 161, 16))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.label_2.setFont(font)
            self.label_2.setObjectName("label_2")
            self.switch_2 = QtWidgets.QSpinBox(self.centralwidget)
            self.switch_2.setGeometry(QtCore.QRect(240, 450, 121, 22))
            self.switch_2.setMaximum(1000)
            self.switch_2.setObjectName("switch_2")
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            self.label_3.setGeometry(QtCore.QRect(380, 450, 81, 21))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.label_3.setFont(font)
            self.label_3.setObjectName("label_3")
            self.f_send = QtWidgets.QPushButton(self.centralwidget)
            self.f_send.setGeometry(QtCore.QRect(182, 507, 121, 51))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.f_send.setFont(font)
            self.f_send.setStyleSheet("color:white;\n"
                                      "background-color:#25D366")
            self.f_send.setObjectName("f_send")
            self.all_account = QtWidgets.QTextEdit(self.centralwidget)
            self.all_account.setGeometry(QtCore.QRect(80, 270, 321, 151))
            self.all_account.setObjectName("all_account")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label.setText(_translate(
                "MainWindow", "What you want to do ?"))
            self.r1.setText(_translate(
                "MainWindow", "Send from new fresh session (Require Login)"))
            self.r2.setText(_translate(
                "MainWindow", "Send from saved accounts (Do not Require Login)"))
            self.r3.setText(_translate(
                "MainWindow", "Rotate between accounts"))
            self.label_2.setText(_translate(
                "MainWindow", "Switch Account after"))
            self.label_3.setText(_translate("MainWindow", "messages"))
            self.f_send.setText(_translate("MainWindow", "Submit"))

    class main_popup2(QtWidgets.QMainWindow, whatsapp_popup2):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            try:

                parent_dir = "C:/WhatsappBulkSender/"
                all_dir = os.listdir(parent_dir)
                for o_dir in all_dir:
                    #                     print(o_dir)
                    self.com1.addItem(o_dir)
                    self.all_account.append(o_dir)
            except:
                pass

            self.f_send.clicked.connect(self.main_send)

        def main_send(self):
            try:

                global total
                global value_msg
                total_user = []
                global unique
                if self.r1.isChecked():
                    unique = "first"
#                     print("First Radio button")
#                     print(total_user)
                    total = total_user
                    self.hide()
        #             s=MainWindow()
        #             MainWindow.final_send(s)

                elif self.r2.isChecked():
                    unique = "second"
#                     print("Second Radio Button")
                    text = str(self.com1.currentText())
                    parent_dir = "C:/WhatsappBulkSender/"
                    main_path = os.path.join(parent_dir, text)
                    total_user.append(main_path)

#                     print(total_user)
                    total = total_user
                    self.hide()
        #             MainWindow.final_send(self)
        #             s=MainWindow()
        #             print(s.final_send())
        #             self.final_send()

                else:
                    #                     print("third radio button")
                    unique = "third"
                    value_msg = self.switch_2.value()
#                     print(value_msg)
                    all_acc = self.all_account.toPlainText()
                    parent_dir = "C:/WhatsappBulkSender/"
                    one_acc = all_acc.split('\n')
                    for single_acc in one_acc:
                        one_path = os.path.join(parent_dir, single_acc)
                        total_user.append(one_path)
#                     print(total_user)
                    total = total_user
                    self.hide()
            except:

                pass

    class whatsapp_popup1(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(657, 571)
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(100)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                MainWindow.sizePolicy().hasHeightForWidth())
            MainWindow.setSizePolicy(sizePolicy)
            MainWindow.setMinimumSize(QtCore.QSize(657, 571))
            MainWindow.setMaximumSize(QtCore.QSize(657, 571))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot1.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            MainWindow.setStyleSheet("background-color:white;")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(200, -10, 231, 41))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.show_multiple = QtWidgets.QTableWidget(self.centralwidget)
            self.show_multiple.setGeometry(QtCore.QRect(20, 150, 621, 281))
            self.show_multiple.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.show_multiple.setWordWrap(True)
            self.show_multiple.setObjectName("show_multiple")
            self.show_multiple.setColumnCount(2)
            self.show_multiple.setRowCount(0)
            item = QtWidgets.QTableWidgetItem()
            self.show_multiple.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.show_multiple.setHorizontalHeaderItem(1, item)
            self.show_multiple.horizontalHeader().setStretchLastSection(True)
            self.add_multiple = QtWidgets.QPushButton(self.centralwidget)
            self.add_multiple.setGeometry(QtCore.QRect(470, 70, 93, 28))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.add_multiple.setFont(font)
            self.add_multiple.setStyleSheet("color:white;\n"
                                            "background-color:#25D366")
            self.add_multiple.setObjectName("add_multiple")
            self.delete_multiple = QtWidgets.QPushButton(self.centralwidget)
            self.delete_multiple.setGeometry(QtCore.QRect(210, 470, 211, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.delete_multiple.setFont(font)
            self.delete_multiple.setStyleSheet("color:white;\n"
                                               "background-color:#25D366")
            self.delete_multiple.setObjectName("delete_multiple")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(70, 70, 161, 16))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.label_2.setFont(font)
            self.label_2.setObjectName("label_2")
            self.multi_input = QtWidgets.QLineEdit(self.centralwidget)
            self.multi_input.setGeometry(QtCore.QRect(250, 70, 191, 22))
            self.multi_input.setObjectName("multi_input")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Account"))
            self.label.setText(_translate(
                "MainWindow", "Add Multiple Account"))
            item = self.show_multiple.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Mobile Number"))
            item = self.show_multiple.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Path"))
            self.add_multiple.setText(_translate("MainWindow", "Add"))
            self.delete_multiple.setText(_translate(
                "MainWindow", "Delete Selected Row"))
            self.label_2.setText(_translate(
                "MainWindow", "Enter Mobile Number"))

    class main_popup1(QtWidgets.QMainWindow, whatsapp_popup1):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.add_multiple.clicked.connect(self.multiple_account)
            self.delete_multiple.clicked.connect(self.delete_account)
            parent_dir = "C:/WhatsappBulkSender/"
            try:

                all_dir = os.listdir(parent_dir)
                for o_dir in all_dir:
                    o_path = os.path.join(parent_dir, o_dir)

                    numRows = self.show_multiple.rowCount()
                    self.show_multiple.insertRow(numRows)
                    self.show_multiple.setItem(
                        numRows, 0, QtWidgets.QTableWidgetItem(o_dir))
                    self.show_multiple.setItem(
                        numRows, 1, QtWidgets.QTableWidgetItem(o_path))

            except:
                pass

        def delete_account(self):
            try:

                selected = self.show_multiple.currentRow()
                widgetItem = self.show_multiple.item(selected, 1)
                ans = widgetItem.text()
#                 print(selected)
#                 print(ans)

                self.show_multiple.removeRow(selected)
                shutil.rmtree(ans)
            except:
                pass

        def resource_path(self, relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        def multiple_account(self):
            try:

                parent_dir = "C:/WhatsappBulkSender/"

                mbl = self.multi_input.text()

                path = os.path.join(parent_dir, mbl)

                if os.path.exists(path):
                    print('Path Already Exists')
                else:
                    os.makedirs(path)

                    # chrome_path = "D:\drivers\chromedriver.exe"
                    chrome_options = Options()
                    chrome_options.add_argument(f'--user-data-dir={path}')
        #             chrome_options.add_argument('--user-data-dir=D://Whatsapp_Bulk_Do_Not_Delete')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--ignore-ssl-errors')

                    # Anish Chrome Path Fix
                    self.browser = webdriver.Chrome(self.resource_path(
                    './driver/chromedriver.exe'), options=chrome_options)
                    # self.browser = webdriver.Chrome(
                        # executable_path=chrome_path, options=chrome_options)
                    self.browser.get('https://web.whatsapp.com/')
                    try:

                        check_element = WebDriverWait(self.browser, 1000).until(
                            EC.presence_of_element_located((By.CLASS_NAME, search_boxji)))
                        numRows = self.show_multiple.rowCount()
                        self.show_multiple.insertRow(numRows)
                        self.show_multiple.setItem(
                            numRows, 0, QtWidgets.QTableWidgetItem(mbl))
                        self.show_multiple.setItem(
                            numRows, 1, QtWidgets.QTableWidgetItem(path))
                        sleep(2)
                        self.browser.quit()

                    except:
                        self.browser.quit()
            except:

                pass

    class whatsapp_popup3(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(588, 447)
            MainWindow.setMaximumSize(QtCore.QSize(588, 477))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot1.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser.setGeometry(QtCore.QRect(10, 70, 571, 351))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.textBrowser.setFont(font)
            self.textBrowser.setObjectName("textBrowser")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(170, 20, 211, 31))
            font = QtGui.QFont()
            font.setPointSize(18)
            font.setBold(True)
            font.setWeight(75)
            self.label.setFont(font)
            self.label.setObjectName("label")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 588, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Terms of Use"))
            self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">License Agreement</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">Please read the following important information before continuing.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">1. License key can be used by only one person or entity. This key cannot be used again in another system or computer. Once you enter the provided key during login process, you can use the tool from that system or computer only.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">2. Sharing of this tool is not allowed so it is advised that please do not try to share this tool with anyone. Attempt for sharing this tool could lead to cancellation of your license.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">3. In case of any issue occurs in software due to source site, then it will take minimum 07 days or maximum 60 days to get the issue resolved.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">4. In case of found any malicious user activity, the license will be revoked immediately without any warning.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">5. Once you make the payment, it will not be refunded to you in any case. Hence, you can\'t claim for refund after making payment.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">6. Source site will be responsible in case of any service interruption. Our software is only responsible for data extraction which is publicly available.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">7. We will not have or accept any liability, obligation or responsibility whatsoever for the content of source websites and will not accept any responsibility and shall not be held responsible for any loss or damage arising from or in respect of any use or misuse or reliance on content of source websites.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">8. Although the information provided to you on the site is obtained or compiled from sources we believe to be reliable, we cannot and do not guarantee the accuracy, validity or completeness of any information or data made available to you for any particular purpose.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">9. If software doesn\'t work or gets stopped permanently then you have an option to convert your license to any other software of same price. Moreover, this license conversion is possible only once.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:400;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400;\">10. This computer program is protected by copyright law and international treaties. Un-authorized reproduction or distribution of this program, or any portion of it, may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent possible under the law.</span></p></body></html>"))
            self.label.setText(_translate("MainWindow", "Terms of Use"))

    class main_popup3(QtWidgets.QMainWindow, whatsapp_popup3):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1243, 715)
            MainWindow.setMaximumSize(QtCore.QSize(1243, 715))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot1.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            MainWindow.setStyleSheet("background-color:white")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.resume = QtWidgets.QPushButton(self.centralwidget)
            self.resume.setGeometry(QtCore.QRect(970, 290, 93, 28))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.resume.setFont(font)
            self.resume.setStyleSheet("color:white;\n"
                                      "background-color:#25D366")
            self.resume.setObjectName("resume")
            self.time_delay = QtWidgets.QLineEdit(self.centralwidget)
            self.time_delay.setGeometry(QtCore.QRect(830, 450, 113, 22))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.time_delay.setFont(font)
            self.time_delay.setStyleSheet("background-color:white")
            self.time_delay.setObjectName("time_delay")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(360, 160, 241, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.label_2.setFont(font)
            self.label_2.setObjectName("label_2")
            self.label_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(20, 80, 271, 20))
            self.label_6.setObjectName("label_6")
            self.import_num = QtWidgets.QPushButton(self.centralwidget)
            self.import_num.setGeometry(QtCore.QRect(10, 30, 240, 31))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.import_num.setFont(font)
            self.import_num.setStyleSheet("color:white;\n"
                                          "background-color:#25D366")
            self.import_num.setObjectName("import_num")
            self.media_btn = QtWidgets.QPushButton(self.centralwidget)
            self.media_btn.setGeometry(QtCore.QRect(430, 440, 151, 28))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.media_btn.setFont(font)
            self.media_btn.setStyleSheet("color:white;\n"
                                         "background-color:#25D366")
            self.media_btn.setObjectName("media_btn")
            self.add_country_code = QtWidgets.QPushButton(self.centralwidget)
            self.add_country_code.setGeometry(QtCore.QRect(70, 180, 141, 28))
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(75)
            self.add_country_code.setFont(font)
            self.add_country_code.setStyleSheet("color:white;\n"
                                                "background-color:#25D366")
            self.add_country_code.setObjectName("add_country_code")
            self.select_acc = QtWidgets.QPushButton(self.centralwidget)
            self.select_acc.setGeometry(QtCore.QRect(430, 600, 151, 31))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.select_acc.setFont(font)
            self.select_acc.setStyleSheet("color:white;\n"
                                          "background-color:#25D366")
            self.select_acc.setObjectName("select_acc")
            self.label_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_5.setGeometry(QtCore.QRect(20, 70, 201, 16))
            self.label_5.setObjectName("label_5")
            self.label_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_7.setGeometry(QtCore.QRect(790, 410, 201, 21))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.label_7.setFont(font)
            self.label_7.setObjectName("label_7")
            self.file_btn = QtWidgets.QPushButton(self.centralwidget)
            self.file_btn.setGeometry(QtCore.QRect(430, 510, 151, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.file_btn.setFont(font)
            self.file_btn.setStyleSheet("color:white;\n"
                                        "background-color:#25D366")
            self.file_btn.setObjectName("file_btn")
            self.msg_box = QtWidgets.QTextEdit(self.centralwidget)
            self.msg_box.setGeometry(QtCore.QRect(310, 200, 401, 201))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.msg_box.setFont(font)
            self.msg_box.setStyleSheet("background-color:white")
            self.msg_box.setObjectName("msg_box")
            self.file = QtWidgets.QLabel(self.centralwidget)
            self.file.setGeometry(QtCore.QRect(440, 560, 141, 21))
            self.file.setText("")
            self.file.setObjectName("file")
            self.save_table = QtWidgets.QPushButton(self.centralwidget)
            self.save_table.setGeometry(QtCore.QRect(180, 620, 121, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.save_table.setFont(font)
            self.save_table.setStyleSheet("color:white;\n"
                                          "background-color:#25D366")
            self.save_table.setObjectName("save_table")
            self.group_btn = QtWidgets.QPushButton(self.centralwidget)
            self.group_btn.setGeometry(QtCore.QRect(760, 30, 221, 41))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.group_btn.setFont(font)
            self.group_btn.setStyleSheet("color:white;\n"
                                         "background-color:#25D366")
            self.group_btn.setObjectName("group_btn")
            self.add_multiple = QtWidgets.QPushButton(self.centralwidget)
            self.add_multiple.setGeometry(QtCore.QRect(990, 30, 231, 41))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.add_multiple.setFont(font)
            self.add_multiple.setStyleSheet("color:white;\n"
                                            "background-color:#25D366")
            self.add_multiple.setObjectName("add_multiple")
            self.media = QtWidgets.QLabel(self.centralwidget)
            self.media.setGeometry(QtCore.QRect(440, 480, 161, 20))
            self.media.setText("")
            self.media.setObjectName("media")
            self.pause = QtWidgets.QPushButton(self.centralwidget)
            self.pause.setGeometry(QtCore.QRect(860, 290, 93, 28))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.pause.setFont(font)
            self.pause.setStyleSheet("color:white;\n"
                                     "background-color:#25D366")
            self.pause.setObjectName("pause")
            self.stop = QtWidgets.QPushButton(self.centralwidget)
            self.stop.setGeometry(QtCore.QRect(750, 290, 93, 28))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.stop.setFont(font)
            self.stop.setStyleSheet("color:white;\n"
                                    "background-color:#25D366")
            self.stop.setObjectName("stop")
            self.country = QtWidgets.QLineEdit(self.centralwidget)
            self.country.setGeometry(QtCore.QRect(130, 140, 71, 22))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.country.setFont(font)
            self.country.setObjectName("country")
            self.group_box = QtWidgets.QTextEdit(self.centralwidget)
            self.group_box.setGeometry(QtCore.QRect(460, 20, 281, 61))
            self.group_box.setStyleSheet("background-color:white;\n"
                                         "")
            self.group_box.setObjectName("group_box")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(20, 140, 101, 21))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.clear_num = QtWidgets.QPushButton(self.centralwidget)
            self.clear_num.setGeometry(QtCore.QRect(30, 620, 111, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.clear_num.setFont(font)
            self.clear_num.setStyleSheet("color:white;\n"
                                         "background-color:#25D366")
            self.clear_num.setObjectName("clear_num")
            self.clear_msg = QtWidgets.QPushButton(self.centralwidget)
            self.clear_msg.setGeometry(QtCore.QRect(1080, 290, 131, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.clear_msg.setFont(font)
            self.clear_msg.setStyleSheet("color:white;\n"
                                         "background-color:#25D366")
            self.clear_msg.setObjectName("clear_msg")
            self.send = QtWidgets.QPushButton(self.centralwidget)
            self.send.setGeometry(QtCore.QRect(650, 590, 181, 51))
            font = QtGui.QFont()
            font.setPointSize(26)
            font.setBold(True)
            font.setWeight(75)
            self.send.setFont(font)
            self.send.setStyleSheet("color:white;\n"
                                    "background-color:#25D366")
            self.send.setObjectName("send")
            self.add_files = QtWidgets.QCheckBox(self.centralwidget)
            self.add_files.setGeometry(QtCore.QRect(610, 520, 141, 21))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.add_files.setFont(font)
            self.add_files.setObjectName("add_files")
            self.label_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_4.setGeometry(QtCore.QRect(910, 130, 141, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.label_4.setFont(font)
            self.label_4.setObjectName("label_4")
            self.add_media = QtWidgets.QCheckBox(self.centralwidget)
            self.add_media.setGeometry(QtCore.QRect(610, 440, 141, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.add_media.setFont(font)
            self.add_media.setObjectName("add_media")
            self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
            self.tableWidget.setGeometry(QtCore.QRect(30, 220, 251, 381))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.tableWidget.setFont(font)
            self.tableWidget.setStyleSheet("background-color:white;")
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)
            self.total_msg = QtWidgets.QLabel(self.centralwidget)
            self.total_msg.setGeometry(QtCore.QRect(800, 350, 411, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.total_msg.setFont(font)
            self.total_msg.setText("")
            self.total_msg.setObjectName("total_msg")
            self.manual = QtWidgets.QPushButton(self.centralwidget)
            self.manual.setGeometry(QtCore.QRect(270, 30, 163, 33))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.manual.setFont(font)
            self.manual.setStyleSheet("color:white;\n"
                                      "background-color:#25D366")
            self.manual.setObjectName("manual")
            self.show_result = QtWidgets.QTextEdit(self.centralwidget)
            self.show_result.setGeometry(QtCore.QRect(750, 180, 461, 101))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.show_result.setFont(font)
            self.show_result.setStyleSheet("background-color:white")
            self.show_result.setObjectName("show_result")
            self.label_9 = QtWidgets.QLabel(self.centralwidget)
            self.label_9.setGeometry(QtCore.QRect(780, 490, 301, 21))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.label_9.setFont(font)
            self.label_9.setObjectName("label_9")
            self.label_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_10.setGeometry(QtCore.QRect(800, 510, 151, 16))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.label_10.setFont(font)
            self.label_10.setObjectName("label_10")
            self.label_11 = QtWidgets.QLabel(self.centralwidget)
            self.label_11.setGeometry(QtCore.QRect(780, 530, 321, 21))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.label_11.setFont(font)
            self.label_11.setObjectName("label_11")
            self.label_12 = QtWidgets.QLabel(self.centralwidget)
            self.label_12.setGeometry(QtCore.QRect(800, 550, 161, 16))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.label_12.setFont(font)
            self.label_12.setObjectName("label_12")
            self.line = QtWidgets.QFrame(self.centralwidget)
            self.line.setGeometry(QtCore.QRect(0, 110, 1251, 16))
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            self.label_3.setGeometry(QtCore.QRect(320, 410, 361, 21))
            font = QtGui.QFont()
            font.setPointSize(7)
            self.label_3.setFont(font)
            self.label_3.setObjectName("label_3")
            self.License_show = QtWidgets.QLabel(self.centralwidget)
            self.License_show.setGeometry(QtCore.QRect(880, 0, 311, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.License_show.setFont(font)
            self.License_show.setStyleSheet("color:red;")
            self.License_show.setObjectName("License_show")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1243, 26))
            self.menubar.setObjectName("menubar")
            self.menuHelp = QtWidgets.QMenu(self.menubar)
            self.menuHelp.setObjectName("menuHelp")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
            self.License_btn = QtWidgets.QAction(MainWindow)
            self.License_btn.setObjectName("License_btn")
            self.menuHelp.addAction(self.License_btn)
            self.menubar.addAction(self.menuHelp.menuAction())

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate(
                "MainWindow", "Whatsapp Bulk Sender"))
            self.resume.setText(_translate("MainWindow", "RESUME"))
            self.label_2.setText(_translate(
                "MainWindow", "Please Type your Message"))
            self.label_6.setText(_translate(
                "MainWindow", "*Second Column should be Whatsapp Number"))
            self.import_num.setText(_translate(
                "MainWindow", "Import From Device"))
            self.media_btn.setText(_translate("MainWindow", "Select media"))
            self.add_country_code.setText(
                _translate("MainWindow", "Add Country Code"))
            self.select_acc.setText(_translate("MainWindow", "Select Account"))
            self.label_5.setText(_translate(
                "MainWindow", "* First Column should be Name"))
            self.label_7.setText(_translate(
                "MainWindow", "Time delay in seconds"))
            self.file_btn.setText(_translate("MainWindow", "Select file"))
            self.msg_box.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p></body></html>"))
            self.msg_box.setPlaceholderText(_translate(
                "MainWindow", "Type your message...."))
            self.save_table.setText(_translate("MainWindow", "Save Table"))
            self.group_btn.setText(_translate(
                "MainWindow", "Import From Group"))
            self.add_multiple.setText(_translate(
                "MainWindow", "Add Multiple Account"))
            self.pause.setText(_translate("MainWindow", "PAUSE"))
            self.stop.setText(_translate("MainWindow", "STOP"))
            self.group_box.setWhatsThis(_translate(
                "MainWindow", "<html><head/><body><p><br/></p></body></html>"))
            self.group_box.setPlaceholderText(_translate(
                "MainWindow", "Enter the manual Number or Group name"))
            self.label.setText(_translate("MainWindow", "Country Code"))
            self.clear_num.setText(_translate("MainWindow", "Clear Table"))
            self.clear_msg.setText(_translate("MainWindow", "CLEAR RESULT"))
            self.send.setText(_translate("MainWindow", "Send"))
            self.add_files.setText(_translate("MainWindow", "Send Files"))
            self.label_4.setText(_translate("MainWindow", "Showing Result"))
            self.add_media.setText(_translate("MainWindow", "Send Media"))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Name"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Mobile"))
            self.manual.setText(_translate("MainWindow", "Write Manually"))
            self.label_9.setText(_translate(
                "MainWindow", "* If you type 10 it will pick random digit "))
            self.label_10.setText(_translate("MainWindow", "between 0 and 10"))
            self.label_11.setText(_translate(
                "MainWindow", "* If you type 10,20 it will pick random digit"))
            self.label_12.setText(_translate(
                "MainWindow", "between 10 and 20"))
            self.label_3.setText(_translate(
                "MainWindow", "*If you type {} in message box, Name will printed instead of {}"))
            self.License_show.setText(_translate(
                "MainWindow", "License Valid Until : 25 June 2020"))
            self.menuHelp.setTitle(_translate("MainWindow", "Help"))
            self.License_btn.setText(_translate("MainWindow", "License"))

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.License_show.setText(message)

            self.import_num.clicked.connect(self.import_number)
    #         self.add_country.stateChanged.connect(self.add_country_code)
            self.clear_num.clicked.connect(self.clear_table)
    #         self.pushButton.clicked.connect(self.list_pop)
            self.send.clicked.connect(self.send_wala)
            self.select_acc.clicked.connect(self.rotate_send)
            self.media_btn.clicked.connect(self.get_path_media)
            self.file_btn.clicked.connect(self.get_path_file)
            self.manual.clicked.connect(self.import_manually)
            self.group_btn.clicked.connect(self.group_wala)
            self.stop.clicked.connect(self.kill_g)
            self.pause.clicked.connect(self.pause_g)
            self.resume.clicked.connect(self.resume_g)
            self.add_country_code.clicked.connect(self.add_country_codes)
            self.add_multiple.clicked.connect(self.multiple_account_popup)
            self.clear_msg.clicked.connect(self.clear_msg_box)
            self.save_table.clicked.connect(self.table_save_csv)
            self.License_btn.triggered.connect(self.license_popup)

        @QtCore.pyqtSlot()
        def send_wala(self):
            try:

                threading.Thread(target=self.final_send, daemon=True).start()
            except:
                pass

        @QtCore.pyqtSlot()
        def group_wala(self):
            try:

                threading.Thread(target=self.group_extractor,
                                 daemon=True).start()
            except:
                pass

        def rotate_send(self):
            try:

                self.k = main_popup2()
                self.k.show()
            except:
                pass

        def multiple_account_popup(self):
            try:

                self.y = main_popup1()
                self.y.show()
            except:
                pass

        def license_popup(self):
            try:

                self.t = main_popup3()
                self.t.show()
            except:
                passs

        def pause_g(self):
            try:

                self.show_result.append("Pause Button is Clicked!!!")
                self.is_paused = True
            except:
                pass

        def resume_g(self):
            try:

                self.show_result.append("Resume Button is Clicked!!!")
                self.is_paused = False
            except:
                pass

        def kill_g(self):
            try:

                self.show_result.append("Stop Button is Clicked!!!")
                self.is_killed = True
            except:
                pass

        def group_extractor(self):
            try:
                global unique

                all_url = self.group_box.toPlainText()
                sab_url = all_url.split('\n')

                if len(all_url) == 0:

                    self.show_result.append("Please Enter the Group name")
                else:
                    self.show_result.append(
                        "SCAN YOUR QR CODE FOR WHATSAPP WEB")
                    unique = "four"
                    self.whatsapp_login()
                    sleep(5)
                    Name = []
                    Mobile = []
                    initial_c = 0
                    try:
                        for groupji in sab_url:
                            sleep(2)
                            search_box = self.browser.find_element_by_class_name(
                                main_search_box)
                            search_box.send_keys(groupji+Keys.ENTER)
                            sleep(5)

                            all_group = self.browser.find_element_by_class_name(
                                group_member_extractor)
                            sleep(6)
                            all_member = all_group.text

                            z = all_member.split(',')

                            for one_member in z:
                                k = "".join(one_member.split())
                                if k[0] == '+':
                                    #                                 sliced=k[3:]
                                    sliced = k[3:]
                                    Mobile.append(sliced)
                                    Name.append("na")
            #                         print(sliced)
                                else:
                                    continue
                                sf = pandas.DataFrame(
                                    {'Name': Name, 'Mobile Number': Mobile})

                                row = sf.iloc[initial_c].T
            #                     new_row=[row[0],row[1]]
#                                 print(row[0])
#                                 print(row[1])
                                initial_c = len(Mobile)
                                numRows = self.tableWidget.rowCount()
                                self.tableWidget.insertRow(numRows)
                                # Add text to the row
                                self.tableWidget.setItem(
                                    numRows, 0, QtWidgets.QTableWidgetItem(row[0]))
                                self.tableWidget.setItem(
                                    numRows, 1, QtWidgets.QTableWidgetItem(row[1]))
                        self.show_result.append(
                            "Group Member Extraction completed")
                        self.browser.quit()

                    except:
                        self.show_result.append("No Group found")
                        self.browser.quit()

            except:
                self.show_result.append("Unable to fetch group member")
                self.show_result.append("Please Try again later!!!")

        def import_manually(self):
            try:

                all_number = self.group_box.toPlainText()
                one_number = all_number.split('\n')

                if len(all_number) == 0:

                    self.show_result.append("Please Enter the Number first")
                else:
                    self.group_box.clear()

                    for oneji in one_number:
                        if ',' in oneji:
                            o_oneji = oneji.split(',')
                            manual_number = o_oneji[0]
                            manual_name = o_oneji[1]
                        else:
                            manual_number = oneji
                            manual_name = "na"
                        numRows = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(numRows)
                        self.tableWidget.setItem(
                            numRows, 0, QtWidgets.QTableWidgetItem(manual_name))
                        self.tableWidget.setItem(
                            numRows, 1, QtWidgets.QTableWidgetItem(manual_number))

            except:
                pass

        def table_save_csv(self):
            try:

                file_path = QFileDialog.getSaveFileName(
                    self, 'Telegram UserId', './', "Excel (*.csv)")
#                 print(file_path[0])
                self.make_table_df()
                self.resend_df.to_csv(file_path[0], index=False)
                self.show_result.append("File Saved Successfully!!!")
#                 print('Save clicked')
            except:
                pass

        def clear_msg_box(self):
            try:
                self.show_result.clear()
                self.total_msg.clear()
            except:
                pass

        def make_table_df(self):
            try:

                rowCount = self.tableWidget.rowCount()
#                 print(rowCount)
                columnCount = self.tableWidget.columnCount()
#                 print(columnCount)
                NAME = []
                for row in range(rowCount):
                    widgetItem = self.tableWidget.item(row, 0)
                    try:

                        NAME.append(widgetItem.text())
                    except:
                        NAME.append(None)
#                 print(NAME)
                MOBILE = []
                for row in range(rowCount):
                    widgetItem = self.tableWidget.item(row, 1)
                    try:

                        MOBILE.append(widgetItem.text())
                    except:
                        MOBILE.append(None)
#                 print(MOBILE)
                self.resend_df = pd.DataFrame(list(zip(NAME, MOBILE)),
                                              columns=['NAME', 'MOBILE'])
#                 print(self.resend_df)
            except:
                pass

        def get_path_media(self):

            try:

                fileName = QFileDialog.getOpenFileNames(self, 'OpenFile', "")
                self.media_file = fileName[0]
                self.media.setText(str(len(self.media_file))+" Media Selected")
                self.add_media.setChecked(True)
            except:
                pass

        def get_path_file(self):
            try:

                fileName = QFileDialog.getOpenFileNames(self, 'OpenFile', "")

                self.doc_file = fileName[0]
                self.file.setText(str(len(self.doc_file))+" File Selected")
                self.add_files.setChecked(True)
            except:
                pass

        def import_number(self):

            try:

                fileName = QFileDialog.getOpenFileName(
                    self, 'OpenFile', "", "Excel (*.xls *.xlsx *.csv)")
#                 print(fileName)
                try:

                    df = pandas.read_excel(fileName[0])
                except:
                    df = pandas.read_csv(fileName[0])

#                 print(df)
                self.new_df = df
                self.very_new_df = df
#                 print(len(df))
                for c in range(len(df)):
                    row = df.iloc[c].T

                    numRows = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numRows)
                    self.tableWidget.setItem(
                        numRows, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(
                        numRows, 1, QtWidgets.QTableWidgetItem(str(row[1])))

            except:
                self.show_result.append("Failed to import Number")
                self.show_result.append("Please Try again later")

        def clear_table(self):
            try:

                for i in reversed(range(self.tableWidget.rowCount())):
                    self.tableWidget.removeRow(i)
            except:
                pass

        def resource_path(self, relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        def whatsapp_login(self):

            #             print(len(total))
            #             print(unique)

            try:

                if unique == "first":
                    # print("The login value is first")
                    # chrome_path = "D:\drivers\chromedriver.exe"
                    chrome_options = Options()
        #             chrome_options.add_argument('--user-data-dir=D://Whatsapp_Bulk_Do_Not_Delete')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--ignore-ssl-errors')
                    # Anish Chrome Path fix
                    self.browser = webdriver.Chrome(self.resource_path(
                    './driver/chromedriver.exe'), options=chrome_options)
                    # self.browser = webdriver.Chrome(
                    #     executable_path=chrome_path, options=chrome_options)

                elif unique == "second":
                    # print("The login value is second")
                    pathji = total[0]
                    # chrome_path = "D:\drivers\chromedriver.exe"
                    chrome_options = Options()

                    chrome_options.add_argument(f'--user-data-dir={pathji}')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--ignore-ssl-errors')

                    # Anish Chrome Path fix
                    self.browser = webdriver.Chrome(self.resource_path(
                        './driver/chromedriver.exe'), options=chrome_options)
                    # self.browser = webdriver.Chrome(
                    #     executable_path=chrome_path, options=chrome_options)

                elif unique == "third":
                    # print("The login value is third")
                    # chrome_path = "D:\drivers\chromedriver.exe"
                    chrome_options = Options()
                    chrome_options.add_argument(
                        f'--user-data-dir={self.naya_pathji}')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--ignore-ssl-errors')

                    # Anish Chrome Path fix
                    self.browser = webdriver.Chrome(self.resource_path(
                        './driver/chromedriver.exe'), options=chrome_options)
                    # self.browser = webdriver.Chrome(
                    #     executable_path=chrome_path, options=chrome_options)
                else:
                    print("I am getting executed")
                    # chrome_path = "D:\drivers\chromedriver.exe"
                    chrome_options = Options()
        #             chrome_options.add_argument('--user-data-dir=D://Whatsapp_Bulk_Do_Not_Delete')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--ignore-ssl-errors')

                    # Anish Chrome Path fix
                    self.browser = webdriver.Chrome(self.resource_path(
                        './driver/chromedriver.exe'), options=chrome_options)

                    # self.browser = webdriver.Chrome(
                    #     executable_path=chrome_path, options=chrome_options)

                self.browser.get('https://web.whatsapp.com/')
                try:

                    check_element = WebDriverWait(self.browser, 1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME, search_boxji)))

                    self.show_result.append("Logged In Successfully")
                except:
                    self.show_result.append("Not Logged In")

                    self.browser.quit()
            except:


                pass

        def send_attachment(self):


            try:
                for one_media in self.media_file:
                    sleep(1)

                    image_path = one_media.replace("/", "\\")
                    clipButton = self.browser.find_element_by_xpath(clipbtn)
                    clipButton.click()
                    sleep(1)
                    mediaButton = self.browser.find_element_by_xpath(
                        input_media)

                    mediaButton.send_keys(image_path)
                    sleep(3)
                    whatsapp_send_button = self.browser.find_element_by_xpath(
                        media_send_btn)
                    whatsapp_send_button.click()
                    self.show_result.append('Media sent')
            except:
                self.show_result.append('Media not sent')

        def send_files(self):


            try:
                for one_file in self.doc_file:
                    sleep(1)

                    docPath = one_file.replace("/", "\\")
                    clipButton = self.browser.find_element_by_xpath(clipbtn)
                    clipButton.click()
                    sleep(1)
                    docButton = self.browser.find_element_by_xpath(input_files)
                    docButton.send_keys(docPath)
                    sleep(3)
                    whatsapp_send_button = self.browser.find_element_by_xpath(
                        file_send_btn)
                    whatsapp_send_button.click()

                    self.show_result.append('File sent')
            except:
                self.show_result.append('File Not sent')

        def add_country_codes(self):
            code = self.country.text()
            if len(code) == 0:
                self.show_result.append("Please Input the country code")
            else:
                try:
                    self.make_table_df()
                    for i in reversed(range(self.tableWidget.rowCount())):
                        self.tableWidget.removeRow(i)

                    for c in range(len(self.resend_df)):
                        row = self.resend_df.iloc[c].T

                        numRows = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(numRows)
                        z = code+str(row[1])
#                         print(z)

                        self.tableWidget.setItem(
                            numRows, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                        self.tableWidget.setItem(
                            numRows, 1, QtWidgets.QTableWidgetItem(z))
                except:
                    # print(e)

                    pass

        def final_send(self):
            try:

                msgg = self.msg_box.toPlainText()
    #             print("The message is")
    #             print(msgg)

                rowCount = self.tableWidget.rowCount()
    #             print("The length of row is :")
    #             print(rowCount)

                columnCount = self.tableWidget.columnCount()
    #             print("The length of column is :")
    #             print(columnCount)
                NAME = []
                for row in range(rowCount):
                    widgetItem = self.tableWidget.item(row, 0)
                    try:

                        NAME.append(widgetItem.text())
                    except:
                        NAME.append(None)
    #             print(NAME)
                MOBILE = []
                for row in range(rowCount):
                    widgetItem = self.tableWidget.item(row, 1)
                    try:

                        MOBILE.append(widgetItem.text())
                    except:
                        MOBILE.append(None)
    #             print(MOBILE)
                send_df = pd.DataFrame(list(zip(NAME, MOBILE)),
                                       columns=['NAME', 'MOBILE'])
    #             print(send_df)
                if self.add_media.isChecked():
                    choice = "yes"
    #                 print(choice)
                else:
                    choice = ""
                if self.add_files.isChecked():
                    docChoice = "yes"
    #                 print(docChoice)
                else:
                    docChoice = ""

                time_dif = self.time_delay.text()
                if len(time_dif) == 0:
                    time_dif = '3,5'
    #                 print(time_dif)
                else:
                    pass
                if ',' in time_dif:

                    time_dif = time_dif
    #                 print(time_dif)
                else:
                    time_dif = '0,'+time_dif
    #                 print(time_dif)
                new_time = time_dif.split(',')
                a = new_time[0]
    #             print("first time is "+a)

                b = new_time[1]
    #             print("Second time is "+b)

                phone_ji = send_df.MOBILE
                phn_num = list(phone_ji.values)
    #             print("#############################################################")
    #             print(phn_num)
    #             print(type(phn_num))
        #         phn_num = list(chain.from_iterable(phone_ji))

                msgg = self.msg_box.toPlainText()
                total_number = len(phn_num)
                count = 0
    #             print(msgg)
                self.is_killed = False
                self.is_paused = False

                index = 0
    #             print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
                self.show_result.append("SCAN YOUR QR CODE FOR WHATSAPP WEB")
                if unique == "third":
                    check1 = len(phn_num)
    #                 print("The value of Check1 is ")
    #                 print(check1)
    #                 print(value_msg)
                    check2 = int(value_msg)
    #                 print("The value of Check2 is ")
    #                 print(check2)
                    if check1 % check2 == 0:

                        check3 = check1//check2
    #                     print("The value of check3 is ")
    #                     print(check3)
                    else:
                        check3 = check1//check2
                        check3 = check3+1
    #                     print("The value of check3 is ")
    #                     print(check3)

                    new_list = list(islice(cycle(total), check3))
    #                 print("The list is ###################################")
    #                 print(new_list)
                    the_keeper = 0
                    for new_pathji in new_list:
                        self.naya_pathji = new_pathji
                        if self.is_killed:
                            # self.show_result.append("Bulk WhatsApp Message Sending Stopped")
                            break

                        self.whatsapp_login()
                        sleep(4)
                        if re.findall('{}', msgg):
                            print(phn_num, type(phn_num))
                            for idx, p in enumerate(phn_num):

                                if p == "":
                                    continue
                                if idx == check2:
                                    #                                 print("Break up hogaya")
                                    self.browser.quit()
                                    break
                                if the_keeper == len(phn_num):
                                    break

                                p = phn_num[the_keeper]

        #                         phn_num.remove(p)
        #                         print("I am going to removed",p)
        #                         print(phn_num)
                                print(idx)

                                the_keeper += 1

                                new_name = send_df.NAME[send_df['MOBILE'] == p]
                                s = new_name[index]
                                message = re.sub('{}', s, msgg)
                                index = index+1
                                url_msg = quote(message)

                                try:

                                    link = 'https://web.whatsapp.com/send?phone=' + p + '&text=' + url_msg

                                    self.browser.get(link)
    #                                 print("Sending message to", p)
                                    sleep(4)

                                    self.show_result.append(
                                        '{}/{} => Sending message to {}.'.format((the_keeper), total_number, p))

                                    self.browser.implicitly_wait(10)
                                    try:
                                        click_btn = WebDriverWait(self.browser, delay).until(
                                            EC.element_to_be_clickable((By.CLASS_NAME, main_send_button)))
                                        sleep(2)
                                        click_btn.click()
                                        self.show_result.append("Message sent")
                                    except (UnexpectedAlertPresentException, NoAlertPresentException) as e:
                                        #                                     print("alert present")
                                        Alert(self.browser).accept()
                                        self.show_result.append(
                                            "Message not sent to " + p)

                                    if (choice == "yes"):
                                        try:
                                            sleep(3)
                                            self.send_attachment()
                                        except:
                                            print()
                                    if (docChoice == "yes"):
                                        try:
                                            sleep(3)
                                            self.send_files()
                                        except:
                                            print()
                                    sleep(random.randint(int(a), int(b)))
                                    count += 1
                                    self.show_result.append(
                                        "Message sent succesfully to" + p)
                                except Exception as e:
                                    #                                 print('Failed to send message to ' + str(p) + str(e))

                                    self.show_result.append(
                                        'Message not sent to ' + str(p))
                                while self.is_paused:
                                    time.sleep(0)

                                if self.is_killed:
                                    self.show_result.append(
                                        "Bulk WhatsApp Message Sending Stopped")
                                    break

        #             self.show_result.append(f"Total message sent out of {total_number} is {count}")
        #             self.total_msg.setText(f"Total message sent out of {total_number} is {count}")
        #             self.browser.quit()

                        else:
                            for idx, p in enumerate(phn_num):

                                if p == "":
                                    continue
                                if idx == check2:
                                    #                                 print("Break up hogaya")
                                    self.browser.quit()
                                    break
    #                             print("The value of the_keeper is ", the_keeper)
    #                             print("The value of phn_num is ", len(phn_num))

                                if the_keeper == len(phn_num):
                                    #                                 print("I am going to break down")
                                    break

                                p = phn_num[the_keeper]

        #                         phn_num.remove(p)
        #                         print("I am going to removed",p)
        #                         print(phn_num)
    #                             print(idx)

                                the_keeper += 1

                                url_msg = quote(msgg)

                                try:

                                    link = 'https://web.whatsapp.com/send?phone=' + p + '&text=' + url_msg
                                    # driver  = webdriver.Chrome()
                                    self.browser.get(link)
                                    sleep(4)
    #                                 print("Sending message to", p)
                                    self.show_result.append(
                                        '{}/{} => Sending message to {}.'.format((the_keeper), total_number, p))

                                    self.browser.implicitly_wait(10)
                                    try:
                                        click_btn = WebDriverWait(self.browser, delay).until(
                                            EC.element_to_be_clickable((By.CLASS_NAME, main_send_button)))
                                        sleep(2)
                                        click_btn.click()
                                        self.show_result.append("Message sent")
                                    except (UnexpectedAlertPresentException, NoAlertPresentException) as e:
                                        #                                     print("alert present")
                                        Alert(self.browser).accept()
    #                                     print(e)
                                        self.show_result.append(
                                            "Message not sent to " + p)
                                    if (choice == "yes"):
                                        try:
                                            sleep(3)
                                            self.send_attachment()
                                        except:
                                            print()
                                    if (docChoice == "yes"):
                                        try:
                                            sleep(3)
                                            self.send_files()
                                        except:
                                            print()
                                    sleep(random.randint(int(a), int(b)))
                                    count += 1
                                    self.show_result.append(
                                        "Message sent succesfully to" + p)
                                except Exception as e:
                                    #                                 print('Failed to send message to ' + str(p) + str(e))
                                    self.show_result.append(
                                        'Message not sent to ' + str(p))
                                while self.is_paused:
                                    time.sleep(0)

                                if self.is_killed:
                                    self.show_result.append(
                                        "Bulk WhatsApp Message Sending Stopped")
                                    break
                    self.show_result.append(
                        f"Total message sent out of {total_number} is {count}")
                    self.total_msg.setText(
                        f"Total message sent out of {total_number} is {count}")
                    self.browser.quit()

                else:
                    self.whatsapp_login()
                    sleep(4)
                    if re.findall('{}', msgg):
                        for idx, p in enumerate(phn_num):

                            if p == "":
                                continue

                            new_name = send_df.NAME[send_df['MOBILE'] == p]
                            s = new_name[index]
                            message = re.sub('{}', s, msgg)
                            index = index+1
                            url_msg = quote(message)

                            try:

                                link = 'https://web.whatsapp.com/send?phone=' + p + '&text=' + url_msg

                                self.browser.get(link)
    #                             print("Sending message to", p)
                                sleep(4)

                                self.show_result.append(
                                    '{}/{} => Sending message to {}.'.format((idx+1), total_number, p))

                                self.browser.implicitly_wait(10)
                                try:
                                    click_btn = WebDriverWait(self.browser, delay).until(
                                        EC.element_to_be_clickable((By.CLASS_NAME, main_send_button)))
                                    sleep(2)
                                    click_btn.click()
                                    self.show_result.append("Message sent")
                                except (UnexpectedAlertPresentException, NoAlertPresentException) as e:
                                    #                                 print("alert present")
                                    Alert(self.browser).accept()
                                    self.show_result.append(
                                        "Message not sent to " + p)

                                if (choice == "yes"):
                                    try:
                                        sleep(3)
                                        self.send_attachment()
                                    except:
                                        print()
                                if (docChoice == "yes"):
                                    try:
                                        sleep(3)
                                        self.send_files()
                                    except:
                                        print()
                                sleep(random.randint(int(a), int(b)))
                                count += 1
                                self.show_result.append(
                                    "Message sent succesfully to" + p)
                            except Exception as e:
                                #                             print('Failed to send message to ' + str(p) + str(e))

                                self.show_result.append(
                                    'Message not sent to ' + str(p))
                            while self.is_paused:
                                time.sleep(0)

                            if self.is_killed:
                                self.show_result.append(
                                    "Bulk WhatsApp Message Sending Stopped")
                                break

                        self.show_result.append(
                            f"Total message sent out of {total_number} is {count}")
                        self.total_msg.setText(
                            f"Total message sent out of {total_number} is {count}")
                        self.browser.quit()

                    else:
                        for idx, p in enumerate(phn_num):

                            if p == "":
                                continue

                            url_msg = quote(msgg)

                            try:

                                link = 'https://web.whatsapp.com/send?phone=' + p + '&text=' + url_msg
                                # driver  = webdriver.Chrome()
                                self.browser.get(link)
                                sleep(4)
    #                             print("Sending message to", p)
                                self.show_result.append(
                                    '{}/{} => Sending message to {}.'.format((idx+1), total_number, p))

                                self.browser.implicitly_wait(10)
                                try:
                                    click_btn = WebDriverWait(self.browser, delay).until(
                                        EC.element_to_be_clickable((By.CLASS_NAME, main_send_button)))
                                    sleep(2)
                                    click_btn.click()
                                    self.show_result.append("Message sent")
                                except (UnexpectedAlertPresentException, NoAlertPresentException) as e:
                                    #                                 print("alert present")
                                    Alert(self.browser).accept()
    #                                 print(e)
                                    self.show_result.append(
                                        "Message not sent to " + p)
                                if (choice == "yes"):
                                    try:
                                        sleep(3)
                                        self.send_attachment()
                                    except:
                                        print()
                                if (docChoice == "yes"):
                                    try:
                                        sleep(3)
                                        self.send_files()
                                    except:
                                        print()
                                sleep(random.randint(int(a), int(b)))
                                count += 1
                                self.show_result.append(
                                    "Message sent succesfully to" + p)
                            except Exception as e:
                                #                             print('Failed to send message to ' + str(p) + str(e))
                                self.show_result.append(
                                    'Message not sent to ' + str(p))
                            while self.is_paused:
                                time.sleep(0)

                            if self.is_killed:
                                self.show_result.append(
                                    "Bulk WhatsApp Message Sending Stopped")
                                break
                        self.show_result.append(
                            f"Total message sent out of {total_number} is {count}")
                        self.total_msg.setText(
                            f"Total message sent out of {total_number} is {count}")
                        self.browser.quit()

            except:
                pass
                # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", e)
                # self.browser.quit()
                # try:
                #     self.browser.quit()
                # except:
                #     pass

    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        def getToken(path):
            global message
            if os.path.exists(path):
                with open(path+'/token.txt', 'r') as f:
                    token = f.read()
                    f.close()
                print('Token taken from computer folder', token)
                cond, mess = auth(token, 'whatsapp')
                if cond:
                    message = mess
                    w = MainWindow()
                    w.show()
                    sys.exit(app.exec_())
                else:
                    print(f'here i am jghghjhjhjhjk')
                    print(mess)
                    message = mess
                    print(message)
                    w = Token_page()
                    w.show()
                    sys.exit(app.exec_())
            else:
                os.mkdir(path)
                print("open the token page and take the token")
                message = 'Please Enter your Token'
                w = Token_page()
                w.show()
                sys.exit(app.exec_())

    path = os.path.join("C:\\", "Token")
    getToken(path)


except:
    pass
