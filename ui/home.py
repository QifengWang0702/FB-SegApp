# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QMessageBox, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from ui.extra import Extra_UI
from util.service import *


# noinspection PyArgumentList
class home_UI(QWidget):
    openConfigClicked = pyqtSignal(int)
    updateStatusClicked = pyqtSignal(tuple)

    def __init__(self, computerStatus):
        super(home_UI, self).__init__()

        self.home_layout = QGridLayout()
        self.setLayout(self.home_layout)

        configs = getConfigs()
        self.pic_path = configs['save']['pic']
        self.configs_path = configs['save']['configs']
        self.ico = configs['picture']['ico']
        self.tutorial = configs['picture']['tutorial']
        self.logo = configs['picture']['logo']
        self.homes = configs['picture']['homes']

        self.lastTime = getLastLoginTime()
        self.reportNum = getReportNum()
        self.computerStatus = computerStatus
        self.userInfo = getUserInfo()

        if self.userInfo['identity'] == 'A':
            self.init_UI_A()
        else:
            self.init_UI_D()

    def init_UI_D(self):
        self.widget1 = QWidget()
        self.widget1.setObjectName('widget1')
        self.layout1 = QGridLayout()
        self.widget1.setLayout(self.layout1)

        self.widget2 = QWidget()
        self.widget2.setObjectName('widget2')
        self.layout2 = QGridLayout()
        self.widget2.setLayout(self.layout2)

        self.home_layout.addWidget(self.widget1, 0, 0, 3, 10)  # 上
        self.home_layout.addWidget(self.widget2, 3, 0, 12, 10)  # 下

        # 上
        self.label_1 = QLabel("")
        self.label_1.setPixmap(QPixmap(f'{self.pic_path}/{self.logo}').scaled(290, 290))
        self.label_2 = QLabel("Welcome to IRSPUI !     ")

        # 下
        self.buttons = []
        self.buttons.append(QPushButton("Beginner's\nTutorial\n\n\n\n\n\n"))
        self.buttons.append(QPushButton(f"Historical reports\ncurrently have {self.reportNum}\n\n\n"))

        lastText = f'The last login was on\n{self.lastTime}\n'
        if self.lastTime == '2024-01-01':
            lastText = 'This is the first\ntime login\n'
        self.buttons.append(QPushButton(lastText))

        statusText = "Equipment inspection\nDevice is ready\n\n\n"
        if self.computerStatus[0] == -1 or self.computerStatus[1] == -1:
            statusText = "Equipment inspection\nDevice is NOT ready!\n\n\n"
        self.buttons.append(QPushButton(statusText))
        self.buttons.append(QPushButton("Account settings\n\n"))

        # 右侧
        # 上
        self.layout1.addWidget(self.label_1, 0, 0, 1, 3, Qt.AlignRight)
        self.layout1.addWidget(self.label_2, 0, 2, 1, 9, Qt.AlignCenter)

        # 下
        self.layout2.addWidget(self.buttons[0], 0, 0, 8, 3)
        self.layout2.addWidget(self.buttons[1], 0, 3, 4, 3)
        self.layout2.addWidget(self.buttons[2], 0, 6, 4, 3)
        self.layout2.addWidget(self.buttons[3], 4, 3, 4, 3)
        self.layout2.addWidget(self.buttons[4], 4, 6, 4, 3)

        # 点击响应
        self.buttons[0].clicked.connect(self.onTutorialClicked)  # type: ignore
        self.buttons[1].clicked.connect(self.onReportClicked)  # type: ignore
        self.buttons[3].clicked.connect(lambda: self.onStatusClicked())  # type: ignore
        self.buttons[4].clicked.connect(self.onConfigClicked)  # type: ignore

        self.label_2.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 80px;
            font-weight: bold } ''')

        for i in range(5):
            str1 = ''' QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-weight: bold;
            width: 40px;'''
            str2 = f"font-size: 42px; height: 300px; image: url({self.pic_path}/{self.homes[i]}); "
            if i == 0:
                str2 = f"font-size: 64px; height: 700px; image: url({self.pic_path}/{self.homes[i]}); "
            str3 = '''margin: 25px;
            border-radius:20px;
            border-bottom: 8px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
            border-right: 8px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); } 
            QPushButton:hover { background: #A9A9A9; '''
            str4 = f"image: url({self.pic_path}/{self.homes[i]}); "
            self.buttons[i].setStyleSheet(str1 + str2 + str3 + str4 + "}")

    def init_UI_A(self):
        self.widget1 = QWidget()
        self.widget1.setObjectName('widget1')
        self.layout1 = QGridLayout()
        self.widget1.setLayout(self.layout1)

        self.widget2 = QWidget()
        self.widget2.setObjectName('widget2')
        self.layout2 = QGridLayout()
        self.widget2.setLayout(self.layout2)

        self.home_layout.addWidget(self.widget1, 0, 0, 3, 10)  # 上
        self.home_layout.addWidget(self.widget2, 3, 0, 12, 10)  # 下

        # 上
        self.label_1 = QLabel("")
        self.label_1.setPixmap(QPixmap(f'{self.pic_path}/{self.logo}').scaled(290, 290))
        self.label_2 = QLabel("Welcome to IRSPUI !     ")

        # 下
        self.buttons = []
        self.buttons.append(QPushButton("Running\nLogs\n\n\n\n\n\n"))
        self.buttons.append(QPushButton(f"Historical reports\ncurrently have {self.reportNum}\n\n\n"))

        lastText = f'The last login was on\n{self.lastTime}\n'
        if self.lastTime == '2024-01-01':
            lastText = 'This is the first\ntime login\n'
        self.buttons.append(QPushButton(lastText))

        statusText = "Equipment inspection\nDevice is ready\n\n\n"
        if self.computerStatus[0] == -1 or self.computerStatus[1] == -1:
            statusText = "Equipment inspection\nDevice is NOT ready!\n\n\n"
        self.buttons.append(QPushButton(statusText))
        self.buttons.append(QPushButton("System configuration\n\n"))

        # 右侧
        # 上
        self.layout1.addWidget(self.label_1, 0, 0, 1, 3, Qt.AlignRight)
        self.layout1.addWidget(self.label_2, 0, 2, 1, 9, Qt.AlignCenter)

        # 下
        self.layout2.addWidget(self.buttons[0], 0, 0, 8, 3)
        self.layout2.addWidget(self.buttons[1], 0, 3, 4, 3)
        self.layout2.addWidget(self.buttons[2], 0, 6, 4, 3)
        self.layout2.addWidget(self.buttons[3], 4, 3, 4, 3)
        self.layout2.addWidget(self.buttons[4], 4, 6, 4, 3)

        # 点击响应
        self.buttons[0].clicked.connect(self.onRunningLogClicked)  # type: ignore
        self.buttons[1].clicked.connect(self.onReportClicked)  # type: ignore
        self.buttons[3].clicked.connect(lambda: self.onStatusClicked())  # type: ignore
        self.buttons[4].clicked.connect(self.onConfigClicked)  # type: ignore

        self.label_2.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 80px;
            font-weight: bold } ''')

        for i in range(len(self.homes)):
            str1 = ''' QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-weight: bold;
            width: 40px;'''
            str2 = f"font-size: 42px; height: 300px; image: url({self.pic_path}/{self.homes[i]}); "
            if i == 0:
                str2 = f"font-size: 64px; height: 700px; image: url({self.pic_path}/{self.homes[i]}); "
            str3 = '''margin: 25px;
            border-radius:20px;
            border-bottom: 8px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
            border-right: 8px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); } 
            QPushButton:hover { background: #A9A9A9; '''
            str4 = f"image: url({self.pic_path}/{self.homes[i]}); "
            self.buttons[i].setStyleSheet(str1 + str2 + str3 + str4 + "}")

    def onTutorialClicked(self):
        self.tutorialUI = Extra_UI()
        self.tutorialUI.report_ui(f'{self.configs_path}/{self.tutorial}')
        self.tutorialUI.show()

    def onRunningLogClicked(self):
        flag = openDir('log')
        if not flag:
            self.message_warning('Open failed, please check path log!')
            logger.error('home - onRunningLogClicked - Open failed!')
        else:
            logger.info('home - onRunningLogClicked - Open successfully!')

    def onReportClicked(self):
        self.reportNum = getReportNum()
        self.buttons[1].setText(f'Historical reports\ncurrently have {self.reportNum}\n\n\n')

    def onStatusClicked(self, computerStatus: tuple = None):
        try:
            if computerStatus is None:
                self.computerStatus = getComputerStatus()
                self.updateStatusClicked.emit(self.computerStatus)  # type: ignore
            else:
                self.computerStatus = computerStatus
            if self.computerStatus[0] == -1 or self.computerStatus[1] == -1:
                self.buttons[3].setText("Equipment inspection\nDevice is NOT ready!\n\n\n")
            else:
                self.buttons[3].setText('Equipment inspection\nDevice is ready\n\n\n')
        except Exception as e:
            logger.error(f'home - onStatusClicked - {e}')

    def onConfigClicked(self):
        if self.userInfo['identity'] == 'A':
            self.openConfigClicked.emit(5)  # type: ignore
        else:
            self.openConfigClicked.emit(4)  # type: ignore

    def message_warning(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()
