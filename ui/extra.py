# -*- coding: UTF-8 -*-
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QPen
from PyQt5.QtCore import QTimer, QRect, Qt, pyqtSignal
import qtawesome
import fitz
from util.service import *
from util.logger import logger


class CLabel(QLabel):
    def __init__(self, parent=None):
        super(CLabel, self).__init__(parent)
        self.x0 = 28
        self.y0 = 19
        self.x1 = 972
        self.y1 = 681
        self.lab = QLabel(self)

        self.lab.setText("Please accurately place the \nultrasound image into the green box")
        self.lab.setStyleSheet(''' QLabel { color: rgba(0, 255, 0, 130);
                               font-size: 48px;
                               font-family: 'Times New Roman';
                               background: transparent; } ''')
        self.lab.setAlignment(Qt.AlignCenter)
        x = int(self.x0 + (self.x1 - self.x0) / 2)
        y = int(self.y0 + (self.y1 - self.y0) / 2)
        # print(self.lab.size())
        self.lab.move(x - 345, y - 70)

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
        painter.drawRect(rect)


# 数据居中显示
class CenterDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = QStyledItemDelegate.sizeHint(self, option, index)
        size.setHeight(40)  # 设置行高度为30
        return size

    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        QStyledItemDelegate.paint(self, painter, option, index)


