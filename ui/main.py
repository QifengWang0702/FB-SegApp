# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import qtawesome
from ui.seg import seg_UI
from ui.home import home_UI
from ui.history import history_UI
from util.logger import logger
from ui.configs import configs_UI
from util.service import getComputerStatus, getUserInfo, getConfigs


# noinspection PyArgumentList
class Prenatal_UI(QMainWindow):
    updateComputerStatusClicked = pyqtSignal(tuple)
    resetClicked = pyqtSignal()

    def __init__(self):
        super(Prenatal_UI, self).__init__()

        configs = getConfigs()
        self.pic_path = configs['save']['pic']
        self.ico = configs['picture']['ico']
        self.head_path = configs['save']['head']
        self.head = configs['picture']['head']
        self.login = configs['picture']['login']

        self.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        self.setWindowTitle("Intelligent Recognition System for Prenatal Ultrasound Images")

        w = QApplication.desktop().height()
        h = int(w / 1.5)

        self.setFixedSize(w, h)

        self.computerStatus = getComputerStatus()
        self.userInfo = getUserInfo()
        if self.userInfo['identity'] == 'A':
            self.init_UI_A()
        else:
            self.init_UI_D()

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.updateComputerStatus())  # type: ignore
        self.timer.start(180000)  # 3min刷新一次

        logger.info('main - __init__ - Jump to IRSPUI successfully!')

    def init_UI_D(self):
        # 创建布局
        # 全局
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.main_layout.setSpacing(0)

        # 左侧
        self.left_widget = QWidget()
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.left_widget1 = QWidget()
        self.left_layout1 = QGridLayout()
        self.left_widget1.setLayout(self.left_layout1)

        self.left_widget2 = QWidget()  # 占位
        self.left_layout2 = QGridLayout()
        self.left_widget2.setLayout(self.left_layout2)

        self.left_widget3 = QWidget()
        self.left_layout3 = QGridLayout()
        self.left_widget3.setLayout(self.left_layout3)

        # 右侧
        self.right_widget = QWidget()
        self.right_layout = QStackedLayout()
        self.right_widget.setLayout(self.right_layout)

        # 具体布局
        self.main_layout.addWidget(self.left_widget, 0, 0, 14, 4)
        self.main_layout.addWidget(self.right_widget, 0, 4, 14, 10)

        self.left_layout.addWidget(self.left_widget1, 0, 0, 4, 2)  # 左上
        self.left_layout.addWidget(self.left_widget2, 4, 0, 8, 2)  # 左下
        self.left_layout.addWidget(self.left_widget3, 12, 0, 2, 2)  # 左下

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.left_layout.setVerticalSpacing(0)
        self.left_layout.setSpacing(0)
        self.left_layout1.setSpacing(0)

        # 创建组件
        # 左侧组件
        # 左上
        loginName = self.userInfo['loginName']
        self.left_label_1 = QLabel("")
        self.left_label_2 = QLabel("")
        self.left_label_2.setPixmap(QPixmap(f'{self.head_path}/{loginName}/{self.head}').scaled(180, 180))
        self.left_label_3 = QLabel(self.userInfo['loginName'])
        self.left_label_4 = QLabel("")

        self.left_buttons = []

        self.left_buttons.append(QPushButton(qtawesome.icon('fa.home', color='#2c3a45'), "Home"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.user', color='#2c3a45'), "Report generate"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.bars', color='#2c3a45'), "History query"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.camera', color='#2c3a45'), " Photo import  "))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.folder-open', color='#2c3a45'), " File import     "))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.cogs', color='#2c3a45'), "Account settings"))
        # self.left_buttons.append(QPushButton(qtawesome.icon('fa.bars',color='#2c3a45'),"User administration"))
        # self.left_buttons[5].setObjectName('left_button_4')

        # 左下
        MemoryText = f"Memory: {self.computerStatus[0]}%"
        if self.computerStatus[0] == -1:
            MemoryText = f"Memory: Error!"
        CPUText = f"CPU: {self.computerStatus[1]}%"
        if self.computerStatus[1] == -1:
            CPUText = f"CPU: Error!"
        GPUtext = f'GPU: {self.computerStatus[2]}%'
        if self.computerStatus[2] == 'None GPU':
            GPUtext = f'GPU: {self.computerStatus[2]}'
        self.left_label_5 = QLabel(MemoryText)
        self.left_label_6 = QLabel(CPUText)

        self.left_label_7 = QLabel(GPUtext)

        # 右侧组件
        self.home = home_UI(self.computerStatus)
        self.photo = seg_UI('photo')
        self.file = seg_UI('file')
        self.history = history_UI('pregnant')
        self.configs = configs_UI()

        self.right_layout.addWidget(self.home)
        self.right_layout.addWidget(self.photo)
        self.right_layout.addWidget(self.file)
        self.right_layout.addWidget(self.history)
        self.right_layout.addWidget(self.configs)

        # 组件布局位置
        # 左侧
        # 左上
        self.left_layout1.addWidget(self.left_label_1, 0, 0, 1, 3)
        self.left_layout1.addWidget(self.left_label_2, 1, 0, 2, 3, Qt.AlignCenter)
        self.left_layout1.addWidget(self.left_label_3, 3, 0, 1, 3, Qt.AlignCenter)
        self.left_layout1.addWidget(self.left_label_4, 4, 0, 1, 3)

        self.left_layout1.addWidget(self.left_buttons[0], 5, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[1], 8, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[3], 11, 0, 1, 3, Qt.AlignRight)
        self.left_layout1.addWidget(self.left_buttons[4], 12, 0, 1, 3, Qt.AlignRight)
        self.left_layout1.addWidget(self.left_buttons[2], 13, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[5], 16, 0, 3, 3)

        # 左下
        self.left_layout3.addWidget(self.left_label_5, 0, 0, 1, 3)
        self.left_layout3.addWidget(self.left_label_6, 1, 0, 2, 3)
        self.left_layout3.addWidget(self.left_label_7, 3, 0, 1, 3)

        # 去除边界空行
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout1.setContentsMargins(0, 0, 0, 0)
        self.left_layout2.setContentsMargins(0, 0, 0, 0)
        # self.left_layout3.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        # 点击响应
        self.left_buttons[0].clicked.connect(lambda: self.onClicked(0))  # type: ignore
        self.left_buttons[1].clicked.connect(lambda: self.onClicked(1))  # type: ignore
        self.left_buttons[2].clicked.connect(lambda: self.onClicked(3))  # type: ignore
        self.left_buttons[3].clicked.connect(lambda: self.onClicked(1))  # type: ignore
        self.left_buttons[4].clicked.connect(lambda: self.onClicked(2))  # type: ignore
        self.left_buttons[5].clicked.connect(lambda: self.onClicked(4))  # type: ignore
        self.home.openConfigClicked.connect(self.onClicked)
        self.home.updateStatusClicked.connect(self.updateComputerStatus)
        self.file.updateDataClicked.connect(self.history.updateStatus)
        self.photo.updateDataClicked.connect(self.history.updateStatus)
        self.configs.changeUserInfoClicked.connect(self.changeUserInfo)
        self.updateComputerStatusClicked.connect(self.home.onStatusClicked)  # type: ignore

        # 改变样式
        # 左侧
        self.left_widget.setStyleSheet(''' *{ background-color: #DCDCDC; }
        QLabel { font-size: 30px;
        font-family: '微软雅黑';
        font-weight: bold; }
        QPushButton {
        border: none;
        font-size: 30px;
        text-align: left;
        padding-left: 30px;
        height: 70px;
        font-family: 'Times New Roman'; }
        QPushButton:hover { background: #F5F5F5; } ''')

        self.left_widget3.setStyleSheet(''' QLabel { font-size: 25px;
                font-family: 'Times New Roman';
                font-weight: bold } ''')

        self.left_label_2.setStyleSheet('''border-width: 10px;
            border-radius:20px;
            border-style: solid;
            border-color: #666666;
            background-color: rgb(255, 255, 255);''')

        self.left_buttons[0].setStyleSheet("QPushButton { background-color: #F5F5F5; }")

        self.right_widget.setStyleSheet(''' *{ background-color: #F5F5F5; } ''')

    def init_UI_A(self):
        # 创建布局
        # 全局
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.main_layout.setSpacing(0)

        # 左侧
        self.left_widget = QWidget()
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.left_widget1 = QWidget()
        self.left_layout1 = QGridLayout()
        self.left_widget1.setLayout(self.left_layout1)

        self.left_widget2 = QWidget()  # 占位
        self.left_layout2 = QGridLayout()
        self.left_widget2.setLayout(self.left_layout2)

        self.left_widget3 = QWidget()
        self.left_layout3 = QGridLayout()
        self.left_widget3.setLayout(self.left_layout3)

        # 右侧
        self.right_widget = QWidget()
        self.right_layout = QStackedLayout()
        self.right_widget.setLayout(self.right_layout)

        # 具体布局
        self.main_layout.addWidget(self.left_widget, 0, 0, 14, 4)
        self.main_layout.addWidget(self.right_widget, 0, 4, 14, 10)

        self.left_layout.addWidget(self.left_widget1, 0, 0, 4, 2)  # 左上
        self.left_layout.addWidget(self.left_widget2, 4, 0, 8, 2)  # 左下
        self.left_layout.addWidget(self.left_widget3, 12, 0, 2, 2)  # 左下

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.left_layout.setVerticalSpacing(0)
        self.left_layout.setSpacing(0)
        self.left_layout1.setSpacing(0)

        # 创建组件
        # 左侧组件
        # 左上
        loginName = self.userInfo['loginName']
        self.left_label_1 = QLabel("")
        self.left_label_2 = QLabel("")
        self.left_label_2.setPixmap(QPixmap(f'{self.head_path}/{loginName}/{self.head}').scaled(180, 180))
        self.left_label_3 = QLabel(self.userInfo['loginName'])
        self.left_label_4 = QLabel("")

        self.left_buttons = []

        self.left_buttons.append(QPushButton(qtawesome.icon('fa.home', color='#2c3a45'), "Home"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.user', color='#2c3a45'), "Report generate"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.bars', color='#2c3a45'), "History query"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.camera', color='#2c3a45'), " Photo import  "))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.folder-open', color='#2c3a45'), " File import     "))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.bars', color='#2c3a45'), "User query"))
        self.left_buttons.append(QPushButton(qtawesome.icon('fa.cogs', color='#2c3a45'), "System configuration"))
        # self.left_buttons.append(QPushButton(qtawesome.icon('fa.bars',color='#2c3a45'),"User administration"))
        # self.left_buttons[5].setObjectName('left_button_4')

        # 左下
        MemoryText = f"Memory: {self.computerStatus[0]}%"
        if self.computerStatus[0] == -1:
            MemoryText = f"Memory: Error!"
        CPUText = f"CPU: {self.computerStatus[1]}%"
        if self.computerStatus[1] == -1:
            CPUText = f"CPU: Error!"
        GPUtext = f'GPU: {self.computerStatus[2]}%'
        if self.computerStatus[2] == 'None GPU':
            GPUtext = f'GPU: {self.computerStatus[2]}'
        self.left_label_5 = QLabel(MemoryText)
        self.left_label_6 = QLabel(CPUText)

        self.left_label_7 = QLabel(GPUtext)

        # 右侧组件
        self.home = home_UI(self.computerStatus)
        self.photo = seg_UI('photo')
        self.file = seg_UI('file')
        self.history = history_UI('pregnant')
        self.user = history_UI('doctor')
        self.configs = configs_UI()

        self.right_layout.addWidget(self.home)
        self.right_layout.addWidget(self.photo)
        self.right_layout.addWidget(self.file)
        self.right_layout.addWidget(self.history)
        self.right_layout.addWidget(self.user)
        self.right_layout.addWidget(self.configs)

        # 组件布局位置
        # 左侧
        # 左上
        self.left_layout1.addWidget(self.left_label_1, 0, 0, 1, 3)
        self.left_layout1.addWidget(self.left_label_2, 1, 0, 2, 3, Qt.AlignCenter)
        self.left_layout1.addWidget(self.left_label_3, 3, 0, 1, 3, Qt.AlignCenter)
        self.left_layout1.addWidget(self.left_label_4, 4, 0, 1, 3)

        self.left_layout1.addWidget(self.left_buttons[0], 5, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[1], 8, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[3], 11, 0, 1, 3, Qt.AlignRight)
        self.left_layout1.addWidget(self.left_buttons[4], 12, 0, 1, 3, Qt.AlignRight)
        self.left_layout1.addWidget(self.left_buttons[2], 13, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[5], 16, 0, 3, 3)
        self.left_layout1.addWidget(self.left_buttons[6], 19, 0, 3, 3)

        # 左下
        self.left_layout3.addWidget(self.left_label_5, 0, 0, 1, 3)
        self.left_layout3.addWidget(self.left_label_6, 1, 0, 2, 3)
        self.left_layout3.addWidget(self.left_label_7, 3, 0, 1, 3)

        # 去除边界空行
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout1.setContentsMargins(0, 0, 0, 0)
        self.left_layout2.setContentsMargins(0, 0, 0, 0)
        # self.left_layout3.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        # 点击响应
        self.left_buttons[0].clicked.connect(lambda: self.onClicked(0))  # type: ignore
        self.left_buttons[1].clicked.connect(lambda: self.onClicked(1))  # type: ignore
        self.left_buttons[2].clicked.connect(lambda: self.onClicked(3))  # type: ignore
        self.left_buttons[3].clicked.connect(lambda: self.onClicked(1))  # type: ignore
        self.left_buttons[4].clicked.connect(lambda: self.onClicked(2))  # type: ignore
        self.left_buttons[5].clicked.connect(lambda: self.onClicked(4))  # type: ignore
        self.left_buttons[6].clicked.connect(lambda: self.onClicked(5))  # type: ignore
        self.resetClicked.connect(self.photo.onResetClicked)  # type: ignore
        self.resetClicked.connect(self.file.onResetClicked)  # type: ignore
        self.home.openConfigClicked.connect(self.onClicked)
        self.home.updateStatusClicked.connect(self.updateComputerStatus)
        self.file.updateDataClicked.connect(self.history.updateStatus)
        self.photo.updateDataClicked.connect(self.history.updateStatus)
        self.file.updateDataClicked.connect(self.home.onReportClicked)
        self.photo.updateDataClicked.connect(self.home.onReportClicked)
        self.configs.changeUserInfoClicked.connect(self.changeUserInfo)
        self.updateComputerStatusClicked.connect(self.home.onStatusClicked)  # type: ignore

        # 改变样式
        # 左侧
        self.left_widget.setStyleSheet(''' *{ background-color: #DCDCDC; }
        QLabel { font-size: 30px;
        font-family: '微软雅黑';
        font-weight: bold; }
        QPushButton {
        border: none;
        font-size: 30px;
        text-align: left;
        padding-left: 30px;
        height: 70px;
        font-family: 'Times New Roman'; }
        QPushButton:hover { background: #F5F5F5; } ''')

        self.left_widget3.setStyleSheet(''' QLabel { font-size: 25px;
                font-family: 'Times New Roman';
                font-weight: bold } ''')

        self.left_label_2.setStyleSheet('''border-width: 10px;
            border-radius:20px;
            border-style: solid;
            border-color: #666666;
            background-color: rgb(255, 255, 255);''')

        self.left_buttons[0].setStyleSheet("QPushButton { background-color: #F5F5F5; }")

        self.right_widget.setStyleSheet(''' *{ background-color: #F5F5F5; } ''')

    def onClicked(self, index):
        dic = {
            0: self.left_buttons[0],
            1: self.left_buttons[3],
            2: self.left_buttons[4],
            3: self.left_buttons[2],
            4: self.left_buttons[5],
            5: self.left_buttons[-1]
        }
        self.right_layout.setCurrentIndex(index)
        for butt in self.left_buttons:
            butt.setStyleSheet("QPushButton { background-color: #DCDCDC; } QPushButton:hover { background: #F5F5F5; } ")
        button = dic[index]
        button.setStyleSheet("QPushButton { background-color: #F5F5F5; }")
        if self.file.root_path != '' or self.photo.root_path != '':
            self.resetClicked.emit()  # type: ignore

    def updateComputerStatus(self, computerStatus: tuple = None):
        try:
            if computerStatus is None:
                self.computerStatus = getComputerStatus()
                self.updateComputerStatusClicked.emit(self.computerStatus)  # type: ignore
            else:
                self.computerStatus = computerStatus
            MemoryText = f"Memory: {self.computerStatus[0]}%"
            if self.computerStatus[0] == -1:
                MemoryText = f"Memory: Error!"
            CPUText = f"CPU: {self.computerStatus[1]}%"
            if self.computerStatus[1] == -1:
                CPUText = f"CPU: Error!"
            GPUtext = f'GPU: {self.computerStatus[2]}%'
            if self.computerStatus[2] == 'None GPU':
                GPUtext = f'GPU: {self.computerStatus[2]}'
            self.left_label_5.setText(MemoryText)
            self.left_label_6.setText(CPUText)
            self.left_label_7.setText(GPUtext)
        except Exception as e:
            logger.error(f'main - updateComputerStatus - {e}')

    def changeUserInfo(self):
        self.userInfo = getUserInfo()
        loginName = self.userInfo['loginName']
        self.left_label_3.setText(loginName)
        self.left_label_2.setPixmap(QPixmap(f'{self.head_path}/{loginName}/{self.head}').scaled(180, 180))
