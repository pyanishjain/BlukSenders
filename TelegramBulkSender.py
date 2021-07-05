# https://web.telegram.org/#/im?p=@icospeaks
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QFileDialog
    import pandas
    import re
    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtWidgets import QMessageBox
    # from PyQt5.QtWidgets import *
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
    import time
    import datetime
    import os
    import argparse
    import platform
    import pandas as pd
    import re
    import threading
    import random
    import os
    import uuid
    # from bot_function import *

    # For Api calls
    from itertools import chain
    from datetime import datetime
    import requests
    import socket
    import json

    # base_url = "http://127.0.0.1:8000/"
    # base_url = "http://minerv100.herokuapp.com/"
    base_url = 'http://165.232.178.222/'

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
            elif remote_ip_address != local_ip_address:
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

    message = ''

    # login_locator_name = "im_dialog_peer"
    # sendbtn_class = 'composer_rich_textarea'
    # hamburger_icon = "//div[@class ='icon-hamburger-wrap']"
    # contact_button = '//span[@my-i18n="im_contacts"]'
    # contact_members_class = 'md_modal_list_peer_name'
    # contact_search_button = 'contacts_modal_search_field'
    # group_members_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "tg_head_peer_status", " " ))]//span'
    # username_className = 'md_modal_section_param_value'
    # contact_group_click_geturl = "md_modal_split_action_msg"
    # input_media = '//input[@accept="image/*, video/*, audio/*"]'
    # input_file = '//input[@title="Send file"]'
    # delay = 10

    # Getting variables from the api
    variables = getVariable('telegram')
    # for var in variables:
    #     print(var)

    # print('dfsadfsadfsdf', contact_members_class)
    # print('dfdfsdf', contact_search_button)
    # print('11111111', variables[4], ',2345', variables[5])

    # print("$$$$$$$$$$$$$44", variables[4])

    # print(type(contact_members_class), type(variables[4]))

    # if contact_members_class == variables[4].strip():
    #     print("HHAHHAHAHHAHAHAHAHAHAHAHAHH")

    login_locator_name = variables[0].strip()
    sendbtn_class = variables[1].strip()
    hamburger_icon = variables[2].strip()
    contact_button = variables[3].strip()
    contact_members_class = variables[4].strip()
    contact_search_button = variables[5].strip()
    group_members_xpath = variables[6].strip()
    username_className = variables[7].strip()
    contact_group_click_geturl = variables[8].strip()
    input_media = variables[9].strip()
    input_file = variables[10].strip()
    delay = int(variables[11])

    chrome_path = r"C:\Users\ANISH JAIN\Music\chromedriver.exe"

    class Ui_MainWindowzero(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(891, 301)
            MainWindow.setMaximumSize(QtCore.QSize(891, 301))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            MainWindow.setFont(font)
            MainWindow.setStyleSheet("background-color:white;")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot3.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
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
            self.token_show.setGeometry(QtCore.QRect(5, 39, 750, 31))
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
                "MainWindow", "Telegram Bulk Sender"))
            self.label.setText(_translate("MainWindow", "Enter the Token Id"))
            self.token_click.setText(_translate("MainWindow", "Submit"))

    class Token_page(QtWidgets.QMainWindow, Ui_MainWindowzero):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.token_show.setText(message)
            self.token_click.clicked.connect(self.main_page)

        def main_page(self):
            # Anish Write your code
            # Token Input
            # tokenji=self.token_input.text()
            #self.token_show.setText("Invalid Token Id")

            global message
            token = self.token_input.text().strip()
            print(token)
            path = os.path.join("C:\\", "Token")
            with open(path+'/token.txt', 'w') as f:
                f.write(token)
                f.close()
            cond, mess = auth(token, 'telegram')
            if cond:
                print("everything works", mess)
                message = mess
                print("#####", message)
                self.z = MainWindow()
                self.z.show()
                self.hide()
            # sys.exit(app.exec_())
            else:
                print('somthing went wrong')
                message = mess
                self.token_show.setText(message)
                # w = Token_page()
                # w.show()
                # # w.hide()
                # # w.show()
                # sys.exit(app.exec_())

    class Ui_MainWindows(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(588, 447)
            MainWindow.setMaximumSize(QtCore.QSize(588, 477))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot3.png"),
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

    class MainWindow_main(QtWidgets.QMainWindow, Ui_MainWindows):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

    class Ui_MainWindowone(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1239, 724)
            MainWindow.setMaximumSize(QtCore.QSize(1239, 724))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot3.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            font = QtGui.QFont()
            font.setPointSize(9)
            MainWindow.setFont(font)
            MainWindow.setStyleSheet("border-top-color: rgb(86, 130, 163);\n"
                                     "background-color: rgb(255, 255, 255);")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.import_userid = QtWidgets.QPushButton(self.centralwidget)
            self.import_userid.setGeometry(QtCore.QRect(30, 20, 161, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.import_userid.setFont(font)
            self.import_userid.setStyleSheet("color: white;\n"
                                             "background-color:#5682a3")
            self.import_userid.setObjectName("import_userid")
            self.group_btn = QtWidgets.QPushButton(self.centralwidget)
            self.group_btn.setGeometry(QtCore.QRect(800, 40, 181, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.group_btn.setFont(font)
            self.group_btn.setStyleSheet("color: white;\n"
                                         "background-color:#5682a3")
            self.group_btn.setObjectName("group_btn")
            self.account_btn = QtWidgets.QPushButton(self.centralwidget)
            self.account_btn.setGeometry(QtCore.QRect(1000, 40, 211, 41))
            font = QtGui.QFont()
            font.setFamily("Arial Black")
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.account_btn.setFont(font)
            self.account_btn.setStyleSheet("color: white;\n"
                                           "background-color:#5682a3")
            self.account_btn.setObjectName("account_btn")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(220, 30, 161, 31))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.label_2.setFont(font)
            self.label_2.setObjectName("label_2")
            self.url_group = QtWidgets.QTextEdit(self.centralwidget)
            self.url_group.setGeometry(QtCore.QRect(390, 20, 401, 71))
            font = QtGui.QFont()
            font.setPointSize(7)
            self.url_group.setFont(font)
            self.url_group.setStyleSheet("background-color:white")
            self.url_group.setObjectName("url_group")
            self.show_userid = QtWidgets.QTableWidget(self.centralwidget)
            self.show_userid.setGeometry(QtCore.QRect(20, 140, 281, 451))
            self.show_userid.setStyleSheet("background-color:white;")
            self.show_userid.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.show_userid.setObjectName("show_userid")
            self.show_userid.setColumnCount(2)
            self.show_userid.setRowCount(0)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.show_userid.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.show_userid.setHorizontalHeaderItem(1, item)
            self.clear_userid = QtWidgets.QPushButton(self.centralwidget)
            self.clear_userid.setGeometry(QtCore.QRect(20, 610, 121, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.clear_userid.setFont(font)
            self.clear_userid.setStyleSheet("color: white;\n"
                                            "background-color:#5682a3")
            self.clear_userid.setObjectName("clear_userid")
            self.save_table = QtWidgets.QPushButton(self.centralwidget)
            self.save_table.setGeometry(QtCore.QRect(160, 610, 111, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.save_table.setFont(font)
            self.save_table.setStyleSheet("color: white;\n"
                                          "background-color:#5682a3")
            self.save_table.setObjectName("save_table")
            self.clear_msg = QtWidgets.QPushButton(self.centralwidget)
            self.clear_msg.setGeometry(QtCore.QRect(750, 380, 131, 31))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.clear_msg.setFont(font)
            self.clear_msg.setStyleSheet("color: white;\n"
                                         "background-color:#5682a3")
            self.clear_msg.setObjectName("clear_msg")
            self.label_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_4.setGeometry(QtCore.QRect(390, 120, 211, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.label_4.setFont(font)
            self.label_4.setObjectName("label_4")
            self.msg_box = QtWidgets.QTextEdit(self.centralwidget)
            self.msg_box.setGeometry(QtCore.QRect(330, 160, 381, 241))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.msg_box.setFont(font)
            self.msg_box.setStyleSheet("background-color:white;")
            self.msg_box.setObjectName("msg_box")
            self.show_result = QtWidgets.QTextEdit(self.centralwidget)
            self.show_result.setGeometry(QtCore.QRect(750, 210, 461, 141))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.show_result.setFont(font)
            self.show_result.setStyleSheet("background-color:white;")
            self.show_result.setObjectName("show_result")
            self.label_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_5.setGeometry(QtCore.QRect(880, 180, 181, 20))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.label_5.setFont(font)
            self.label_5.setObjectName("label_5")
            self.media_btn = QtWidgets.QPushButton(self.centralwidget)
            self.media_btn.setGeometry(QtCore.QRect(390, 440, 131, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.media_btn.setFont(font)
            self.media_btn.setStyleSheet("color: white;\n"
                                         "background-color:#5682a3")
            self.media_btn.setObjectName("media_btn")
            self.file_btn = QtWidgets.QPushButton(self.centralwidget)
            self.file_btn.setGeometry(QtCore.QRect(390, 530, 131, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.file_btn.setFont(font)
            self.file_btn.setStyleSheet("color: white;\n"
                                        "background-color:#5682a3")
            self.file_btn.setObjectName("file_btn")
            self.label_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(770, 460, 211, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.label_6.setFont(font)
            self.label_6.setObjectName("label_6")
            self.time_delay = QtWidgets.QLineEdit(self.centralwidget)
            self.time_delay.setGeometry(QtCore.QRect(800, 500, 111, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.time_delay.setFont(font)
            self.time_delay.setStyleSheet("background-color:white;")
            self.time_delay.setObjectName("time_delay")
            self.media_check = QtWidgets.QCheckBox(self.centralwidget)
            self.media_check.setGeometry(QtCore.QRect(570, 450, 141, 20))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(10)
            self.media_check.setFont(font)
            self.media_check.setStyleSheet("")
            self.media_check.setObjectName("media_check")
            self.file_check = QtWidgets.QCheckBox(self.centralwidget)
            self.file_check.setGeometry(QtCore.QRect(560, 540, 111, 20))
            font = QtGui.QFont()
            font.setFamily("Segoe Print")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.file_check.setFont(font)
            self.file_check.setStyleSheet("")
            self.file_check.setObjectName("file_check")
            self.Send_btn = QtWidgets.QPushButton(self.centralwidget)
            self.Send_btn.setGeometry(QtCore.QRect(550, 600, 121, 61))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.Send_btn.setFont(font)
            self.Send_btn.setStyleSheet("color: white;\n"
                                        "background-color:#5682a3")
            self.Send_btn.setObjectName("Send_btn")
            self.total_msg = QtWidgets.QLabel(self.centralwidget)
            self.total_msg.setGeometry(QtCore.QRect(850, 420, 361, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.total_msg.setFont(font)
            self.total_msg.setText("")
            self.total_msg.setObjectName("total_msg")
            self.label_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_7.setGeometry(QtCore.QRect(30, 70, 241, 16))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.label_7.setFont(font)
            self.label_7.setObjectName("label_7")
            self.label_8 = QtWidgets.QLabel(self.centralwidget)
            self.label_8.setGeometry(QtCore.QRect(30, 90, 261, 16))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.label_8.setFont(font)
            self.label_8.setObjectName("label_8")
            self.med_path = QtWidgets.QLabel(self.centralwidget)
            self.med_path.setGeometry(QtCore.QRect(380, 490, 151, 16))
            self.med_path.setText("")
            self.med_path.setObjectName("med_path")
            self.fil_path = QtWidgets.QLabel(self.centralwidget)
            self.fil_path.setGeometry(QtCore.QRect(390, 590, 111, 20))
            self.fil_path.setText("")
            self.fil_path.setObjectName("fil_path")
            self.stop = QtWidgets.QPushButton(self.centralwidget)
            self.stop.setGeometry(QtCore.QRect(910, 380, 81, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.stop.setFont(font)
            self.stop.setStyleSheet("color: white;\n"
                                    "background-color:#5682a3")
            self.stop.setObjectName("stop")
            self.pause = QtWidgets.QPushButton(self.centralwidget)
            self.pause.setGeometry(QtCore.QRect(1020, 380, 81, 28))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.pause.setFont(font)
            self.pause.setStyleSheet("color: white;\n"
                                     "background-color:#5682a3")
            self.pause.setObjectName("pause")
            self.resume = QtWidgets.QPushButton(self.centralwidget)
            self.resume.setGeometry(QtCore.QRect(1130, 380, 81, 28))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.resume.setFont(font)
            self.resume.setStyleSheet("color: white;\n"
                                      "background-color:#5682a3")
            self.resume.setObjectName("resume")
            self.label_9 = QtWidgets.QLabel(self.centralwidget)
            self.label_9.setGeometry(QtCore.QRect(780, 540, 301, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.label_9.setFont(font)
            self.label_9.setObjectName("label_9")
            self.label_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_10.setGeometry(QtCore.QRect(790, 570, 151, 16))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.label_10.setFont(font)
            self.label_10.setObjectName("label_10")
            self.label_11 = QtWidgets.QLabel(self.centralwidget)
            self.label_11.setGeometry(QtCore.QRect(780, 590, 321, 21))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.label_11.setFont(font)
            self.label_11.setObjectName("label_11")
            self.label_12 = QtWidgets.QLabel(self.centralwidget)
            self.label_12.setGeometry(QtCore.QRect(790, 620, 161, 16))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.label_12.setFont(font)
            self.label_12.setObjectName("label_12")
            self.line = QtWidgets.QFrame(self.centralwidget)
            self.line.setGeometry(QtCore.QRect(-10, 110, 1251, 20))
            self.line.setStyleSheet("")
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            self.License_show = QtWidgets.QLabel(self.centralwidget)
            self.License_show.setGeometry(QtCore.QRect(890, 0, 400, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.License_show.setFont(font)
            self.License_show.setStyleSheet("color:red;")
            self.License_show.setObjectName("License_show")
            self.label_13 = QtWidgets.QLabel(self.centralwidget)
            self.label_13.setGeometry(QtCore.QRect(330, 410, 361, 21))
            font = QtGui.QFont()
            font.setPointSize(7)
            self.label_13.setFont(font)
            self.label_13.setObjectName("label_13")
            MainWindow.setCentralWidget(self.centralwidget)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1239, 26))
            self.menubar.setObjectName("menubar")
            self.menuHelp = QtWidgets.QMenu(self.menubar)
            self.menuHelp.setObjectName("menuHelp")
            MainWindow.setMenuBar(self.menubar)
            self.License_btn = QtWidgets.QAction(MainWindow)
            self.License_btn.setObjectName("License_btn")
            self.menuHelp.addAction(self.License_btn)
            self.menubar.addAction(self.menuHelp.menuAction())

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate(
                "MainWindow", "Telegram Bulk Sender"))
            self.import_userid.setText(_translate(
                "MainWindow", "Import from File"))
            self.group_btn.setText(_translate(
                "MainWindow", "Extract from Group"))
            self.account_btn.setText(_translate(
                "MainWindow", "Extract from Account"))
            self.label_2.setText(_translate(
                "MainWindow", "Enter the url of Group"))
            self.url_group.setPlaceholderText(_translate(
                "MainWindow", "You can enter multiple Telegram Group url....."))
            item = self.show_userid.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Name"))
            item = self.show_userid.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "User Id"))
            self.clear_userid.setText(_translate("MainWindow", "CLEAR TABLE"))
            self.save_table.setText(_translate("MainWindow", "SAVE TABLE"))
            self.clear_msg.setText(_translate("MainWindow", "CLEAR RESULT"))
            self.label_4.setText(_translate(
                "MainWindow", "Please Type your Message"))
            self.msg_box.setPlaceholderText(_translate(
                "MainWindow", "Please Type your message....."))
            self.label_5.setText(_translate("MainWindow", "Showing Result"))
            self.media_btn.setText(_translate("MainWindow", "Select Media"))
            self.file_btn.setText(_translate("MainWindow", "Select File"))
            self.label_6.setText(_translate(
                "MainWindow", "Time Delay in Seconds"))
            self.media_check.setText(_translate("MainWindow", "Send Media"))
            self.file_check.setText(_translate("MainWindow", "Send File"))
            self.Send_btn.setText(_translate("MainWindow", "SEND"))
            self.label_7.setText(_translate(
                "MainWindow", "* First Column should be Name"))
            self.label_8.setText(_translate(
                "MainWindow", "*Second Column should be UserId"))
            self.stop.setText(_translate("MainWindow", "STOP"))
            self.pause.setText(_translate("MainWindow", "PAUSE"))
            self.resume.setText(_translate("MainWindow", "RESUME"))
            self.label_9.setText(_translate(
                "MainWindow", "* If you type 10 it will pick random digit "))
            self.label_10.setText(_translate("MainWindow", "between 0 and 10"))
            self.label_11.setText(_translate(
                "MainWindow", "* If you type 10,20 it will pick random digit"))
            self.label_12.setText(_translate(
                "MainWindow", "between 10 and 20"))
            self.License_show.setText(_translate(
                "MainWindow", "License Valid Until : 25 June 2020"))
            self.label_13.setText(_translate(
                "MainWindow", "*If you type {} in message box, Name will printed instead of {}"))
            self.menuHelp.setTitle(_translate("MainWindow", "Help"))
            self.License_btn.setText(_translate("MainWindow", "License"))

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindowone):
        valueChanged = QtCore.pyqtSignal(list)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.License_show.setText(message)
            self.is_paused = False
            self.is_killed = False

            self.Send_btn.clicked.connect(self.send_wala)
            self.valueChanged.connect(self.on_value_changed)
            self.import_userid.clicked.connect(self.import_number)
            self.clear_userid.clicked.connect(self.clear_table)
            self.media_btn.clicked.connect(self.get_path_media)
            self.file_btn.clicked.connect(self.get_path_file)

            self.group_btn.clicked.connect(self.on_clicked)

            self.account_btn.clicked.connect(self.account_wala)
            self.save_table.clicked.connect(self.table_save_csv)
            self.clear_msg.clicked.connect(self.clear_msg_box)
            self.stop.clicked.connect(self.kill_g)
            self.pause.clicked.connect(self.pause_g)
            self.resume.clicked.connect(self.resume_g)
            self.License_btn.triggered.connect(self.license_popup)
            # License_show

        @QtCore.pyqtSlot()
        def send_wala(self):
            threading.Thread(target=self.final_send, daemon=True).start()

        @QtCore.pyqtSlot()
        def account_wala(self):
            threading.Thread(target=self.account_extract, daemon=True).start()

        @QtCore.pyqtSlot()
        def on_clicked(self):
            threading.Thread(target=self.group_extract, daemon=True).start()

        @QtCore.pyqtSlot(list)
        def on_value_changed(self, value):

            numRows = self.show_userid.rowCount()
            self.show_userid.insertRow(numRows)
            # Add text to the row
            self.show_userid.setItem(
                numRows, 0, QtWidgets.QTableWidgetItem(value[0]))
            self.show_userid.setItem(
                numRows, 1, QtWidgets.QTableWidgetItem(value[1]))

        def pause_g(self):
            self.show_result.append("Pause Button is Clicked!!!")
            self.is_paused = True

        def resume_g(self):
            self.show_result.append("Resume Button is Clicked!!!")
            self.is_paused = False

        def kill_g(self):
            self.show_result.append("Stop Button is Clicked!!!")
            self.is_killed = True

        def license_popup(self):

            self.t = MainWindow_main()
            self.t.show()

        def clear_msg_box(self):
            try:
                self.show_result.clear()
                self.total_msg.clear()
            except:
                pass

        def resource_path(self, relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        def telegram_login(self):
            try:
                self.show_result.append("Work in Progress")
                # chrome_path = "D:\drivers\chromedriver.exe"
                chrome_options = Options()
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_argument('--ignore-ssl-errors')
                chrome_options.add_argument('--user-data-dir=./User_Data')
                # self.browser = webdriver.Chrome(self.resource_path(
                #     './driver/chromedriver.exe'), options=chrome_options)
                self.browser = webdriver.Chrome(
                    executable_path=chrome_path, options=chrome_options)
                self.browser.get('https://web.telegram.org/#/login')
                try:

                    check_element = WebDriverWait(self.browser, 1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME, login_locator_name)))

                    self.show_result.append("Logged In Successfully")
                except:
                    self.show_result.append("Not Logged In")

                    self.browser.quit()

            except:
                pass

        def account_extract(self):
            try:

                self.is_killed = False
                self.is_paused = False
                kintinBarSearchKare = 20

                Name = []
                userids = []
                initial_c = 0
                self.telegram_login()
                sleep(5)
                loginCheck = self.browser.find_element_by_class_name(
                    login_locator_name)
                if loginCheck.is_displayed():

                    self.show_result.append("Extracting User Id... ")
                    sleep(3)

                    def clickContactBTN():
                        try:
                            WebDriverWait(self.browser, 30).until(
                                EC.element_to_be_clickable((By.XPATH, hamburger_icon))).click()
                            # driver.find_elements_by_class_name('icon-hamburger-wrap')[0].click()
                            sleep(1)
                            WebDriverWait(self.browser, 30).until(
                                EC.element_to_be_clickable((By.XPATH, contact_button))).click()
                            self.browser.find_element_by_xpath(
                                contact_button).click()
                        except:
                            pass

                    clickContactBTN()
                    sleep(3)

                    member_urls = []
                    names = []
                    userNames = []
                    userIds = []

                    def getMembers(char, index):

                        try:
                            self.browser.find_element_by_class_name(
                                contact_search_button).send_keys(char)

                            name = self.browser.execute_script(
                                f"return document.getElementsByClassName('{contact_members_class}')[{index}].textContent")
        #                     print(name)
                            # names.append(name)
                            self.browser.execute_script(
                                f"document.getElementsByClassName('{contact_members_class}')[{index}].click()")
                            curl = self.browser.current_url
                            var = curl.split("=")[-1]
                            if var not in userids:
                                userids.append(var)
                                Name.append(name)
#                               print("I am working")
#                             for word in names:
#                                 if word not in Name:
#                                     Name.append(word)
# #                                     print(Name)
#                             for shabd in member_urls:
#                                 if shabd not in userids:
#                                     userids.append(shabd)
# #                                     print(userids)

                            clickContactBTN()

                        except IndexError as error:
                            self.browser.find_element_by_class_name(
                                contact_search_button).clear()
                            sleep(1)
                            print(e)
                            return 'noContact'
                        except Exception as e:
                            self.browser.find_element_by_class_name(
                                contact_search_button).clear()
                            sleep(1)
                            print(e)
                            return 'noContact'

                    alphabet = 'abcdefghijklmnopqrstuvwxyz'
                    alphabetji = []
                    betabet = []
                    for index, char in enumerate(alphabet):
                        for i in range(26):
                            if index > i:
                                for j in range(i):
                                    s = char + alphabet[j]
                                    betabet.append(s)

                            if alphabet[i] == char:
                                s = char
                            else:
                                s = char+alphabet[i]
                            betabet.append(s)
                            for pattern in betabet:
                                if pattern not in alphabetji:
                                    alphabetji.append(pattern)

                    try:

                        self.browser.maximize_window()
                    except:
                        pass
                    for char in alphabetji:
                        if self.is_killed:

                            self.browser.quit()
                            self.show_result.append(
                                "Account member userId extraction Stopped!!!")

                            break
                        for k in range(kintinBarSearchKare):
                            var = getMembers(char, k)
                            if var == 'noContact':
                                break
                            sleep(2)
                            try:

                                self.kf = pandas.DataFrame(
                                    {'Name': Name, 'User Id': userids})

                                row = self.kf.iloc[initial_c].T
                                new_row = [row[0], row[1]]
#                                 print(row[0])
#                                 print(row[1])
                                initial_c = len(Name)
#                                 print("The Lenght of Name is ")
#                                 print(len(Name))
                                numRows = self.show_userid.rowCount()
                                self.show_userid.insertRow(numRows)
                                self.show_userid.setItem(
                                    numRows, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                                self.show_userid.setItem(
                                    numRows, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                            except:
                                pass
                            while self.is_paused:
                                time.sleep(0)

                            if self.is_killed:
                                self.browser.quit()
                                self.show_result.append(
                                    "Account member userId extraction Stopped!!!")

                                break
                    self.browser.quit()
                    self.show_result.append(
                        "Account member userId extracted Successfully!!!")
                    sleep(4)

                else:
                    self.browser.quit()
                    self.show_result.append("Not Logged In!!!")
                    self.show_result.append(
                        "Please check your mobile number or otp")
            except:
                pass

        def table_save_csv(self):
            try:

                file_path = QFileDialog.getSaveFileName(
                    self, 'Telegram UserId', './', "Excel (*.csv)")
#                 print(file_path[0])
                self.make_table_df()
                self.send_df.to_csv(file_path[0], index=False)
                self.show_result.append("File Saved Successfully!!!")
#                 print('Save clicked')
            except:
                pass

        def group_extract(self):
            try:
                self.is_killed = False
                self.is_paused = False
                userId = []
                initial_c = 0

    #             group_members_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "tg_head_peer_status", " " ))]//span'
    #             username_className = 'md_modal_section_param_value'
                mainnames = []
#                 print("Work is going on")
                all_url = self.url_group.toPlainText()
                sab_url = all_url.split('\n')

                if len(all_url) == 0:
                    self.show_result.append("Please Enter the url")
                else:
                    self.telegram_login()
                    sleep(5)
                    try:
                        #                         print("all well")

                        loginCheck = self.browser.find_element_by_class_name(
                            login_locator_name)
                    except:
                        self.browser.quit()
                        self.show_result.append("Not Logged In!!!")
                        self.show_result.append(
                            "Please check your mobile number or otp")

                    if loginCheck.is_displayed():

                        self.show_result.append(
                            "Extracting Group Member User Id....")
                        for url in sab_url:
                            #                             print("very good")
                            def getGroup(link):
                                self.browser.get(url)
                                sleep(1)
                                try:

                                    WebDriverWait(self.browser, 50).until(
                                        EC.element_to_be_clickable((By.XPATH, group_members_xpath))).click()
                                except:
                                    self.browser.quit()
                                    self.show_result.append(
                                        "Group member user Id extraction Failed!!!")
                                    self.show_result.append(
                                        "please try again later")

                                sleep(2)
                                totalMembersCount = len(
                                    self.browser.find_elements_by_class_name(contact_members_class))
                                return totalMembersCount

                            totalMembersCount = getGroup(url)

                            for i in range(1, totalMembersCount, 2):
                                getGroup(url)
#                                 print("hey")

                                try:

                                    mainname = self.browser.find_elements_by_class_name(contact_members_class)[
                                        i].text
#                                     print(mainname)
                    #                 print("hey")
                                    mainnames.append(mainname)
                                except:
                                    mainnames.append(None)

                                try:

                                    self.browser.find_elements_by_class_name(
                                        contact_members_class)[i].click()
                                    sleep(2)
                                    self.browser.find_elements_by_class_name(
                                        contact_group_click_geturl)[1].click()
                                    curl = self.browser.current_url
                                    uid = curl.split("=")[-1]
                                    userId.append(uid)
#                                     print(uid)
                                except Exception as e:
                                    userId.append(None)

                                sf = pandas.DataFrame(
                                    {'Name': mainnames, 'User Id': userId})

                                row = sf.iloc[initial_c].T
                                new_row = [row[0], row[1]]
#                                 print(row[0])
#                                 print(row[1])
                                initial_c = len(mainnames)
                                self.valueChanged.emit(new_row)
                                while self.is_paused:
                                    time.sleep(0)

                                if self.is_killed:
                                    self.show_result.append(
                                        "Group member userId extraction Stopped!!!")

                                    break
                        self.show_result.append(
                            "UserId Extracted Successfully")
                        self.browser.quit()
                    else:
                        self.browser.quit()
                        self.show_result.append("Not Logged In!!!")
                        self.show_result.append(
                            "Please check your mobile number or otp")
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

                    numRows = self.show_userid.rowCount()
                    self.show_userid.insertRow(numRows)
                    self.show_userid.setItem(
                        numRows, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    z = str(row[1])
#                     print(z)
                    if len(z) > 20 and z[0] == 'u':
                        z = z

                    elif z[0] == '@':
                        z = z
                    else:
                        z = '@'+z

                    self.show_userid.setItem(
                        numRows, 1, QtWidgets.QTableWidgetItem(z))
            except:
                pass

        def clear_table(self):
            try:

                for i in reversed(range(self.show_userid.rowCount())):

                    self.show_userid.removeRow(i)
            except:
                pass

        def get_path_media(self):

            try:

                fileName = QFileDialog.getOpenFileNames(self, 'OpenFile', "")
                self.media_file = fileName[0]
                self.med_path.setText(
                    str(len(self.media_file))+" Media Selected")
                self.media_check.setChecked(True)
            except:
                pass

        def get_path_file(self):
            try:

                fileName = QFileDialog.getOpenFileNames(self, 'OpenFile', "")

                self.doc_file = fileName[0]
                self.fil_path.setText(str(len(self.doc_file))+" File Selected")
                self.file_check.setChecked(True)
            except:
                pass
    #         print(doc_file)

        def send_attachment(self):
            for one_media in self.media_file:

                image_path = one_media.replace("/", "\\")
                sleep(1)
                try:

                    clipButton = self.browser.find_element_by_xpath(
                        input_media)
                    sleep(1)
                    clipButton.send_keys(image_path)
                    self.show_result.append("Media Sent")
                except:
                    self.show_result.append("Media Not Sent")
                sleep(3)

        def send_files(self):
            for one_file in self.doc_file:

                docPath = one_file.replace("/", "\\")

                try:
                    sleep(1)
                    docButton = self.browser.find_element_by_xpath(input_file)
                    sleep(2)
                    docButton.send_keys(docPath)
                    self.show_result.append("File Sent")
                except:
                    self.show_result.append("File Not Sent")
                sleep(3)

        def make_table_df(self):
            try:

                rowCount = self.show_userid.rowCount()
#                 print(rowCount)
                columnCount = self.show_userid.columnCount()
#                 print(columnCount)
                NAME = []
                for row in range(rowCount):
                    widgetItem = self.show_userid.item(row, 0)
                    try:

                        NAME.append(widgetItem.text())
                    except:
                        NAME.append(None)
#                 print(NAME)
                MOBILE = []
                for row in range(rowCount):
                    widgetItem = self.show_userid.item(row, 1)
                    try:

                        MOBILE.append(widgetItem.text())
                    except:
                        MOBILE.append(None)
#                 print(MOBILE)
                self.send_df = pd.DataFrame(list(zip(NAME, MOBILE)),
                                            columns=['NAME', 'MOBILE'])
#                 print(self.send_df)
            except:
                pass

        def final_send(self):
            try:
                self.is_killed = False
                self.is_paused = False
                self.telegram_login()
                sleep(4)
                loginCheck = self.browser.find_element_by_class_name(
                    login_locator_name)
                if loginCheck.is_displayed():
                    #                     self.show_result.append("Logged IN Successfully!!!")
                    #                 campName=self.camp_name.text()
                    time_dif = self.time_delay.text()
                    if len(time_dif) == 0:
                        time_dif = '3,5'
#                         print(time_dif)
                    else:
                        pass
                    if ',' in time_dif:

                        time_dif = time_dif
#                         print(time_dif)
                    else:
                        time_dif = '0,'+time_dif
#                         print(time_dif)
                    new_time = time_dif.split(',')
                    a = new_time[0]
#                     print("first time is "+a)

                    b = new_time[1]
#                     print("Second time is "+b)
    #                 self.show_result.append("Campaign Name:- "+campName)

                    if self.media_check.isChecked():
                        choice = "yes"
#                         print(choice)
                    else:
                        choice = ""
                    if self.file_check.isChecked():
                        docChoice = "yes"
#                         print(docChoice)
                    else:
                        docChoice = ""
                    self.make_table_df()

                    phn_num = self.send_df.MOBILE
                    total_number = len(phn_num)
                    msgg = self.msg_box.toPlainText()
                    count = 0
#                     print(msgg)
            #         msg='hello how are you {}'
                    index = 0

                    if re.findall('{}', msgg):

                        for idx, p in enumerate(phn_num):
                            if p == "":
                                continue

                            new_name = self.send_df.NAME[self.send_df['MOBILE'] == p]
                            s = new_name[index]
                            message = re.sub('{}', s, msgg)
                            index = index+1

                            try:

                                link = 'https://web.telegram.org/#/im?p='+p
                                # driver  = webdriver.Chrome()
                                self.browser.get(link)
                                sleep(2)
        #                         print("Sending message to "+ p)
#                                 print('{}/{} => Sending message to {}.'.format((idx+1), total_number, p))
        #                         self.show_result.append("Sending message to "+ p)
        #                         self.textChanged.emit(p)

                                self.show_result.append(
                                    '{}/{} => Sending message to {}.'.format((idx+1), total_number, p))

                                self.browser.implicitly_wait(10)
                                try:
                                    input_box = WebDriverWait(self.browser, delay).until(
                                        EC.element_to_be_clickable((By.CLASS_NAME, sendbtn_class)))
                                    sleep(random.randint(0, 2))
                                    if "\n" in message:
                                        for part in message.split('\n'):

                                            input_box.send_keys(part)
                                            ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
                                                Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

                                    else:
                                        message = message
                                        input_box.send_keys(message)
#
                                    input_box.send_keys(Keys.ENTER)

                                    sleep(3)

                                except (UnexpectedAlertPresentException, NoAlertPresentException) as e:
                                    #                                     print("alert present")
                                    Alert(self.browser).accept()
#                                     print("Message not sent to "+ p)
                                    self.show_result.append(
                                        "Message not sent to " + p)

                                if (choice == "yes"):
                                    try:
                                        sleep(4)
                                        self.send_attachment()

                                    except:
                                        print()
                                if (docChoice == "yes"):
                                    try:
                                        sleep(4)
                                        self.send_files()

                                    except:
                                        print()
#                                 print(time_dif)
#                                 print("Message sent succesfully to "+ p)
                                sleep(random.randint(int(a), int(b)))
                                self.show_result.append("Message sent to " + p)

                                count += 1

                            except Exception as e:
                                #                                 print('Failed to send message to ' + str(p) + str(e))
                                self.show_result.append(
                                    'Failed to send message to ' + str(p))
                            while self.is_paused:
                                time.sleep(0)

                            if self.is_killed:
                                self.show_result.append(
                                    "Bulk Telegram Message Sending Stopped")
                                break
#                         print(f"Total message sent out of {total_number} is {count}")
                        self.show_result.append(
                            f"Total message sent out of {total_number} is {count}")
                        self.total_msg.setText(
                            f"Total message sent out of {total_number} is {count}")

                    else:

                        for idx, p in enumerate(phn_num):
                            if p == "":
                                continue
                            try:

                                link = 'https://web.telegram.org/#/im?p='+p
                                self.browser.get(link)
                                sleep(2)
        #                             print("Sending message to"+ p)
#                                     print('{}/{} => Sending message to {}.'.format((idx+1), total_number, p))
                                self.show_result.append(
                                    '{}/{} => Sending message to {}.'.format((idx+1), total_number, p))
                                sleep(2)

        #                             self.show_result.append("Sending message to"+ p)

                                self.browser.implicitly_wait(10)
                                try:
                                    input_box = WebDriverWait(self.browser, delay).until(
                                        EC.element_to_be_clickable((By.CLASS_NAME, sendbtn_class)))
                                    sleep(1)
                                    if "\n" in msgg:
                                        for part in msgg.split('\n'):

                                            input_box.send_keys(part)
                                            ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
                                                Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

                                    else:
                                        msgg = msgg
                                        input_box.send_keys(msgg)

                                    sleep(1)
                                    input_box.send_keys(Keys.ENTER)
                                    sleep(3)

                                except (UnexpectedAlertPresentException, NoAlertPresentException) as e:
                                    #                                         print("alert present")
                                    Alert(browser).accept()
#                                         print("Message not sent to"+ p)
                                    self.show_result.append(
                                        "Message not sent to" + p)
                                if (choice == "yes"):
                                    try:
                                        sleep(4)
                                        self.send_attachment()

                                    except:
                                        print()
                                if (docChoice == "yes"):
                                    try:
                                        sleep(4)
                                        self.send_files()

                                    except:
                                        print()

#                                     print(time_dif)
#                                     print("Message sent succesfully to "+ p)
                                sleep(2)
                                sleep(random.randint(int(a), int(b)))
                                self.show_result.append("Message sent to " + p)

                                count += 1

                            except Exception as e:
                                #                                 print('Failed to send message to ' + str(p) + str(e))
                                self.show_result.append(
                                    'Failed to send message to ' + str(p))
                            while self.is_paused:
                                time.sleep(0)

                            if self.is_killed:
                                self.show_result.append(
                                    "Bulk Telegram Message Sending Stopped")
                                break
#                         print(f"Total message sent out of {total_number} is {count}")
                        self.show_result.append(
                            f"Total message sent out of {total_number} is {count}")
                        self.total_msg.setText(
                            f"Total message sent out of {total_number} is {count}")
                    self.show_result.append("Task Completed")
                    self.browser.quit()

                else:
                    self.browser.quit()
                    self.show_result.append("Not Logged In!!!")
                    self.show_result.append("Please Login first")
            except Exception as e:
                #                 print(e)

                self.show_result.append(
                    "Make Sure You follows the Correct Steps!!!")
                self.show_result.append("Please Try again later")

    import sys

    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        def getToken(path):
            global message
            if os.path.exists(path):
                with open(path+'/token.txt', 'r') as f:
                    token = f.read()
                    f.close()
                print('Token taken from computer folder', token)
                cond, mess = auth(token, 'telegram')
                cond = True
                if cond:
                    print("hi there")
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


except Exception as e:
    print(e)
