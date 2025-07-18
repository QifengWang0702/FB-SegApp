# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import qtawesome
from util.service import *
from util.logger import logger


# noinspection PyArgumentList
class configs_UI(QWidget):
    changeUserInfoClicked = pyqtSignal()

    def __init__(self):
        super(configs_UI, self).__init__()

        self.configs_layout = QGridLayout()
        self.setLayout(self.configs_layout)
        self.userInfo = getUserInfo()
        self.infoList = getUpdateAble('doctor')
        configs = getConfigs()
        self.pic_path = configs['save']['pic']
        self.head_path = configs['save']['head']
        self.configs_path = configs['save']['configs']
        self.head = configs['picture']['head']
        self.ico = configs['picture']['ico']

        # 用户头像路径
        self.user_path = ''

        if self.userInfo['identity'] == 'A':
            self.init_UI_A()
        else:
            self.init_UI_D()

    def init_UI_D(self):
        self.up_widget = QWidget()
        self.up_layout = QGridLayout()
        self.up_widget.setLayout(self.up_layout)

        self.null_widget = QWidget()
        self.null_layout = QGridLayout()
        self.null_widget.setLayout(self.null_layout)

        self.left_widget = QWidget()
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QWidget()
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.down_widget = QWidget()
        self.down_layout = QGridLayout()
        self.down_widget.setLayout(self.down_layout)

        self.configs_layout.addWidget(self.up_widget, 0, 0, 10, 30)
        self.configs_layout.addWidget(self.null_widget, 10, 0, 30, 2)
        self.configs_layout.addWidget(self.left_widget, 10, 2, 30, 14)
        self.configs_layout.addWidget(self.right_widget, 10, 16, 30, 14)
        self.configs_layout.addWidget(self.down_widget, 40, 0, 5, 30)

        loginName = self.userInfo['loginName']
        self.label_1 = QLabel("")
        self.label_1.setPixmap(QPixmap(f'{self.head_path}/{loginName}/{self.head}').scaled(180, 180))
        self.labels = []
        self.valueEdits = []
        for key, value in self.userInfo.items():
            if key == 'operation':
                continue
            self.labels.append(QLabel(f"{key}:"))
            self.valueEdits.append(QLineEdit(f"{value}"))
            self.valueEdits[-1].setReadOnly(True)
            self.valueEdits[-1].setFixedWidth(330)
        self.labels.append(QLabel(f"Feedback:"))
        self.valueEdits.append(QLineEdit())
        self.valueEdits[-1].setFixedWidth(330)

        self.buttons = []
        for i in range(3):
            if i < 2:
                self.valueEdits[(i + 1) * 2].setEchoMode(QLineEdit.Password)
            name = 'fa.eye-slash'
            if i == 2:
                name = 'fa.external-link-square'
            self.buttons.append(QPushButton(qtawesome.icon(name, color='#2c3a45'), ''))
            self.buttons[-1].setFixedSize(30, 30)
            self.buttons[-1].setFlat(True)
        self.button_1 = QPushButton(qtawesome.icon('fa.refresh', color='#2c3a45'), 'Change avatar')
        self.button_1.setFixedSize(220, 70)
        self.button_2 = QPushButton(qtawesome.icon('fa.pencil-square-o', color='#2c3a45'), 'Update info')
        self.button_2.setFixedSize(200, 70)

        # for i in range(len(self.buttons)):
        #     print(i)
        self.buttons[0].clicked.connect(lambda: self.onVisibleClicked(0))  # type: ignore
        self.buttons[1].clicked.connect(lambda: self.onVisibleClicked(1))  # type: ignore
        self.buttons[2].clicked.connect(self.onFeedbackClicked)  # type: ignore
        self.button_1.clicked.connect(self.onChangeClicked)  # type: ignore
        self.button_2.clicked.connect(self.onUpdateClicked)  # type: ignore

        self.up_layout.addWidget(self.label_1, 0, 5, 5, 5, Qt.AlignCenter)
        self.up_layout.addWidget(self.button_1, 5, 5, 5, 5, Qt.AlignCenter)
        self.down_layout.addWidget(self.button_2, 0, 5, 5, 5, Qt.AlignCenter)
        for i in range(len(self.valueEdits)):
            if i % 2 == 0:
                self.left_layout.addWidget(self.labels[i], i * 3, 0, 3, 3)
                self.left_layout.addWidget(self.valueEdits[i], i * 3, 3, 3, 9)
            else:
                self.right_layout.addWidget(self.labels[i], i * 3 - 3, 0, 3, 3)
                self.right_layout.addWidget(self.valueEdits[i], i * 3 - 3, 3, 3, 9)
            if i == 2 or i == 4:
                self.left_layout.addWidget(self.buttons[int(i / 2) - 1], i * 3, 12, 3, 3)
            if i == 9:
                self.right_layout.addWidget(self.buttons[-1], i * 3 - 3, 12, 3, 3)

        self.null_layout.setContentsMargins(20, 20, 20, 20)
        self.left_layout.setContentsMargins(20, 20, 20, 20)
        self.right_layout.setContentsMargins(20, 20, 20, 20)

        self.setStyleSheet(''' *{ background-color: #DCDCDC; }
                QLabel { font-size: 35px;
                font-family: 'Times New Roman' } 
                QLineEdit { font-family: 'Times New Roman';
                font-size: 35px;
                border: none;
                background-color: #DCDCDC; }''')

        self.left_widget.setStyleSheet(''' QPushButton { border: none; } ''')

        self.up_widget.setStyleSheet(''' *{ background-color: #F5F5F5; }
                    QLabel {border-width: 10px;
                    border-radius:20px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: rgb(255, 255, 255); }
                    QPushButton { background-color: #D3D3D3;
                    font-family: 'Times New Roman';
                    font-size: 26px;
                    font-weight: bold;
                    border-radius: 20px;
                    height: 100px;
                    border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
                    border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
                    QPushButton:hover { background: #A9A9A9; } ''')

        self.down_widget.setStyleSheet(''' *{ background-color: #F5F5F5; }
                    QPushButton { background-color: #D3D3D3;
                    font-family: 'Times New Roman';
                    font-size: 26px;
                    font-weight: bold;
                    border-radius: 20px;
                    height: 100px;
                    border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
                    border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
                    QPushButton:hover { background: #A9A9A9; } ''')

        self.valueEdits[-1].setStyleSheet("QLineEdit { background-color: #FFFFFF; } ")
        self.buttons[-1].setStyleSheet('''QPushButton { background-color: #D3D3D3;
                        border: none; } 
                        QPushButton:hover { background: #A9A9A9; }''')

    def init_UI_A(self):
        self.up_widget = QWidget()
        self.up_layout = QGridLayout()
        self.up_widget.setLayout(self.up_layout)

        self.null_widget = QWidget()
        self.null_layout = QGridLayout()
        self.null_widget.setLayout(self.null_layout)

        self.left_widget = QWidget()
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QWidget()
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.down_widget = QWidget()
        self.down_layout = QGridLayout()
        self.down_widget.setLayout(self.down_layout)

        self.configs_layout.addWidget(self.up_widget, 0, 0, 10, 30)
        self.configs_layout.addWidget(self.null_widget, 10, 0, 30, 2)
        self.configs_layout.addWidget(self.left_widget, 10, 2, 30, 14)
        self.configs_layout.addWidget(self.right_widget, 10, 16, 30, 14)
        self.configs_layout.addWidget(self.down_widget, 40, 0, 5, 30)

        loginName = self.userInfo['loginName']
        self.label_1 = QLabel("")
        self.label_1.setPixmap(QPixmap(f'{self.head_path}/{loginName}/{self.head}').scaled(180, 180))
        self.labels = []
        self.valueEdits = []
        for key, value in self.userInfo.items():
            if key == 'operation':
                continue
            self.labels.append(QLabel(f"{key}:"))
            self.valueEdits.append(QLineEdit(f"{value}"))
            self.valueEdits[-1].setReadOnly(True)
            self.valueEdits[-1].setFixedWidth(330)

        self.buttons = []
        for i in range(2):
            self.valueEdits[(i + 1) * 2].setEchoMode(QLineEdit.Password)
            self.buttons.append(QPushButton(qtawesome.icon('fa.eye-slash', color='#2c3a45'), ''))
            self.buttons[-1].setFixedSize(30, 30)
            self.buttons[-1].setFlat(True)
        self.button_1 = QPushButton(qtawesome.icon('fa.refresh', color='#2c3a45'), 'Change avatar')
        self.button_1.setFixedSize(220, 70)
        self.button_2 = QPushButton(qtawesome.icon('fa.pencil-square-o', color='#2c3a45'), 'Update info')
        self.button_2.setFixedSize(200, 70)
        self.button_3 = QPushButton(qtawesome.icon('fa.cog', color='#2c3a45'), 'Update configs')
        self.button_3.setFixedSize(250, 70)

        # for i in range(len(self.buttons)):
        #     print(i)
        self.buttons[0].clicked.connect(lambda: self.onVisibleClicked(0))  # type: ignore
        self.buttons[1].clicked.connect(lambda: self.onVisibleClicked(1))  # type: ignore
        self.button_1.clicked.connect(self.onChangeClicked)  # type: ignore
        self.button_2.clicked.connect(self.onUpdateClicked)  # type: ignore
        self.button_3.clicked.connect(self.onUpdateConfigsClicked)  # type: ignore

        self.up_layout.addWidget(self.label_1, 0, 5, 5, 5, Qt.AlignCenter)
        self.up_layout.addWidget(self.button_1, 5, 5, 5, 5, Qt.AlignCenter)
        self.down_layout.addWidget(self.button_2, 0, 5, 5, 5, Qt.AlignCenter)
        for i in range(len(self.valueEdits)):
            if i % 2 == 0:
                self.left_layout.addWidget(self.labels[i], i * 3, 0, 3, 3)
                self.left_layout.addWidget(self.valueEdits[i], i * 3, 3, 3, 9)
            else:
                self.right_layout.addWidget(self.labels[i], i * 3 - 3, 0, 3, 3)
                self.right_layout.addWidget(self.valueEdits[i], i * 3 - 3, 3, 3, 9)
            if i == 2 or i == 4:
                self.left_layout.addWidget(self.buttons[int(i / 2) - 1], i * 3, 12, 3, 3)
        self.right_layout.addWidget(self.button_3, 24, 2, 3, 9)

        self.null_layout.setContentsMargins(20, 20, 20, 20)
        self.left_layout.setContentsMargins(20, 20, 20, 20)
        self.right_layout.setContentsMargins(20, 20, 20, 20)

        self.setStyleSheet(''' *{ background-color: #DCDCDC; }
                QLabel { font-size: 35px;
                font-family: 'Times New Roman' } 
                QLineEdit { font-family: 'Times New Roman';
                font-size: 35px;
                border: none;
                background-color: #DCDCDC; }''')

        self.left_widget.setStyleSheet(''' QPushButton { border: none; } ''')

        self.up_widget.setStyleSheet(''' *{ background-color: #F5F5F5; }
                    QLabel {border-width: 10px;
                    border-radius:20px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: rgb(255, 255, 255); }
                    QPushButton { background-color: #D3D3D3;
                    font-family: 'Times New Roman';
                    font-size: 26px;
                    font-weight: bold;
                    border-radius: 20px;
                    height: 100px;
                    border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
                    border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
                    QPushButton:hover { background: #A9A9A9; } ''')

        self.down_widget.setStyleSheet(''' *{ background-color: #F5F5F5; }
                    QPushButton { background-color: #D3D3D3;
                    font-family: 'Times New Roman';
                    font-size: 26px;
                    font-weight: bold;
                    border-radius: 20px;
                    height: 100px;
                    border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
                    border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
                    QPushButton:hover { background: #A9A9A9; } ''')

        self.button_3.setStyleSheet('''QPushButton { background-color: #C0C0C0;
                    font-family: 'Times New Roman';
                    font-size: 26px;
                    font-weight: bold;
                    border-radius: 20px;
                    height: 100px; }
                    QPushButton:hover { background: #A9A9A9; } ''')

    def onVisibleClicked(self, index):
        try:
            if self.valueEdits[(index + 1) * 2].echoMode() == QLineEdit.Normal:
                self.buttons[index].setIcon(qtawesome.icon('fa.eye-slash', color='#2c3a45'))
                self.valueEdits[(index + 1) * 2].setEchoMode(QLineEdit.Password)
            else:
                self.buttons[index].setIcon(qtawesome.icon('fa.eye', color='#2c3a45'))
                self.valueEdits[(index + 1) * 2].setEchoMode(QLineEdit.Normal)
        except Exception as e:
            logger.error(f'configs - onVisibleClicked - {e}')

    def onChangeClicked(self):
        try:
            absolute_path = QFileDialog.getOpenFileName(self, 'Open file',
                                                        '.', "image files (*.jpg;*.jpeg;*.png)")
            if absolute_path[0] != '':
                self.user_path = changeUserHead(absolute_path[0], self.userInfo['loginName'])
                logger.info(f'configs - onChangeClicked - Image path: {absolute_path[0]}')
            else:
                logger.info(f'configs - onChangeClicked - No image path!')
            if self.user_path != '':
                logger.info(f'configs - onChangeClicked - Display image: {self.user_path}')
                self.label_1.setPixmap(QPixmap(self.user_path).scaled(180, 180))
                self.changeUserInfoClicked.emit()  # type: ignore
            else:
                if absolute_path[0] != '':
                    self.message_warning('Change user head failed!')
                logger.info(f'configs - onChangeClicked - No image display!')
        except Exception as e:
            logger.error(f'configs - onChangeClicked - {e}')
            self.message_warning('Change user head failed!')
            self.user_path = ''

    def onUpdateClicked(self):
        try:
            if self.button_2.text() == 'OK':
                keys = []
                values = []
                loginName = self.userInfo['loginName']
                cardId = self.userInfo['cardId']
                for i in range(len(self.valueEdits) - 1):
                    if self.labels[i].text()[:-1] in self.infoList:
                        judge = False
                        if 'loginName' in self.labels[i].text() and loginName != self.valueEdits[i].text():
                            judge = True
                        if 'cardId' in self.labels[i].text() and cardId != self.valueEdits[i].text():
                            judge = True
                        flag, tap, warn = isLegal(self.labels[i].text()[:-1], self.valueEdits[i].text(), judge)
                        if not flag:
                            logger.error(f'configs - onUpdateClicked - {tap}')
                            if warn != '':
                                tap = tap + '\n' + warn
                            self.message_warning(tap)
                            return

                        keys.append(self.labels[i].text()[:-1])
                        values.append(self.valueEdits[i].text())

                if not updateInfo('doctor', self.userInfo['userId'], keys, values):
                    logger.error(f'configs - onUpdateClicked - Update error!')
                    updateInfo('doctor', self.userInfo['userId'], self.userInfo.keys(), self.userInfo.values())

                for i in range(len(self.valueEdits) - 1):
                    if self.labels[i].text()[:-1] in self.infoList:
                        self.valueEdits[i].setReadOnly(True)
                        self.valueEdits[i].setStyleSheet("QLineEdit { background-color: #DCDCDC; }")

                        isEncod = i % 2 == 0 and (i == 2 or i == 4)
                        if isEncod and self.valueEdits[i].echoMode() == QLineEdit.Normal:
                            self.valueEdits[i].setEchoMode(QLineEdit.Password)
                            self.buttons[int(i / 2) - 1].setEnabled(True)
                            self.buttons[int(i / 2) - 1].setIcon(qtawesome.icon('fa.eye-slash', color='#2c3a45'))
                self.button_2.setIcon(qtawesome.icon('fa.pencil-square-o', color='#2c3a45'))
                self.button_2.setText('Update info')

                self.userInfo = getUserInfo()
                self.changeUserInfoClicked.emit()  # type: ignore
            else:
                for i in range(len(self.valueEdits) - 1):
                    if self.labels[i].text()[:-1] in self.infoList:
                        self.valueEdits[i].setReadOnly(False)
                        self.valueEdits[i].setStyleSheet("QLineEdit { background-color: #F5F5F5; }")
                        if self.valueEdits[i].echoMode() == QLineEdit.Password:
                            self.valueEdits[i].setEchoMode(QLineEdit.Normal)
                            self.buttons[int(i / 2) - 1].setEnabled(False)
                            self.buttons[int(i / 2) - 1].setIcon(qtawesome.icon('fa.eye', color='#2c3a45'))
                self.button_2.setIcon(qtawesome.icon('fa.check-circle', color='#2c3a45'))
                self.button_2.setText('OK')
            if self.userInfo['identity'] == 'D':
                self.buttons[-1].setIcon(qtawesome.icon('fa.external-link-square', color='#2c3a45'))
        except Exception as e:
            logger.error(f'configs - onUpdateClicked - {e}')

    def onFeedbackClicked(self):
        if self.valueEdits[-1].text() == '':
            self.message_warning('Please enter your feedback!')
            return
        logger.error(self.userInfo['loginName'] + ': ' + self.valueEdits[-1].text())
        self.valueEdits[-1].setText('')
        self.message_warning('Feedback successfully!')

    def onUpdateConfigsClicked(self):
        flag = openDir(self.configs_path)
        if not flag:
            self.message_warning('Open failed, please check path configs!')
            logger.error('home - onUpdateConfigsClicked - Open failed!')
        else:
            logger.info('home - onUpdateConfigsClicked - Open successfully!')

    def message_warning(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()
