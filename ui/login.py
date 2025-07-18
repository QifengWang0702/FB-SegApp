import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
# -*- coding: UTF-8 -*-
import qtawesome
from util.service import loadConfigs, getConfigs
from ui.main import Prenatal_UI
from util.logger import logger
from util.service import login
from util.database import get_db_path, init_database

loadConfigs('./configs/configs.yml')
configs = getConfigs()
get_db_path(os.path.join(configs['save']['configs'], configs['database']['path']))
init_database()


# noinspection PyArgumentList
class Login_UI(QMainWindow):
    def __init__(self):
        super(Login_UI, self).__init__()
        self.pic_path = configs['save']['pic']
        self.ico = configs['picture']['ico']
        self.cover = configs['picture']['cover']
        self.login = configs['picture']['login']

        self.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        self.setWindowTitle("IRSPUI Login")

        self.w = int(QApplication.desktop().height() / 2)
        self.h = int(self.w / 1.5)
        # self.w = 900
        # self.h = int(self.w / 1.5)
        self.setFixedSize(self.w, self.h)

        self.init_UI()

    def init_UI(self):
        self.cover_label = QLabel(self)
        self.cover_label.setFixedSize(self.w, int(self.h / 3))
        self.cover_label.setPixmap(QPixmap(f'{self.pic_path}/{self.cover}').scaled(self.w, int(self.h / 3)))
        self.user_label = QLabel(self)
        self.user_label.setFixedSize(120, 120)
        self.user_label.setPixmap(QPixmap(f'{self.pic_path}/{self.login}').scaled(100, 100))
        self.user_label.setAutoFillBackground(True)
        self.error_label = QLabel(self)
        self.error_label.setFixedSize(300, 20)

        self.user_button = QPushButton(qtawesome.icon('fa.user-circle-o', color='#2c3a45'), '', self)
        self.user_button.setFlat(True)
        self.user_button.setEnabled(False)
        self.password_button = QPushButton(qtawesome.icon('fa.lock', color='#2c3a45'), '', self)
        self.password_button.setFlat(True)
        self.password_button.setEnabled(False)
        self.login_button = QPushButton(qtawesome.icon('fa.sign-in', color='#2c3a45'), '', self)
        self.login_button.setText('login')
        self.login_button.setFixedSize(130, 50)

        self.user_edit = QLineEdit(self)
        self.user_edit.setFixedSize(300, 40)
        self.password_edit = QLineEdit(self)
        self.password_edit.setFixedSize(300, 40)
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.cover_label.move(0, 0)
        self.user_label.move(390, 150)
        self.error_label.move(310, 400)
        self.user_button.move(230, 305)
        self.password_button.move(230, 355)
        self.user_edit.move(310, 300)
        self.password_edit.move(310, 350)
        self.login_button.move(380, 450)

        self.login_button.clicked.connect(self.onClicked)  # type: ignore

        self.user_label.setStyleSheet('''border-width: 10px;
            border-radius:20px;
            border-style: solid;
            border-color: #6495ED;
            background-color: rgb(255, 255, 255);''')
        self.login_button.setStyleSheet('''QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-weight: bold;
            border-radius:20px; }
            QPushButton:hover { background: #A9A9A9; }''')

    def onClicked(self):
        try:
            logger.info('login - onClicked - login in!')
            if login(self.user_edit.text(), self.password_edit.text()):
                self.error_label.setText('')
                self.main = Prenatal_UI()
                self.main.show()
                self.close()
            else:
                self.error_label.setText('Username or password error!')
                self.error_label.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                font-size: 20px;
                color: rgb(255, 0, 0) } ''')
                self.password_edit.setText('')
        except Exception as e:
            self.message_warning(f'Login error! Please contact administrator!\nError: {e}')
            logger.error(f'login - onClicked - {e}')

    def message_warning(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()
