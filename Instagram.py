try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    import pprint
    from time import sleep
    from InstagramAPI import InstagramAPI
    import pandas as pd
    import random
    import threading
    import sys
    import os
    # from bot_function import *

    # For Api calls Begins
    from itertools import chain
    from datetime import datetime
    import requests
    import socket
    import json

    # base_url = "http://127.0.0.1:8000/"
    # base_url = "http://minerv100.herokuapp.com/"
    base_url = 'http://165.232.178.222/'

    def getIpAddress():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
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

    following_users = []
    follower_users = []
    message = ''

    class Ui_MainWindowzero(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(891, 301)
            MainWindow.setMaximumSize(QtCore.QSize(891, 301))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot2.png"),
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
            self.token_show.setGeometry(QtCore.QRect(10, 39, 600, 31))
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
                "MainWindow", "Instagram Follower Booster"))
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
            global message
            token = self.token_input.text()
            print(token)
            path = os.path.join("C:\\", "Token")
            with open(path+'/token.txt', 'w') as f:
                f.write(token)
                f.close()
            cond, mess = auth(token, 'instagram')
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

    class Ui_MainWindows(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(588, 447)
            MainWindow.setMaximumSize(QtCore.QSize(588, 477))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot2.png"),
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

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1181, 651)
            MainWindow.setMaximumSize(QtCore.QSize(1181, 651))
            MainWindow.setStyleSheet("background-color:white")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(60, 130, 161, 31))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./bot2.png"),
                           QtGui.QIcon.Selected, QtGui.QIcon.On)
            MainWindow.setWindowIcon(icon)
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.username = QtWidgets.QLineEdit(self.centralwidget)
            self.username.setGeometry(QtCore.QRect(230, 130, 211, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.username.setFont(font)
            self.username.setObjectName("username")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(60, 190, 161, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_2.setFont(font)
            self.label_2.setObjectName("label_2")
            self.password = QtWidgets.QLineEdit(self.centralwidget)
            self.password.setGeometry(QtCore.QRect(230, 190, 211, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.password.setFont(font)
            self.password.setObjectName("password")
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            self.label_3.setGeometry(QtCore.QRect(60, 260, 281, 16))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_3.setFont(font)
            self.label_3.setObjectName("label_3")
            self.label_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_4.setGeometry(QtCore.QRect(60, 380, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_4.setFont(font)
            self.label_4.setObjectName("label_4")
            self.time_delay = QtWidgets.QLineEdit(self.centralwidget)
            self.time_delay.setGeometry(QtCore.QRect(300, 370, 113, 41))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.time_delay.setFont(font)
            self.time_delay.setObjectName("time_delay")
            self.label_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_5.setGeometry(QtCore.QRect(520, -10, 241, 71))
            font = QtGui.QFont()
            font.setPointSize(22)
            font.setBold(True)
            font.setWeight(75)
            self.label_5.setFont(font)
            self.label_5.setStyleSheet("color:#405DE6;\n"
                                       "")
            self.label_5.setObjectName("label_5")
            self.get_follower = QtWidgets.QPushButton(self.centralwidget)
            self.get_follower.setGeometry(QtCore.QRect(50, 530, 241, 51))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.get_follower.setFont(font)
            self.get_follower.setStyleSheet("color:white;\n"
                                            "background-color:#405DE6")
            self.get_follower.setObjectName("get_follower")
            self.show_result = QtWidgets.QTextEdit(self.centralwidget)
            self.show_result.setGeometry(QtCore.QRect(800, 170, 351, 251))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.show_result.setFont(font)
            self.show_result.setObjectName("show_result")
            self.label_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(900, 120, 161, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_6.setFont(font)
            self.label_6.setStyleSheet("color:#F77737")
            self.label_6.setObjectName("label_6")
            self.stop = QtWidgets.QPushButton(self.centralwidget)
            self.stop.setGeometry(QtCore.QRect(790, 450, 81, 28))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.stop.setFont(font)
            self.stop.setStyleSheet("color:white;\n"
                                    "background-color:#5851DB")
            self.stop.setObjectName("stop")
            self.pause = QtWidgets.QPushButton(self.centralwidget)
            self.pause.setGeometry(QtCore.QRect(880, 450, 81, 28))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.pause.setFont(font)
            self.pause.setStyleSheet("color:white;\n"
                                     "background-color:#833AB4")
            self.pause.setObjectName("pause")
            self.resume = QtWidgets.QPushButton(self.centralwidget)
            self.resume.setGeometry(QtCore.QRect(970, 450, 91, 28))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.resume.setFont(font)
            self.resume.setStyleSheet("color:white;\n"
                                      "background-color:#C13584")
            self.resume.setObjectName("resume")
            self.clear_box = QtWidgets.QPushButton(self.centralwidget)
            self.clear_box.setGeometry(QtCore.QRect(1070, 450, 71, 31))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.clear_box.setFont(font)
            self.clear_box.setStyleSheet("color:white;\n"
                                         "background-color:#E1306C")
            self.clear_box.setObjectName("clear_box")
            self.show_msg = QtWidgets.QLabel(self.centralwidget)
            self.show_msg.setGeometry(QtCore.QRect(790, 550, 351, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(True)
            font.setWeight(75)
            self.show_msg.setFont(font)
            self.show_msg.setText("")
            self.show_msg.setObjectName("show_msg")
            self.label_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_7.setGeometry(QtCore.QRect(430, 60, 491, 16))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_7.setFont(font)
            self.label_7.setStyleSheet("color:#FD1D1D")
            self.label_7.setObjectName("label_7")
            self.label_8 = QtWidgets.QLabel(self.centralwidget)
            self.label_8.setGeometry(QtCore.QRect(350, 320, 281, 31))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.label_8.setFont(font)
            self.label_8.setObjectName("label_8")
            self.comp_username = QtWidgets.QTextEdit(self.centralwidget)
            self.comp_username.setGeometry(QtCore.QRect(340, 240, 411, 71))
            font = QtGui.QFont()
            font.setPointSize(8)
            self.comp_username.setFont(font)
            self.comp_username.setObjectName("comp_username")
            self.label_9 = QtWidgets.QLabel(self.centralwidget)
            self.label_9.setGeometry(QtCore.QRect(300, 420, 371, 20))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.label_9.setFont(font)
            self.label_9.setObjectName("label_9")
            self.label_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_10.setGeometry(QtCore.QRect(300, 450, 391, 20))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.label_10.setFont(font)
            self.label_10.setObjectName("label_10")
            self.label_11 = QtWidgets.QLabel(self.centralwidget)
            self.label_11.setGeometry(QtCore.QRect(300, 480, 291, 21))
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(False)
            font.setWeight(50)
            self.label_11.setFont(font)
            self.label_11.setObjectName("label_11")
            self.license_show = QtWidgets.QLabel(self.centralwidget)
            self.license_show.setGeometry(QtCore.QRect(30, 30, 321, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.license_show.setFont(font)
            self.license_show.setStyleSheet("color:white;\n"
                                            "background-color:red;")
            self.license_show.setObjectName("license_show")
            self.unfollow_btn = QtWidgets.QPushButton(self.centralwidget)
            self.unfollow_btn.setGeometry(QtCore.QRect(360, 530, 281, 51))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.unfollow_btn.setFont(font)
            self.unfollow_btn.setStyleSheet("color:white;\n"
                                            "background-color:#405DE6")
            self.unfollow_btn.setObjectName("unfollow_btn")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1181, 26))
            self.menubar.setObjectName("menubar")
            self.menuHelp = QtWidgets.QMenu(self.menubar)
            self.menuHelp.setObjectName("menuHelp")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
            self.license_btn = QtWidgets.QAction(MainWindow)
            self.license_btn.setCheckable(False)
            self.license_btn.setChecked(False)
            self.license_btn.setEnabled(True)
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(75)
            self.license_btn.setFont(font)
            self.license_btn.setObjectName("license_btn")
            self.menuHelp.addAction(self.license_btn)
            self.menubar.addAction(self.menuHelp.menuAction())

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate(
                "MainWindow", "Instagram Follower Booster"))
            self.label.setText(_translate("MainWindow", "YOUR USERNAME"))
            self.label_2.setText(_translate("MainWindow", "YOUR PASSWORD"))
            self.label_3.setText(_translate(
                "MainWindow", "YOUR COMPETITOR USERNAME"))
            self.label_4.setText(_translate(
                "MainWindow", "TIME DELAY IN SECONDS"))
            self.label_5.setText(_translate("MainWindow", "INSTAGRAM"))
            self.get_follower.setText(_translate(
                "MainWindow", "BOOST YOUR FOLLOWERS"))
            self.label_6.setText(_translate("MainWindow", "Showing Result"))
            self.stop.setText(_translate("MainWindow", "STOP"))
            self.pause.setText(_translate("MainWindow", "PAUSE"))
            self.resume.setText(_translate("MainWindow", "RESUME"))
            self.clear_box.setText(_translate("MainWindow", "CLEAR"))
            self.label_7.setText(_translate(
                "MainWindow", "WE DO NOT STORE YOUR USERNAME AND PASSWORD"))
            self.label_8.setText(_translate(
                "MainWindow", "* his/her recent posts should have some likes"))
            self.comp_username.setPlaceholderText(_translate(
                "MainWindow", "You can add multiple target usernames...."))
            self.label_9.setText(_translate(
                "MainWindow", "* If you type 10, it will pick random digit between 0 and 10"))
            self.label_10.setText(_translate(
                "MainWindow", "* If you type 10,20 it will pick random digit between 10 and 20"))
            self.label_11.setText(_translate(
                "MainWindow", "* Set this really long  to avoid from Suspension"))
            self.license_show.setText(_translate(
                "MainWindow", "License valid until  20 April 2021"))
            self.unfollow_btn.setText(_translate(
                "MainWindow", "UNFOLLOW YOUR FOLLOWING"))
            self.menuHelp.setTitle(_translate("MainWindow", "Help"))
            self.license_btn.setText(_translate("MainWindow", "License"))

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.is_killed = False
            self.is_paused = False
            self.license_show.setText(message)
            self.stop.clicked.connect(self.kill_g)
            self.pause.clicked.connect(self.pause_g)
            self.resume.clicked.connect(self.resume_g)
            self.clear_box.clicked.connect(self.clear_msg_box)
            self.get_follower.clicked.connect(self.on_clicked)
            self.license_btn.triggered.connect(self.license_popup)
            self.unfollow_btn.clicked.connect(self.on_unfollow)

        @QtCore.pyqtSlot()
        def on_clicked(self):
            threading.Thread(target=self.hello, daemon=True).start()

        @QtCore.pyqtSlot()
        def on_unfollow(self):
            threading.Thread(target=self.unfollow_following,
                             daemon=True).start()

        def license_popup(self):
            self.t = MainWindow_main()
            self.t.show()

        def pause_g(self):
            self.show_result.append("Pause Button is Clicked!!!")
            self.is_paused = True

        def resume_g(self):
            self.show_result.append("Resume Button is Clicked!!!")
            self.is_paused = False

        def kill_g(self):
            self.show_result.append("Stop Button is Clicked!!!")
            self.is_killed = True

        def clear_msg_box(self):
            try:
                self.show_result.clear()
                self.show_msg.clear()
            except:
                pass

        def unfollow_following(self):
            try:
                self.show_result.append("Work in Progress")
                following_users = []
                follower_users = []

                self.is_killed = False
                self.is_paused = False
                counting = 0
                username1 = self.username.text()
                password1 = self.password.text()
                time_dif = self.time_delay.text()
                if len(time_dif) == 0:
                    time_dif = '5,10'
#                     print(time_dif)
                else:
                    pass
                if ',' in time_dif:

                    time_dif = time_dif
#                     print(time_dif)
                else:
                    time_dif = '0,'+time_dif
#                     print(time_dif)
                new_time = time_dif.split(',')
                c = new_time[0]
#                 print("first time is "+c)

                d = new_time[1]
#                 print("Second time is "+d)
                self.api = InstagramAPI(username1, password1)
                api = self.api
                api.login()
                api.getSelfUserFollowers()
                result = api.LastJson
                for user in result['users']:
                    follower_users.append(
                        {'pk': user['pk'], 'username': user['username']})

                api.getSelfUsersFollowing()
                result = api.LastJson
                for user in result['users']:
                    following_users.append(
                        {'pk': user['pk'], 'username': user['username']})

                for idx, user in enumerate(following_users):
                    if not user['pk'] in [user['pk'] for user in follower_users]:
                        while self.is_paused:

                            sleep(0)

                        if self.is_killed:
                            self.show_result.append(
                                "Unfollow following Stopped!!!")
        #                     self.show_result.append("Total unfollow is "+{counting})
        #                     self.show_msg.setText("Total unfollow is "+{counting})

                            break
        #                 print('Unfollowing @' + user['username'])
                        self.show_result.append('{}.'.format(
                            (counting+1))+'Unfollowing @' + user['username'])
                        api.unfollow(user['pk'])
                        counting += 1
                        # set this really long to avoid from suspension
                        sleep(random.randint(int(c), int(d)))
                self.show_result.append(f"Total unfollowing is {counting}")
                self.show_msg.setText(f"Total unfollowing is {counting}")
            except:
                self.show_result.append("Please check your Credentials!!!")

        def hello(self):
            self.show_result.append("Work in Progress!!!")

            all_username = self.comp_username.toPlainText()
            o_username = all_username.split('\n')
#             print("The total username are ")
    #         print(o_username)
            self.count = 0

            username1 = self.username.text()
            password1 = self.password.text()
    #         print(len(username))
    #         print(len(username1))
    #         print(len(password1))

            if len(username1) == 0 or len(password1) == 0:

                self.show_result.append("Please Fill out the Details")

            else:

                time_dif = self.time_delay.text()
                if len(time_dif) == 0:
                    time_dif = '5,10'
#                     print(time_dif)
                else:
                    pass
                if ',' in time_dif:

                    time_dif = time_dif
#                     print(time_dif)
                else:
                    time_dif = '0,'+time_dif
#                     print(time_dif)
                new_time = time_dif.split(',')
                self.a = new_time[0]
#                 print("first time is "+self.a)

                self.b = new_time[1]
#                 print("Second time is "+self.b)

                for username in o_username:
                    username = username.rstrip()
                    if len(username) == 0:
                        continue
                    else:
                        if self.is_killed:

                            # self.show_result.append("Total Unique Account Followed is "+{self.count})
                            # self.show_msg.setText("Total Unique Account Followed is "+{self.count})

                            break
                        self.show_result.append(
                            f"Your Competitor username is {username}")
                        self.show_result.append("      ")

    #                     print("This time username is "+ username)

                        self.get_likes_list(username)
                self.show_result.append(
                    f"Total Unique Account Followed is {self.count}")
                self.show_msg.setText(
                    f"Total Unique Account Followed is {self.count}")
                self.show_result.append("Task Completed")

        def get_likes_list(self, username):
            try:

                self.is_killed = False
                self.is_paused = False
                users_list = []

    #             print(username)
                username1 = self.username.text()
                password1 = self.password.text()
                self.api = InstagramAPI(username1, password1)
                api = self.api
                api.login()

                api.searchUsername(username)  # Gets most recent post from user
                result = api.LastJson
                username_id = result['user']['pk']
                user_posts = api.getUserFeed(username_id)
                result = api.LastJson
                media_id = result['items'][0]['id']

                api.getMediaLikers(media_id)
                users = api.LastJson['users']
                for user in users:
                    users_list.append(
                        {'pk': user['pk'], 'username': user['username']})

                self.follow_users(users_list)

            except:
                self.show_result.append("Wrong Credentials!!!")
                self.show_result.append("Please Check your Credentials!!!")

        def follow_users(self, users_list):

            try:

                api = self.api
                api.login()
                api.getSelfUsersFollowing()
                result = api.LastJson
                following_users = []
                follower_users = []
    #             print(self.a)
    #             print(self.b)
                for user in result['users']:

                    following_users.append(user['pk'])
        #             for idx, p in enumerate(phn_num):
                for idx, user in enumerate(users_list):
                    while self.is_paused:

                        sleep(0)

                    if self.is_killed:
                        self.show_result.append("Gaining Follower Stopped!!!")
                        # self.show_result.append("Total Unique Account Followed is "+{self.count})
                        # self.show_msg.setText("Total Unique Account Followed is "+{self.count})

                        break

                    if not user['pk'] in following_users:

                        self.show_result.append('{}.'.format(
                            (idx+1))+' Following @' + user['username'])
    #                     print('{}.'.format((idx+1))+' Following @' + user['username'])
                        api.follow(user['pk'])
                        self.count += 1
                        # set this really long to avoid from suspension
                        sleep(random.randint(int(self.a), int(self.b)))
                    else:
                        self.show_result.append('{}.'.format(
                            (idx+1)) + ' Already following @' + user['username'])
    #                     print('{}.'.format((idx+1))+ ' Already following @' + user['username'])
                        sleep(random.randint(int(self.a), int(self.b)))

                self.show_result.append(" ")
            except Exception as e:
                print(e)
                self.show_result.append("Please Try again later")

    #         print(self.count)

    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        def getToken(path):
            global message
            if os.path.exists(path):
                with open(path+'/token.txt', 'r') as f:
                    token = f.read()
                    f.close()
                print('Token taken from computer folder', token)
                cond, mess = auth(token, 'instagram')
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


except Exception as e:
    print(e)