class UserButtonDelegate(QItemDelegate):
    userFeedback = pyqtSignal(int)
    userUpdate = pyqtSignal(int)

    def __init__(self, parent=None):
        super(UserButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        try:
            if not self.parent().indexWidget(index):
                widget = QWidget()
                h_box_layout = QHBoxLayout()
                widget.setLayout(h_box_layout)
                if index.column() == 7:
                    button_read = QPushButton(qtawesome.icon('fa.file-pdf-o', color='#2c3a45'), '', self.parent())
                    button_read.setFixedSize(50, 50)

                    button_read.clicked.connect(lambda: self.reportViewClicked(index))  # type: ignore

                    h_box_layout.addWidget(button_read)
                    h_box_layout.setContentsMargins(0, 0, 0, 0)
                    h_box_layout.setAlignment(Qt.AlignCenter)
                    self.parent().setIndexWidget(index, widget)
                if index.column() == 8:
                    button_update = QPushButton(qtawesome.icon('fa.paint-brush', color='#2c3a45'), '', self.parent())
                    button_update.setFixedSize(50, 50)
                    button_feedback = QPushButton(qtawesome.icon('fa.external-link-square', color='#2c3a45'), '',
                                                  self.parent())
                    button_feedback.setFixedSize(50, 50)

                    button_update.clicked.connect(lambda: self.updateClicked(index))  # type: ignore
                    button_feedback.clicked.connect(lambda: self.feedbackClicked(index))  # type: ignore

                    h_box_layout.addWidget(button_update)
                    h_box_layout.addWidget(button_feedback)
                    h_box_layout.setContentsMargins(0, 0, 0, 0)
                    h_box_layout.setAlignment(Qt.AlignCenter)
                    self.parent().setIndexWidget(index, widget)
        except Exception as e:
            logger.error(f'extras - UserButtonDelegate - {e}')

    def reportViewClicked(self, index):
        self.reportUI = Extra_UI()
        self.reportUI.report_ui(index.data())
        self.reportUI.show()

    def updateClicked(self, index):
        try:
            self.userUpdate.emit(index.row())  # type: ignore
        except Exception as e:
            logger.error(f'AdminButtonDelegate - updateClicked - {e}')

    def feedbackClicked(self, index):
        try:
            self.userFeedback.emit(index.row())  # type: ignore
        except Exception as e:
            logger.error(f'UserButtonDelegate - feedbackClicked - {e}')


class AdminButtonDelegate(QItemDelegate):
    adminDelete = pyqtSignal(int)
    adminUpdate = pyqtSignal(int)

    def __init__(self, parent=None):
        super(AdminButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        try:
            if not self.parent().indexWidget(index):
                widget = QWidget()
                h_box_layout = QHBoxLayout()
                widget.setLayout(h_box_layout)
                if index.column() == 7:
                    button_read = QPushButton(qtawesome.icon('fa.file-pdf-o', color='#2c3a45'), '', self.parent())
                    button_read.setFixedSize(50, 50)

                    button_read.clicked.connect(lambda: self.reportViewClicked(index))  # type: ignore

                    h_box_layout.addWidget(button_read)
                    h_box_layout.setContentsMargins(0, 0, 0, 0)
                    h_box_layout.setAlignment(Qt.AlignCenter)
                    self.parent().setIndexWidget(index, widget)
                else:
                    button_update = QPushButton(qtawesome.icon('fa.paint-brush', color='#2c3a45'), '', self.parent())
                    button_update.setFixedSize(50, 50)
                    button_remove = QPushButton(qtawesome.icon('fa.trash', color='#2c3a45'), '', self.parent())
                    button_remove.setFixedSize(50, 50)

                    button_update.clicked.connect(lambda: self.updateClicked(index))  # type: ignore
                    button_remove.clicked.connect(lambda: self.removeClicked(index))  # type: ignore

                    h_box_layout.addWidget(button_update)
                    h_box_layout.addWidget(button_remove)
                    h_box_layout.setContentsMargins(0, 0, 0, 0)
                    h_box_layout.setAlignment(Qt.AlignCenter)
                    self.parent().setIndexWidget(index, widget)
        except Exception as e:
            logger.error(f'extras - AdminButtonDelegate - {e}')

    def reportViewClicked(self, index):
        self.reportUI = Extra_UI()
        self.reportUI.report_ui(index.data())
        self.reportUI.show()

    def updateClicked(self, index):
        try:
            self.adminUpdate.emit(index.row())  # type: ignore
        except Exception as e:
            logger.error(f'AdminButtonDelegate - updateClicked - {e}')

    def removeClicked(self, index):
        try:
            self.adminDelete.emit(index.row())  # type: ignore
        except Exception as e:
            logger.error(f'AdminButtonDelegate - removeClicked - {e}')


# noinspection PyArgumentList
class Extra_UI(QDialog):
    nameClicked = pyqtSignal(str)
    ageClicked = pyqtSignal(int)
    operateClicked = pyqtSignal(str)

    def __init__(self):
        super(Extra_UI, self).__init__()
        configs = getConfigs()
        self.pic_path = configs['save']['pic']
        self.ico = configs['picture']['ico']
        self.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))

    def info_ui(self):
        self.setWindowTitle("Get Info")
        self.resize(600, 400)
        self.error_label = QLabel(self)
        self.error_label.setFixedSize(380, 30)

        self.name_label = QLabel(self)
        self.name_label.setText('name:')
        self.age_label = QLabel(self)
        self.age_label.setText('age:')
        # self.age_label.setFlat(True)
        # self.age_label.setEnabled(False)
        self.enter_button = QPushButton(qtawesome.icon('fa.sign-in', color='#2c3a45'), 'Enter', self)
        self.enter_button.setFixedSize(130, 50)

        self.name_edit = QLineEdit(self)
        self.name_edit.setFixedSize(300, 40)
        self.age_edit = QLineEdit(self)
        self.age_edit.setFixedSize(300, 40)

        self.name_label.move(100, 110)
        self.age_label.move(110, 170)
        self.error_label.move(100, 210)
        self.name_edit.move(180, 105)
        self.age_edit.move(180, 165)
        self.enter_button.move(230, 300)

        self.enter_button.clicked.connect(self.onInfoClicked)  # type: ignore

        self.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                        font-size: 30px;
                        color: rgb(0, 0, 0) } ''')
        self.error_label.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                        font-size: 25px;
                        color: rgb(255, 0, 0) } ''')
        self.enter_button.setStyleSheet('''QPushButton { background-color: #D3D3D3;
                    font-family: 'Times New Roman';
                    font-weight: bold;
                    border-radius:20px; }
                    QPushButton:hover { background: #A9A9A9; }''')

    def onInfoClicked(self):
        try:
            name = self.name_edit.text()
            age = self.age_edit.text()
            nameFlag, nameTap, nameWarn = isLegal('name', name)
            ageFlag, ageTap, ageWarn = isLegal('age', age)
            if nameFlag and ageFlag:
                self.error_label.setText('')
                self.nameClicked.emit(name)  # type: ignore
                self.ageClicked.emit(int(age))  # type: ignore
                self.close()
            elif not nameFlag:
                self.error_label.setText(nameTap)
                self.message_warning(nameWarn)
                logger.error(f'extras - onInfoClicked -  {nameTap}')
            else:
                self.error_label.setText(ageTap)
                self.message_warning(ageWarn)
                logger.error(f'extras - onInfoClicked -  {ageTap}')
        except Exception as e:
            if len(self.name_edit.text()) > 0:
                name = self.name_edit.text()
                self.nameClicked.emit(name)  # type: ignore
                self.ageClicked.emit(-1)  # type: ignore
                self.close()
            else:
                self.error_label.setText('No name entered!')
            logger.error(f'extras - onInfoClicked -  {e}')

    def report_ui(self, report_path):
        try:
            self.setWindowTitle("Report View")
            self.resize(1100, 1350)
            self.report_label = QLabel("", self)
            self.report_label.move(100, 20)
            if not os.path.exists(report_path):
                logger.error(f'extras - report_ui - {report_path} not exist!')
                self.message_critical(f'{report_path} not exist!')
                return
            file = report_path
            doc = fitz.open(file)  # type: ignore
            page = doc.loadPage(0).getPixmap()
            format = QImage.Format_RGBA8888 if page.alpha else QImage.Format_RGB888
            image = QImage(page.samples, page.width, page.height, page.stride, format)
            self.report_label.resize(page.width * 1.5, page.height * 1.5)
            self.report_label.setScaledContents(True)
            self.report_label.setPixmap(QPixmap.fromImage(image))
            logger.info(f'extras - report_ui - open PDF successfully! path: {report_path}')
        except Exception as e:
            logger.error(f'extras - report_ui - {e}')
            self.message_critical(f'Error! Reason: {e}')

    def camera_ui(self):
        try:
            self.setWindowTitle("Camera")
            self.resize(1200, 900)
            self.cap_path = ''
            self.cameraIds = getCameraList()
            self.cameraId = 0

            self.camera_timer = QTimer(self)
            self.cap = cv2.VideoCapture(self.cameraIds[self.cameraId])

            self.camera_label = CLabel(self)
            # self.camera_label.setFixedSize(1000, 700)
            self.camera_button_1 = QPushButton(qtawesome.icon('fa.camera-retro', color='#2c3a45'), "Change Camera",
                                               self)
            self.camera_button_1.setFixedSize(300, 60)
            if len(self.cameraIds) == 1:
                self.camera_button_1.setEnabled(False)
            self.camera_button_2 = QPushButton(qtawesome.icon('fa.file-image-o', color='#2c3a45'), "Take picture", self)
            self.camera_button_2.setFixedSize(300, 60)
            # self.camera_button_2.setVisible(False)

            self.camera_timer.timeout.connect(self.cameraTimerShow)  # type: ignore
            self.camera_button_1.clicked.connect(self.onCameraClicked)  # type: ignore
            self.camera_button_2.clicked.connect(self.onPictureClicked)  # type: ignore

            self.camera_label.move(100, 50)
            self.camera_button_1.move(150, 800)
            self.camera_button_2.move(750, 800)

            self.camera_button_1.setStyleSheet(''' QPushButton { background-color: #D3D3D3;
                font-family: 'Times New Roman';
                font-size: 26px;
                font-weight: bold;
                border-radius: 20px;
                width: 60px;
                height: 30px; }
                QPushButton:hover { background: #A9A9A9; } ''')

            self.camera_button_2.setStyleSheet(''' QPushButton { background-color: #D3D3D3;
                font-family: 'Times New Roman';
                font-size: 26px;
                font-weight: bold;
                border-radius: 20px;
                width: 60px;
                height: 30px; }
                QPushButton:hover { background: #A9A9A9; } ''')

            self.camera_timer.start(40)
            self.cameraTimerShow()
        except Exception as e:
            logger.error(f'extras - camera_ui - {e}')
            self.message_critical('Get camera failed!')

    def onCameraClicked(self):
        if self.camera_button_1.text() == 'Change Camera':
            self.cameraId = (self.cameraId + 1) % len(self.cameraIds)
            self.cap = cv2.VideoCapture(self.cameraIds[self.cameraId])
            self.cameraTimerShow()
        else:
            self.camera_button_1.setIcon(qtawesome.icon('fa.camera-retro', color='#2c3a45'))
            self.camera_button_1.setText('Change Camera')
            if len(self.cameraIds) == 1:
                self.camera_button_1.setEnabled(False)
            self.camera_button_2.setIcon(qtawesome.icon('fa.file-image-o', color='#2c3a45'))
            self.camera_button_2.setText('Take picture')
            self.cap = cv2.VideoCapture(self.cameraIds[self.cameraId])
            self.camera_timer.start(40)
            self.cameraTimerShow()

    def onPictureClicked(self):
        try:
            if self.camera_button_2.text() == 'Take picture':
                if self.cap.isOpened():
                    # self.camera_button_2.setVisible(True)
                    self.camera_button_1.setIcon(qtawesome.icon('fa.file-image-o', color='#2c3a45'))
                    self.camera_button_1.setText('Take picture again')
                    self.camera_button_1.setEnabled(True)
                    self.camera_button_2.setIcon(qtawesome.icon('fa.check-circle', color='#2c3a45'))
                    self.camera_button_2.setText('OK')
                    # self.camera_button_1.move(150, 800)
                    self.camera_label.setPixmap(QPixmap.fromImage(self.camera_new))
                    self.camera_timer.stop()
                    self.cap.release()
                else:
                    logger.error(f'extras - onPictureClicked - The camera is not turned on!')
                    self.message_critical('The camera is not turned on!')
                    return
            else:
                configs = getConfigs()
                self.cap_path = configs['save']['temp']
                if os.path.exists(self.cap_path):
                    shutil.rmtree(self.cap_path)
                os.makedirs(self.cap_path, exist_ok=True)
                self.cap_path = os.path.join(configs['save']['temp'], 'camera.jpg')
                self.camera_new.save(self.cap_path)
                self.accept()
        except Exception as e:
            logger.error(f'extras - onPictureClicked - {e}')

    def cameraTimerShow(self):
        try:
            __, image = self.cap.read()
            image = cv2.resize(image, (1000, 700))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            self.camera_new = QImage(image.data, 1000, 700, QImage.Format_RGB888)
            self.camera_label.setScaledContents(True)
            self.camera_label.setPixmap(QPixmap.fromImage(self.camera_new))
        except Exception as e:
            logger.error(f'extras - cameraTimerShow - {e}')
            self.message_critical('Get camera video failed!')

    def table_ui(self, winName, tabelName, headers: list, info: list = None, id=0, report=''):
        self.setWindowTitle(winName)
        userInfo = getUserInfo()
        if userInfo['identity'] == 'A':
            self.resize(600, 700)
        else:
            self.resize(600, 400)
        self.error_label = QLabel(self)
        self.error_label.setFixedSize(450, 30)
        self.headers = headers
        self.info = info
        self.tabelName = tabelName
        self.tableId = id
        self.report = report

        if info is not None and len(info) != len(headers):
            logger.error(f'extras - table_ui - The length of info and headers not match!')
            self.message_critical('Open error!')
            self.close()
            return

        self.labels = []
        self.edits = []
        for i in range(len(headers)):
            label = QLabel(self)
            label.setText(headers[i] + ':')
            label.setAlignment(Qt.AlignCenter)
            edit = QLineEdit(self)
            if info is not None:
                edit.setText(str(info[i]))
            edit.setFixedSize(300, 40)
            label.move(60, 110 + i * 60)
            edit.move(210, 105 + i * 60)
            self.labels.append(label)
            self.edits.append(edit)

        self.enter_button = QPushButton(qtawesome.icon('fa.check-circle', color='#2c3a45'), 'OK', self)
        self.enter_button.setFixedSize(140, 50)
        self.cancel_button = QPushButton(qtawesome.icon('fa.times-circle', color='#2c3a45'), 'Cancel', self)
        self.cancel_button.setFixedSize(140, 50)

        self.error_label.move(60, 90 + len(headers) * 60)
        self.enter_button.move(120, 160 + len(headers) * 60)
        self.cancel_button.move(340, 160 + len(headers) * 60)

        self.enter_button.clicked.connect(self.onTableOKClicked)  # type: ignore
        self.cancel_button.clicked.connect(self.onCancelClicked)  # type: ignore

        self.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                        font-size: 30px;
                        color: rgb(0, 0, 0) } 
                        QPushButton { background-color: #D3D3D3;
                        font-family: 'Times New Roman';
                        font-weight: bold;
                        border-radius:20px; }
                        QPushButton:hover { background: #A9A9A9; } ''')
        self.error_label.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                        font-size: 25px;
                        color: rgb(255, 0, 0) } ''')

    def onTableOKClicked(self):
        try:
            self.error_label.setText('')
            keys = []
            values = []
            for i in range(len(self.labels)):
                judge = False
                if self.windowTitle() != 'Add':
                    if 'loginName' in self.labels[i].text() and self.info[0] != self.edits[i].text():
                        judge = True
                    if 'cardId' in self.labels[i].text() and self.info[3] != self.edits[i].text():
                        judge = True
                    if 'doctor' in self.labels[i].text() and self.info[3] != self.edits[i].text():
                        judge = True
                flag, tap, warn = isLegal(self.labels[i].text()[:-1], self.edits[i].text(), judge)
                if not flag:
                    self.error_label.setText(tap)
                    if warn != '':
                        self.message_warning(warn)
                    logger.error(f'extras - onTableOKClicked - {tap}')
                    return
                keys.append(self.labels[i].text()[:-1])
                values.append(self.edits[i].text())
            if self.windowTitle() == 'Add':
                if not addRow(self.tabelName, keys, values):
                    logger.error(f'extras - onTableOKClicked - Add failed!')
                    self.message_critical('Add failed!')
                else:
                    self.message_warning('Add successfully!')
            else:
                if self.tableId == 0:
                    logger.error(f'extras - onTableOKClicked - Id not exist!')
                    self.message_critical('Id not exist!')
                    return
                if self.tabelName == 'doctor':
                    loginName = self.info[0]
                    if not updateInfo(self.tabelName, self.tableId, keys, values, name=loginName):
                        self.message_warning('Update failed!')
                        logger.error(f'extras - onTableOKClicked - Update error!')
                        updateInfo(self.tabelName, self.tableId, self.headers, self.info, name=loginName)
                    else:
                        self.message_warning('Update successfully!')
                else:
                    if not updateInfo(self.tabelName, self.tableId, keys, values, report=self.report):
                        self.message_warning('Update failed!')
                        logger.error(f'extras - onTableOKClicked - Update error!')
                        updateInfo(self.tabelName, self.tableId, self.headers, self.info, report=self.report)
                    else:
                        self.message_warning('Update successfully!')
            self.close()
            self.operateClicked.emit(self.windowTitle())  # type: ignore
        except Exception as e:
            logger.error(f'extras - onTableOKClicked - {e}')

    def feedback_ui(self, id):
        self.setWindowTitle("Feedback")
        self.resize(600, 250)
        self.feedbackId = id
        self.error_label = QLabel(self)
        self.error_label.setFixedSize(450, 30)

        self.label = QLabel(self)
        self.label.setText('suggestion:')
        self.edit = QLineEdit(self)
        self.edit.setFixedSize(300, 40)
        self.enter_button = QPushButton(qtawesome.icon('fa.check-circle', color='#2c3a45'), 'OK', self)
        self.enter_button.setFixedSize(140, 50)
        self.cancel_button = QPushButton(qtawesome.icon('fa.times-circle', color='#2c3a45'), 'Cancel', self)
        self.cancel_button.setFixedSize(140, 50)


        self.label.move(60, 60)
        self.edit.move(210, 55)
        self.error_label.move(60, 100)
        self.enter_button.move(120, 170)
        self.cancel_button.move(340, 170)

        self.enter_button.clicked.connect(self.onFeedbackClicked)  # type: ignore
        self.cancel_button.clicked.connect(self.onCancelClicked)  # type: ignore

        self.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                                font-size: 30px;
                                color: rgb(0, 0, 0) } 
                                QPushButton { background-color: #D3D3D3;
                                font-family: 'Times New Roman';
                                font-weight: bold;
                                border-radius:20px; }
                                QPushButton:hover { background: #A9A9A9; } ''')
        self.error_label.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                                font-size: 25px;
                                color: rgb(255, 0, 0) } ''')

    def onFeedbackClicked(self):
        try:
            if self.edit.text() == '':
                self.message_critical('Please enter your feedback!')
                return
            userInfo = getUserInfo()
            logger.error(userInfo['loginName'] + f': report id {self.feedbackId} - ' + self.edit.text())
            self.message_warning('Feedback successfully!')
            self.close()
            self.operateClicked.emit(self.windowTitle())  # type: ignore
        except Exception as e:
            logger.error(f'extras - onFeedbackClicked -  {e}')

    def onCancelClicked(self):
        try:
            self.close()
            self.operateClicked.emit(self.windowTitle())  # type: ignore
        except Exception as e:
            logger.error(f'extras - onCancelClicked -  {e}')

    def message_critical(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Critical), "Critical", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()

    def message_warning(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()
