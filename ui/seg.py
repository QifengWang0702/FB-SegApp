# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
import qtawesome
from ui.extra import Extra_UI
from util.service import *


# noinspection PyArgumentList
class seg_UI(QWidget):
    updateDataClicked = pyqtSignal()

    def __init__(self, name):
        super(seg_UI, self).__init__()

        self.seg_layout = QGridLayout()
        self.setLayout(self.seg_layout)

        configs = getConfigs()
        self.pic_path = configs['save']['pic']
        self.ico = configs['picture']['ico']

        self.winName = name
        if name == 'file':
            self.init_UI_file()
        else:
            self.init_UI_photo()

        # 打开图片路径
        self.root_path = ''
        # 图片存储名字
        self.file_name = ''
        # 超分辨率重建可视化路径
        self.rebuild_path = ''
        # 图像矫正可视化路径
        self.correct_path = ''
        # 可视化结果路径
        self.visual_path = ''
        # 检查报告路径
        self.report_path = ''

    def init_UI_file(self):
        self.widget1 = QWidget()
        self.layout1 = QGridLayout()
        self.widget1.setLayout(self.layout1)

        self.widget2 = QWidget()
        self.layout2 = QGridLayout()
        self.widget2.setLayout(self.layout2)

        self.widget3 = QWidget()
        self.layout3 = QGridLayout()
        self.widget3.setLayout(self.layout3)

        self.widget4 = QWidget()
        self.layout4 = QGridLayout()
        self.widget4.setLayout(self.layout4)

        self.seg_layout.addWidget(self.widget1, 0, 0, 9, 7)  # 右上左
        self.seg_layout.addWidget(self.widget2, 0, 7, 9, 3)  # 右上右
        self.seg_layout.addWidget(self.widget3, 9, 0, 3, 10)  # 右下左
        self.seg_layout.addWidget(self.widget4, 9, 5, 4, 5)  # 右下右

        # 右上左
        self.label_1 = QLabel("                   Please enter \n\n           fetal ultrasound image")
        self.label_1.setFixedSize(1150, 800)

        # 右上右
        self.button_1 = QPushButton(qtawesome.icon('fa.folder-open', color='#2c3a45'), "Image import")
        self.button_2 = QPushButton(qtawesome.icon('fa.magic', color='#2c3a45'), "Image rebuild")
        self.button_3 = QPushButton(qtawesome.icon('fa.scissors', color='#2c3a45'), "CCC/CV segment")
        self.button_4 = QPushButton(qtawesome.icon('fa.check-square', color='#2c3a45'), "Finish")
        self.button_5 = QPushButton(qtawesome.icon('fa.eye', color='#2c3a45'), "Report view")
        self.button_6 = QPushButton(qtawesome.icon('fa.history', color='#2c3a45'), "Operation reset")

        # 右下左
        self.label_2 = QLabel("Prenatal checkup results")
        self.textEdit_1 = QPlainTextEdit('\n CCC Area: \t\t\t CV Area: \n\n CCC Length: \t\t\t CV Length: ')
        self.textEdit_1.setFixedSize(800, 250)
        self.textEdit_1.setReadOnly(True)

        # 右下右
        self.checkBoxs = []

        self.label_3 = QLabel("Basic information")
        self.label_4 = QLabel("Result: ")
        self.checkBoxs.append(QCheckBox('normal'))
        self.checkBoxs.append(QCheckBox('abnormal'))
        self.textEdit_2 = QPlainTextEdit('\n Department: \n\n\n Doctor: ')
        self.textEdit_2.setFixedSize(270, 200)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_3 = QPlainTextEdit('\n Date: \n\n\n Pregweek: ')
        self.textEdit_3.setFixedSize(270, 200)
        self.textEdit_3.setReadOnly(True)

        self.button_1.clicked.connect(self.onImportClicked)  # type: ignore
        self.button_2.clicked.connect(self.onRebuildClicked)  # type: ignore
        self.button_3.clicked.connect(self.onSegmentationClicked)  # type: ignore
        self.button_4.clicked.connect(self.onFinishClicked)  # type: ignore
        self.button_5.clicked.connect(self.onViewReportClicked)  # type: ignore
        self.button_6.clicked.connect(self.onResetClicked)  # type: ignore
        self.checkBoxs[0].clicked.connect(lambda: self.checkBoxClicked(0))  # type: ignore
        self.checkBoxs[1].clicked.connect(lambda: self.checkBoxClicked(1))  # type: ignore

        # 右侧
        # 右上左
        self.layout1.addWidget(self.label_1, 0, 0, 9, 9)

        # 右上右
        self.layout2.addWidget(self.button_1, 0, 0, 3, 6)
        self.layout2.addWidget(self.button_2, 3, 0, 3, 6)
        self.layout2.addWidget(self.button_3, 6, 0, 3, 6)
        self.layout2.addWidget(self.button_4, 9, 0, 3, 6)
        self.layout2.addWidget(self.button_5, 12, 0, 3, 6)
        self.layout2.addWidget(self.button_6, 15, 0, 3, 6)

        # 右下左
        self.layout3.addWidget(self.label_2, 0, 0, 3, 3)
        self.layout3.addWidget(self.textEdit_1, 3, 0, 13, 13)

        # 右下右
        self.layout4.addWidget(self.label_3, 0, 0, 3, 3)
        self.layout4.addWidget(self.label_4, 3, 0, 1, 2)
        self.layout4.addWidget(self.checkBoxs[0], 3, 1, 1, 2)
        self.layout4.addWidget(self.checkBoxs[1], 3, 3, 1, 2)
        self.layout4.addWidget(self.textEdit_2, 6, 0, 4, 3)
        self.layout4.addWidget(self.textEdit_3, 6, 3, 4, 3)

        self.label_1.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 80px;
            border-radius: 40px;
            background-color: #FFFFFF; } ''')

        self.widget2.setStyleSheet(''' QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            border-radius: 20px;
            height: 100px;
            border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
            border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
            QPushButton:hover { background: #A9A9A9; } ''')

        self.widget3.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 28px;
            font-weight: bold; }
            QPlainTextEdit { font-family: 'Times New Roman';
            font-size: 40px;
            border-radius: 40px;
            background-color: #FFFFFF; }
            QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            border-radius: 20px;
            width: 60px;
            height: 30px;
            border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
            border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
            QPushButton:hover { background: #A9A9A9; } ''')

        self.widget4.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 28px;
            background-color: transparent; }
            QCheckBox { font-family: 'Times New Roman';
            font-size: 28px;
            background-color: transparent; }
            QCheckBox::indicator { border-radius: 10px;
            border: 3px solid #444444;
            width: 15px;
            height: 15px;
            background-color: transparent; }
            QCheckBox::indicator:checked { background-color: #696969; }
            QPlainTextEdit{ font-family: 'Times New Roman';
            font-size: 26px;
            border-radius: 40px;
            background-color: #FFFFFF; } ''')

        self.label_3.setStyleSheet('''QLabel { font-weight: bold; }''')

    def init_UI_photo(self):
        self.widget1 = QWidget()
        self.layout1 = QGridLayout()
        self.widget1.setLayout(self.layout1)

        self.widget2 = QWidget()
        self.layout2 = QGridLayout()
        self.widget2.setLayout(self.layout2)

        self.widget3 = QWidget()
        self.layout3 = QGridLayout()
        self.widget3.setLayout(self.layout3)

        self.widget4 = QWidget()
        self.layout4 = QGridLayout()
        self.widget4.setLayout(self.layout4)

        self.seg_layout.addWidget(self.widget1, 0, 0, 9, 7)  # 右上左
        self.seg_layout.addWidget(self.widget2, 0, 7, 9, 3)  # 右上右
        self.seg_layout.addWidget(self.widget3, 9, 0, 3, 10)  # 右下左
        self.seg_layout.addWidget(self.widget4, 9, 5, 4, 5)  # 右下右

        # 右上左
        self.label_1 = QLabel("                   Please enter \n\n           fetal ultrasound image")
        self.label_1.setFixedSize(1150, 800)
        # self.button_1 = QPushButton(qtawesome.icon('fa.user', color='#2c3a45'), "OK")
        # self.button_1.setVisible(False)

        # 右上右
        self.button_1 = QPushButton(qtawesome.icon('fa.camera', color='#2c3a45'), "Image import")
        self.button_2 = QPushButton(qtawesome.icon('fa.retweet', color='#2c3a45'), "Image correct")
        self.button_3 = QPushButton(qtawesome.icon('fa.scissors', color='#2c3a45'), "CCC/CV segment")
        self.button_4 = QPushButton(qtawesome.icon('fa.check-square', color='#2c3a45'), "Finish")
        self.button_5 = QPushButton(qtawesome.icon('fa.eye', color='#2c3a45'), "Report view")
        self.button_6 = QPushButton(qtawesome.icon('fa.history', color='#2c3a45'), "Operation reset")

        # 右下左
        self.label_2 = QLabel("Prenatal checkup results")
        self.textEdit_1 = QPlainTextEdit('\n CCC Area: \t\t\t CV Area: \n\n CCC Length: \t\t\t CV Length: ')
        self.textEdit_1.setFixedSize(800, 250)
        self.textEdit_1.setReadOnly(True)

        # 右下右
        self.checkBoxs = []

        self.label_3 = QLabel("Basic information")
        self.label_4 = QLabel("Result: ")
        self.checkBoxs.append(QCheckBox('normal'))
        self.checkBoxs.append(QCheckBox('abnormal'))
        self.textEdit_2 = QPlainTextEdit('\n Department: \n\n\n Doctor: ')
        self.textEdit_2.setFixedSize(270, 200)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_3 = QPlainTextEdit('\n Date: \n\n\n Pregweek: ')
        self.textEdit_3.setFixedSize(270, 200)
        self.textEdit_3.setReadOnly(True)

        self.button_1.clicked.connect(self.onCaptureClicked)  # type: ignore
        self.button_2.clicked.connect(self.onCorrectClicked)  # type: ignore
        self.button_3.clicked.connect(self.onSegmentationClicked)  # type: ignore
        self.button_4.clicked.connect(self.onFinishClicked)  # type: ignore
        self.button_5.clicked.connect(self.onViewReportClicked)  # type: ignore
        self.button_6.clicked.connect(self.onResetClicked)  # type: ignore
        # self.button_7.clicked.connect(self.button_7_click)
        self.checkBoxs[0].clicked.connect(lambda: self.checkBoxClicked(0))  # type: ignore
        self.checkBoxs[1].clicked.connect(lambda: self.checkBoxClicked(1))  # type: ignore

        # 右侧
        # 右上左
        self.layout1.addWidget(self.label_1, 0, 0, 9, 9)
        # self.layout2.addWidget(self.button_1, 9, 0, 3, 3, Qt.AlignCenter)

        # 右上右
        self.layout2.addWidget(self.button_1, 0, 0, 3, 6)
        self.layout2.addWidget(self.button_2, 3, 0, 3, 6)
        self.layout2.addWidget(self.button_3, 6, 0, 3, 6)
        self.layout2.addWidget(self.button_4, 9, 0, 3, 6)
        self.layout2.addWidget(self.button_5, 12, 0, 3, 6)
        self.layout2.addWidget(self.button_6, 15, 0, 3, 6)

        # 右下左
        self.layout3.addWidget(self.label_2, 0, 0, 3, 3)
        self.layout3.addWidget(self.textEdit_1, 3, 0, 13, 13)

        # 右下右
        self.layout4.addWidget(self.label_3, 0, 0, 3, 3)
        self.layout4.addWidget(self.label_4, 3, 0, 1, 2)
        self.layout4.addWidget(self.checkBoxs[0], 3, 1, 1, 2)
        self.layout4.addWidget(self.checkBoxs[1], 3, 3, 1, 2)
        self.layout4.addWidget(self.textEdit_2, 6, 0, 4, 3)
        self.layout4.addWidget(self.textEdit_3, 6, 3, 4, 3)

        # self.widget1.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
        #     font-size: 80px;
        #     border-radius: 40px;
        #     background-color: #FFFFFF; }
        #     QPushButton { background-color: #D3D3D3;
        #     font-family: 'Times New Roman';
        #     font-size: 26px;
        #     font-weight: bold;
        #     border-radius: 20px;
        #     width: 60px;
        #     height: 30px;
        #     border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
        #     border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
        #     QPushButton:hover { background: #A9A9A9; } ''')
        self.label_1.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
                    font-size: 80px;
                    border-radius: 40px;
                    background-color: #FFFFFF; } ''')

        self.widget2.setStyleSheet(''' QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            border-radius: 20px;
            height: 100px;
            border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
            border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
            QPushButton:hover { background: #A9A9A9; } ''')

        self.widget3.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 28px;
            font-weight: bold; }
            QPlainTextEdit { font-family: 'Times New Roman';
            font-size: 40px;
            border-radius: 40px;
            background-color: #FFFFFF; }
            QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            border-radius: 20px;
            width: 60px;
            height: 30px;
            border-bottom: 6px solid qlineargradient(y0:0, y1:1,stop: 0 #D3D3D3, stop: 1  #ececef);
            border-right: 6px solid qlineargradient(x0:0, x1:1,stop:  0 #D3D3D3, stop: 1 #ececef); }
            QPushButton:hover { background: #A9A9A9; } ''')

        self.widget4.setStyleSheet(''' QLabel { font-family: 'Times New Roman';
            font-size: 28px;
            background-color: transparent; }
            QCheckBox { font-family: 'Times New Roman';
            font-size: 28px;
            background-color: transparent; }
            QCheckBox::indicator { border-radius: 10px;
            border: 3px solid #444444;
            width: 15px;
            height: 15px;
            background-color: transparent; }
            QCheckBox::indicator:checked { background-color: #696969; }
            QPlainTextEdit{ font-family: 'Times New Roman';
            font-size: 26px;
            border-radius: 40px;
            background-color: #FFFFFF; } ''')

        self.label_3.setStyleSheet('''QLabel { font-weight: bold; }''')

    def onImportClicked(self):
        try:
            if self.root_path != '':
                self.onResetClicked()
            absolute_path = QFileDialog.getOpenFileName(self, 'Open file',
                                                        '.', "image files (*.jpg;*.jpeg;*.png)")
            if absolute_path[0] != '':
                self.root_path = absolute_path[0]
                logger.info(f'seg - onImportClicked - Image path: {absolute_path[0]}')
            else:
                logger.info(f'seg - onImportClicked - No image path!')
                return
            if self.root_path != '':
                logger.info(f'seg - onImportClicked - Display image: {self.root_path}')
                self.label_1.setPixmap(QPixmap(self.root_path).scaled(1150, 800))
            else:
                logger.error(f'seg - onImportClicked - No image display!')
                self.message_warning('No image display!')
                return
            if absolute_path[0] != '' and self.root_path != '':
                self.infoUi = Extra_UI()
                self.infoUi.info_ui()
                self.infoUi.nameClicked.connect(self.getInfo)
                self.infoUi.ageClicked.connect(self.getInfo)
                self.infoUi.show()
        except Exception as e:
            logger.error(f'seg - onImportClicked - {e}')
            self.root_path = ''

    def onCaptureClicked(self):
        try:
            if self.root_path != '':
                self.onResetClicked()
            cameraIds = getCameraList()
            if len(cameraIds) == 0:
                logger.error(f'photo - onCaptureClicked - This computer has no camera!')
                self.message_warning('This computer has no camera!')
                return
            self.cameraUI = Extra_UI()
            self.cameraUI.camera_ui()
            ex = self.cameraUI.exec_()
            if self.cameraUI.cap.isOpened():
                self.cameraUI.camera_timer.stop()
                self.cameraUI.cap.release()
            if ex == self.cameraUI.Accepted:
                if self.cameraUI.cap_path != '':
                    self.root_path = self.cameraUI.cap_path
                    self.label_1.setPixmap(QPixmap(self.root_path).scaled(1150, 800))
                    self.infoUi = Extra_UI()
                    self.infoUi.info_ui()
                    self.infoUi.nameClicked.connect(self.getInfo)
                    self.infoUi.ageClicked.connect(self.getInfo)
                    self.infoUi.show()
        except Exception as e:
            logger.error(f'photo - onCaptureClicked - {e}')

    def onRebuildClicked(self):
        try:
            if self.root_path == '':
                logger.error(f'seg - onRebuildClicked - No image import!')
                self.message_warning('Please select fetal ultrasound image!')
                return
            if self.rebuild_path != '' or self.visual_path != '':
                logger.error(f'seg - onRebuildClicked - Completed super-resolution rebuild!')
                self.message_warning('Already completed super-resolution rebuild!')
                return
            self.rebuild_path, self.file_name = getResolve(self.root_path)
            if self.rebuild_path == '':
                logger.error(f'seg - onRebuildClicked - Super-resolution rebuild error!')
                self.message_warning('Super-resolution rebuild error! Please contact the administrator!')
                self.onResetClicked()
                return
            self.label_1.setPixmap(QPixmap(self.rebuild_path).scaled(1150, 800))
        except Exception as e:
            logger.error(f'seg - onRebuildClicked - {e}')

    def onCorrectClicked(self):
        try:
            if self.root_path == '':
                logger.error(f'seg - onCorrectClicked - No image import!')
                self.message_warning('Please select fetal ultrasound image!')
                return
            if self.correct_path != '' or self.visual_path != '':
                logger.error(f'seg - onCorrectClicked - Completed image correct!')
                self.message_warning('Already completed image correct!')
                return
            self.correct_path, self.file_name = getCorrect(self.root_path)
            if self.correct_path == '':
                logger.error(f'seg - onCorrectClicked - Image correct error!')
                self.message_warning('Image correct error! Please contact the administrator!')
                self.onResetClicked()
                return
            self.label_1.setPixmap(QPixmap(self.correct_path).scaled(1150, 800))
        except Exception as e:
            logger.error(f'seg - onCorrectClicked - {e}')

    def onSegmentationClicked(self):
        try:
            if self.root_path == '':
                logger.error(f'seg - onSegmentationClicked - No image import!')
                self.message_warning('Please select fetal ultrasound image!')
                return
            if self.visual_path != '':
                logger.error(f'seg - onSegmentationClicked - Completed CCC&CV segmentation!')
                self.message_warning('Already completed CCC&CV segmentation!')
                return
            if self.file_name != '':
                if self.rebuild_path != '':
                    self.visual_path, self.file_name, self.CArea, self.VArea, self.CLength, self.VLength = getSegCCC_CV(
                        self.rebuild_path, self.file_name)
                elif self.correct_path != '':
                    self.visual_path, self.file_name, self.CArea, self.VArea, self.CLength, self.VLength = getSegCCC_CV(
                        self.correct_path, self.file_name)
                else:
                    logger.error(f'seg - onSegmentationClicked - Preprocess error!')
                    self.message_warning('Preprocess error!')
                    return
            else:
                self.visual_path, self.file_name, self.CArea, self.VArea, self.CLength, self.VLength = getSegCCC_CV(
                    self.root_path)
            if self.visual_path == '':
                logger.error(f'seg - onSegmentationClicked - Segment CCC&CV error!')
                self.message_warning('Segment CCC&CV error! Please contact the administrator!')
                self.onResetClicked()
                return
            self.pregweek, warn = getOcr(self.root_path)
            if warn != '':
                self.message_warning(warn)
            result = getSegResult(self.CArea, self.CLength, self.VArea, self.VLength)
            self.label_1.setPixmap(QPixmap(self.visual_path).scaled(1150, 800))
            self.textEdit_1.setPlainText(
                f'\n CCC Area: {self.CArea}\t\t CV Area: {self.VArea}\n\n CCC Length: {self.CLength}\t\t CV Length: {self.VLength}')
            if result:
                self.checkBoxClicked(0)
            else:
                self.checkBoxClicked(1)
            for checkBox in self.checkBoxs:
                if checkBox.isChecked():
                    self.result = checkBox.text()
            self.date = getNowTime(0)
            userInfo = getUserInfo()
            department = userInfo['department']
            doctor = userInfo['loginName']
            # if not self.textEdit_2.isVisible():
            #     print('delete textEdit_2')
            #     return
            self.textEdit_2.setPlainText(f'\n Department: {department}\n\n\n Doctor: {doctor}')
            self.textEdit_3.setPlainText(f'\n Date: {self.date}\n\n\n Pregweek: {self.pregweek}')
            if self.CArea <= 0 or self.VArea <= 0:
                logger.error(f'seg - onSegmentationClicked - Please update the algorithm!')
                self.message_warning('Please contact the administrator to update the algorithm!')
            # setPDF(self.file_name, 1)
        except Exception as e:
            logger.error(f'seg - onSegmentationClicked - {e}')
            self.message_warning('Error! Segment failed!')

    def onFinishClicked(self):
        try:
            if self.root_path == '':
                logger.error(f'seg - onFinishClicked - No image import!')
                self.message_warning('Please select fetal ultrasound image!')
                return
            if self.visual_path == '':
                logger.error(f'seg - onFinishClicked - No CCC&CV segment!')
                self.message_warning('Please segment fetal ultrasound image!')
                return
            if self.report_path != '':
                logger.info(f'seg - onFinishClicked - Report {self.reportId} already saved!')
                self.message_warning(f'Report {self.reportId} already saved! Start update!')
                self.reportId = storeResult(self.name, self.date, self.result, self.file_name,
                                            self.pregweek, self.age, isSecond=True)
            else:
                self.reportId = storeResult(self.name, self.date, self.result, self.file_name, self.pregweek, self.age)
            self.report_path = setPDF(self.file_name, self.reportId, self.visual_path, self.CArea, self.CLength,
                                      self.VArea, self.VLength, self.name, self.pregweek, self.date,
                                      self.result, self.age)
            self.updateDataClicked.emit()  # type: ignore
            self.message_warning('The inspection report was saved successfully!')
        except Exception as e:
            logger.error(f'seg - onFinishClicked - {e}')
            self.message_warning('Error! Save failed!')

    def onViewReportClicked(self):
        try:
            if self.root_path == '':
                logger.error(f'seg - onViewReportClicked - No image import!')
                self.message_warning('Please select fetal ultrasound image!')
                return
            if self.visual_path == '':
                logger.error(f'seg - onViewReportClicked - No CCC&CV segment!')
                self.message_warning('Please segment fetal ultrasound image!')
                return
            if self.report_path == '':
                logger.error(f'seg - onViewReportClicked - No report saved!')
                self.message_warning('Please save the inspection report!')
                return
            self.reportUI = Extra_UI()
            self.reportUI.report_ui(self.report_path)
            self.reportUI.show()
        except Exception as e:
            logger.error(f'seg - onViewReportClicked - {e}')
            self.message_warning('Error! Open report failed!')

    def onResetClicked(self):
        try:
            configs = getConfigs()
            if self.file_name != '' and self.report_path == '':
                try:
                    type(self.reportId)
                except Exception:
                    self.reportId = 0
                report_path = os.path.join(configs['save']['report'], getNowTime(0), self.file_name + '.pdf')
                deleteRow('pregnant', 'reportId', self.reportId, report=report_path)


            selfDict = list(vars(self).keys())
            selfList = ['seg_layout', 'winName', 'root_path']
            for name in selfDict:
                if name not in selfList:
                    delattr(self, name)

            self.pic_path = configs['save']['pic']
            self.ico = configs['picture']['ico']
            self.root_path = ''
            self.rebuild_path = ''
            self.correct_path = ''
            self.visual_path = ''
            self.file_name = ''
            self.report_path = ''
            if self.winName == 'file':
                self.init_UI_file()
            else:
                self.init_UI_photo()
            logger.info(f'seg - onResetClicked - Reset successfully!')
        except Exception as e:
            logger.error(f'seg - onResetClicked - {e}')

    def checkBoxClicked(self, num):
        if self.root_path == '':
            logger.error(f'seg - checkBoxClicked - No image import!')
            self.message_warning('Please select fetal ultrasound image!')
            return
        for i in range(len(self.checkBoxs)):
            if i != num:
                self.checkBoxs[i].setChecked(False)
            else:
                self.checkBoxs[i].setChecked(True)
        if self.visual_path != '':
            self.result = self.checkBoxs[num].text()
        else:
            logger.error(f'seg - checkBoxClicked - No visual result!')
            self.message_warning('Please get CCC&CV segmentation!')

    def message_warning(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()

    def getInfo(self, value):
        try:
            logger.info(f'seg - getInfo - Get info: {value}')
            if isinstance(value, int):
                self.age = value
            else:
                self.name = value
        except Exception as e:
            logger.error(f'seg - getInfo - {e}')
