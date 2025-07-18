# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from ui.login import Login_UI


def message_warning(str):
    msg_box = QMessageBox(QMessageBox.Icon(QMessageBox.Warning), "Warning", str)
    msg_box.setWindowIcon(QIcon('./pic/bh.ico'))
    msg_box.show()
    msg_box.exec()
    msg_box.sender().text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    platform = sys.platform
    if 'win' not in platform and 'linux' not in platform:
        message_warning(f'The IRSPUI does not currently support {platform}!')
    else:
        main = Login_UI()
        main.show()
    sys.exit(app.exec_())
