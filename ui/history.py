# -*- coding: UTF-8 -*-
from PyQt5.QtSql import QSqlQueryModel
from ui.extra import *
from util.service import *


# noinspection PyArgumentList
class history_UI(QWidget):

    def __init__(self, tableName):
        super(history_UI, self).__init__()

        self.history_layout = QVBoxLayout()
        self.setLayout(self.history_layout)

        configs = getConfigs()
        self.pic_path = configs['save']['pic']
        self.ico = configs['picture']['ico']

        self.userInfo = getUserInfo()
        self.tableName = tableName
        self.currentPage = 1  # 当前页
        self.totalPage = 1  # 总页数
        self.totalRecordCount = configs['database']['pageCount']  # 总记录数
        self.pageRecordCount = configs['database']['pageCount']  # 每页记录数
        self.queryModel = QSqlQueryModel()

        if self.userInfo['identity'] == 'A':
            self.init_UI_A()
        else:
            self.init_UI_D()
        self.updateStatus()

    def init_UI_D(self):
        self.widget1 = QWidget()
        self.hbox_layout1 = QHBoxLayout()
        self.widget1.setLayout(self.hbox_layout1)

        self.tableView = QTableView()
        self.delegate = UserButtonDelegate(self.tableView)
        # self.tableWeight = QTableWidget()

        self.widget2 = QWidget()
        self.hbox_layout2 = QHBoxLayout()
        self.widget2.setLayout(self.hbox_layout2)

        self.history_layout.addWidget(self.widget1)
        self.history_layout.addWidget(self.tableView)
        self.history_layout.addWidget(self.widget2)

        # 右上
        self.key_label = QLabel("key: ")
        self.value_label = QLabel("value: ")
        self.combo = QComboBox(self)
        self.combo.addItem('--Please select--')
        self.headers = getFieldName(self.tableName)
        for header in self.headers:
            self.combo.addItem(header)
        # self.combo.addItems(['--Please select--', 'id', 'name', 'age', 'pregweek', 'doctor', 'date', 'result'])
        self.combo.setFixedWidth(240)
        self.valueEdit = QLineEdit()
        self.valueEdit.setFixedWidth(240)
        self.selectButton = QPushButton("Select")
        self.resetButton = QPushButton("Reset")

        # 右中
        delegate = CenterDelegate()
        self.tableView.setShowGrid(False)  # 显示网格线
        self.tableView.verticalHeader().hide()
        self.tableView.setFrameShape(QTableView.NoFrame)  # 隐藏外边框
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFixedHeight(80)
        # self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView.setItemDelegate(delegate)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setItemDelegateForColumn(len(self.headers) - 2, self.delegate)
        self.tableView.setItemDelegateForColumn(len(self.headers) - 1, self.delegate)
        # else:
        #     self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # try:
        #     self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # except Exception as e:
        #     print(e)
        # self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动调整行高

        # 右下
        self.jump_label = QLabel("Jump to page ")
        self.cur_label = QLabel("current page: ")
        self.total_label = QLabel("total page: ")
        self.total_page_label = QLabel()
        self.current_page_label = QLabel()
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(40)
        self.prevButton = QPushButton("Prev")
        self.nextButton = QPushButton("Next")
        self.switchPageButton = QPushButton("Switch")

        self.selectButton.clicked.connect(self.onTableChangedClicked)  # type: ignore
        self.resetButton.clicked.connect(self.onTableResetClicked)  # type: ignore
        self.prevButton.clicked.connect(self.onPrevPageClicked)  # type: ignore
        self.nextButton.clicked.connect(self.onNextPageClicked)  # type: ignore
        self.switchPageButton.clicked.connect(self.onSwitchPageClicked)  # type: ignore
        self.delegate.userFeedback.connect(self.onTableFeedbackClicked)
        self.delegate.userUpdate.connect(self.onTableUpdateClicked)

        self.hbox_layout1.addWidget(self.key_label)
        self.hbox_layout1.addWidget(self.combo)
        self.hbox_layout1.addWidget(self.value_label)
        self.hbox_layout1.addWidget(self.valueEdit)
        self.hbox_layout1.addWidget(self.selectButton)
        self.hbox_layout1.addWidget(self.resetButton)
        self.hbox_layout1.addStretch(1)

        self.hbox_layout2.addWidget(self.prevButton)
        self.hbox_layout2.addWidget(self.nextButton)
        self.hbox_layout2.addWidget(self.jump_label)
        self.hbox_layout2.addWidget(self.switchPageLineEdit)
        self.hbox_layout2.addWidget(self.switchPageButton)
        self.hbox_layout2.addWidget(self.cur_label)
        self.hbox_layout2.addWidget(self.current_page_label)
        self.hbox_layout2.addWidget(self.total_label)
        self.hbox_layout2.addWidget(self.total_page_label)
        self.hbox_layout2.addStretch(1)

        self.setStyleSheet(''' QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            border-radius: 20px;
            height: 50px;
            width: 100px; }
            QPushButton:hover { background: #A9A9A9; } 
            QLabel { font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold; }
            QLineEdit { font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            background-color: #FFFFFF; }
            QComboBox { font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            background-color: #D3D3D3;
            border: none; }
            QComboBox::drop-down {
            width: 30px; } ''')

        self.tableView.setStyleSheet(''' QTableView { font-family: 'Times New Roman';
                font-size: 30px; }
                QTableView::item:selected { background-color: #696969;
                font-weight: bold; }
                QHeaderView::section { font-family: 'Times New Roman';
                font-size: 30px;
                background-color: #D3D3D3;
                border: none; }''')

    def init_UI_A(self):
        self.widget1 = QWidget()
        self.hbox_layout1 = QHBoxLayout()
        self.widget1.setLayout(self.hbox_layout1)

        self.tableView = QTableView()
        self.delegate = AdminButtonDelegate(self.tableView)
        # self.tableWeight = QTableWidget()

        self.widget2 = QWidget()
        self.hbox_layout2 = QHBoxLayout()
        self.widget2.setLayout(self.hbox_layout2)

        self.history_layout.addWidget(self.widget1)
        self.history_layout.addWidget(self.tableView)
        self.history_layout.addWidget(self.widget2)

        # 右上
        self.key_label = QLabel("key: ")
        self.value_label = QLabel("value: ")
        self.combo = QComboBox(self)
        self.combo.addItem('--Please select--')
        self.headers = getFieldName(self.tableName)
        for header in self.headers:
            self.combo.addItem(header)
        # self.combo.addItems(['--Please select--', 'id', 'name', 'age', 'pregweek', 'doctor', 'date', 'result'])
        self.combo.setFixedWidth(240)
        self.valueEdit = QLineEdit()
        self.valueEdit.setFixedWidth(240)
        self.selectButton = QPushButton("Select")
        self.resetButton = QPushButton("Reset")
        self.addButton = QPushButton("Add")

        # 右中
        delegate = CenterDelegate()
        self.tableView.setShowGrid(False)  # 显示网格线
        self.tableView.verticalHeader().hide()
        self.tableView.setFrameShape(QTableView.NoFrame)  # 隐藏外边框
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFixedHeight(80)
        # self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView.setItemDelegate(delegate)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.tableName == 'pregnant':
            self.tableView.setItemDelegateForColumn(len(self.headers) - 2, self.delegate)
        self.tableView.setItemDelegateForColumn(len(self.headers) - 1, self.delegate)

        # 右下
        self.jump_label = QLabel("Jump to page ")
        self.cur_label = QLabel("current page: ")
        self.total_label = QLabel("total page: ")
        self.total_page_label = QLabel()
        self.current_page_label = QLabel()
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(40)
        self.prevButton = QPushButton("Prev")
        self.nextButton = QPushButton("Next")
        self.switchPageButton = QPushButton("Switch")

        self.selectButton.clicked.connect(self.onTableChangedClicked)  # type: ignore
        self.resetButton.clicked.connect(self.onTableResetClicked)  # type: ignore
        self.addButton.clicked.connect(self.onTableAddClicked)  # type: ignore
        self.prevButton.clicked.connect(self.onPrevPageClicked)  # type: ignore
        self.nextButton.clicked.connect(self.onNextPageClicked)  # type: ignore
        self.switchPageButton.clicked.connect(self.onSwitchPageClicked)  # type: ignore
        self.delegate.adminDelete.connect(self.onTableDeleteClicked)
        self.delegate.adminUpdate.connect(self.onTableUpdateClicked)

        self.hbox_layout1.addWidget(self.key_label)
        self.hbox_layout1.addWidget(self.combo)
        self.hbox_layout1.addWidget(self.value_label)
        self.hbox_layout1.addWidget(self.valueEdit)
        self.hbox_layout1.addWidget(self.selectButton)
        self.hbox_layout1.addWidget(self.resetButton)
        if self.tableName != 'pregnant':
            self.hbox_layout1.addWidget(self.addButton)
        self.hbox_layout1.addStretch(1)

        self.hbox_layout2.addWidget(self.prevButton)
        self.hbox_layout2.addWidget(self.nextButton)
        self.hbox_layout2.addWidget(self.jump_label)
        self.hbox_layout2.addWidget(self.switchPageLineEdit)
        self.hbox_layout2.addWidget(self.switchPageButton)
        self.hbox_layout2.addWidget(self.cur_label)
        self.hbox_layout2.addWidget(self.current_page_label)
        self.hbox_layout2.addWidget(self.total_label)
        self.hbox_layout2.addWidget(self.total_page_label)
        self.hbox_layout2.addStretch(1)

        self.setStyleSheet(''' QPushButton { background-color: #D3D3D3;
            font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            border-radius: 20px;
            height: 50px;
            width: 100px; }
            QPushButton:hover { background: #A9A9A9; } 
            QLabel { font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold; }
            QLineEdit { font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            background-color: #FFFFFF; }
            QComboBox { font-family: 'Times New Roman';
            font-size: 26px;
            font-weight: bold;
            background-color: #D3D3D3;
            border: none; }
            QComboBox::drop-down {
            width: 30px; } ''')

        self.tableView.setStyleSheet(''' QTableView { font-family: 'Times New Roman';
                font-size: 26px; }
                QTableView::item:selected { background-color: #696969;
                font-weight: bold; }
                QHeaderView::section { font-family: 'Times New Roman';
                font-size: 28px;
                background-color: #D3D3D3;
                border: none; }''')

    def onPrevPageClicked(self):
        self.currentPage -= 1
        self.updateStatus()

    def onNextPageClicked(self):
        self.currentPage += 1
        self.updateStatus()

    def onSwitchPageClicked(self):
        try:
            szText = self.switchPageLineEdit.text()
            pattern = re.compile('^[0-9]+$')
            match = pattern.match(szText)
            if not match:
                self.message_warning("Please enter the number!")
                return
            if szText == "":
                self.message_warning("Please enter the jump page!")
                return
            pageIndex = int(szText)
            if pageIndex > self.totalPage or pageIndex < 1:
                self.message_warning("There is no specified page, please re-enter!")
                return
            self.currentPage = pageIndex
            self.updateStatus()
        except Exception as e:
            logger.error(f'history - onSwitchPageClicked - {e}')

    # 更新空间状态
    def updateStatus(self, key='', value=''):
        try:
            if self.currentPage < 0 or self.currentPage > self.totalPage:
                logger.error(f'history - updateStatus - Invalid page {self.currentPage}, total: {self.totalPage}')
                return
            if key == '--Please select--':
                key = ''

            queryModel = getHistoryList(self.tableName, key=key, value=value)
            if queryModel is None:
                logger.error(f'history - updateStatus - queryModel is None!')
                self.message_warning('Select error! Please check your input!')

            self.totalRecordCount = queryModel.rowCount()
            if self.totalRecordCount % self.pageRecordCount == 0:
                self.totalPage = self.totalRecordCount / self.pageRecordCount
                if self.totalPage < 1:
                    self.totalPage = 1
            else:
                self.totalPage = int(self.totalRecordCount / self.pageRecordCount) + 1

            self.queryModel = getHistoryList(self.tableName, self.currentPage - 1, self.pageRecordCount, key, value,
                                             self.headers)

            self.tableView.setModel(self.queryModel)
            self.current_page_label.setText(str(self.currentPage))
            self.total_page_label.setText(str(int(self.totalPage)))
            if self.currentPage <= 1:
                self.prevButton.setEnabled(False)
            else:
                self.prevButton.setEnabled(True)

            if self.currentPage >= self.totalPage:
                self.nextButton.setEnabled(False)
            else:
                self.nextButton.setEnabled(True)
        except Exception as e:
            logger.error(f'history - updateStatus - {e}')

    def onTableChangedClicked(self):
        comboText = self.combo.currentText()
        lineText = self.valueEdit.text()
        self.currentPage = 1
        self.updateStatus(comboText, lineText)

    def onTableResetClicked(self):
        self.combo.setCurrentText('--Please select--')
        self.valueEdit.setText('')
        self.currentPage = 1
        self.updateStatus()

    def onTableFeedbackClicked(self, row):
        try:
            id = int(self.queryModel.data(self.queryModel.index(row, 0)))
            self.feedbackUI = Extra_UI()
            self.feedbackUI.feedback_ui(id)
            self.feedbackUI.show()
        except Exception as e:
            logger.error(f'history - onTableFeedbackClicked - {e}')

    def onTableAddClicked(self):
        try:
            headers = getUpdateAble(self.tableName)
            self.addUI = Extra_UI()
            self.addUI.table_ui('Add', self.tableName, headers)
            self.addUI.operateClicked.connect(self.delWin)
            self.addUI.show()
        except Exception as e:
            logger.error(f'history - onTableAddClicked - {e}')
            self.message_warning(f'Add failed! Reason: {e}')

    def onTableDeleteClicked(self, row):
        try:
            id = int(self.queryModel.data(self.queryModel.index(row, 0)))
            if self.tableName == 'pregnant':
                report = self.queryModel.data(self.queryModel.index(row, 7))
                flag = deleteRow(self.tableName, self.headers[0], id, report=report)
            else:
                userHead = self.queryModel.data(self.queryModel.index(row, 1))
                flag = deleteRow(self.tableName, self.headers[0], id, userHead=userHead)
            if flag:
                self.message_warning('Delete successfully!')
            else:
                logger.error(f'history - onTableDeleteClicked - delete failed!')
                self.message_warning('Delete failed!')
            self.updateStatus()
        except Exception as e:
            logger.error(f'history - onTableDeleteClicked - {e}')
            self.message_warning(f'Delete failed! Reason: {e}')

    def onTableUpdateClicked(self, row):
        try:
            data = []
            id = 0
            headers = getUpdateAble(self.tableName)
            report = ''
            for column in range(self.queryModel.columnCount()):
                index = self.queryModel.index(row, column)
                if column == 0:
                    id = self.queryModel.data(index)
                if self.queryModel.record(row).fieldName(column) in headers:
                    data.append(self.queryModel.data(index))
                if 'report' in self.queryModel.record(row).fieldName(column):
                    report = self.queryModel.data(index)
            self.updateUI = Extra_UI()
            self.updateUI.table_ui('Update', self.tableName, headers, data, id, report)
            self.updateUI.operateClicked.connect(self.delWin)
            self.updateUI.show()
        except Exception as e:
            logger.error(f'history - onTableUpdateClicked - {e}')
            self.message_warning(f'Update failed! Reason: {e}')

    def message_warning(self, str):
        msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
        msg_box.setWindowIcon(QIcon(f'{self.pic_path}/{self.ico}'))
        msg_box.show()
        msg_box.exec()

    def delWin(self, winName):
        self.updateStatus()
        if winName == 'Add':
            delattr(self, 'addUI')
        else:
            delattr(self, 'updateUI')
