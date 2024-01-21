import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QComboBox, QLabel, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import pyperclip
import threading
import time
import requests


class IPAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('IP地址解析')
        self.setGeometry(100, 100, 400, 400)

        # 输入框
        self.ip_entry = QTextEdit(self)
        self.ip_entry.setPlaceholderText('在此输入IP地址...')
        self.ip_entry.setGeometry(10, 10, 280, 30)

        # 查询按钮
        self.analyze_button = QPushButton('查询', self)
        self.analyze_button.setGeometry(300, 10, 80, 30)
        self.analyze_button.clicked.connect(self.analyze_ip)

        # 显示信息文本框
        self.text_widget = QTextEdit(self)
        self.text_widget.setGeometry(10, 60, 370, 200)
        self.text_widget.setReadOnly(True)

        # 下拉框
        self.mode_dropdown = QComboBox(self)
        self.mode_dropdown.addItems(['在线模式', '离线模式'])
        self.mode_dropdown.setGeometry(10, 280, 120, 30)

        # 清空按钮
        clear_button = QPushButton('清空', self)
        clear_button.setGeometry(140, 280, 60, 30)
        clear_button.clicked.connect(self.clear_text)

        # 退出按钮
        exit_button = QPushButton('退出', self)
        exit_button.setGeometry(210, 280, 60, 30)
        exit_button.clicked.connect(self.close)

        # 设置窗口透明度
        self.setWindowOpacity(0.9)

        # 设置 QSS 样式
        self.setStyleSheet('''
            QMainWindow {
                background-color: rgba(0, 0, 128, 85);  /* 蓝色玻璃半透明 */
            }

            QTextEdit, QComboBox, QPushButton {
                background-color: rgba(255, 255, 255, 60);  /* 白色半透明 */
                border: 1px solid rgba(0, 0, 0, 50);
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton:hover {
                background-color: rgba(200, 200, 255, 200);  /* 按钮悬停时的颜色 */
            }
        ''')

        # 启动剪贴板监控线程
        threading.Thread(target=self.clipboard_monitor, daemon=True).start()

    def analyze_ip(self):
        ip_text = self.ip_entry.toPlainText()
        mode = self.mode_dropdown.currentText()

        if ip_text:
            ip_addresses = self.extract_ips(ip_text)

            for ip_address in ip_addresses:
                if mode == '在线模式':
                    message = self.fetch_ip_info_bili(ip_address)
                else:
                    message = '离线模式（ToDo）'

                self.display_information(message)


    def display_information(self, message):
        self.text_widget.append(message)

    def clear_text(self):
        self.text_widget.clear()

    def clipboard_monitor(self):
        previous_clipboard_data = pyperclip.paste()

        while True:
            current_clipboard_data = pyperclip.paste()

            if current_clipboard_data != previous_clipboard_data:
                self.ip_entry.setPlainText(current_clipboard_data)
                self.analyze_ip()
                previous_clipboard_data = current_clipboard_data

            time.sleep(1)


def run_app():
    app = QApplication(sys.argv)
    # 获取资源文件路径
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    pngPath = os.path.join(basedir, 'res\\原神H.png')
    icoPath = os.path.join(basedir, 'res\\原神H.ico')
    app.setWindowIcon(QIcon(pngPath))  # 设置应用图标
    mainWin = IPAnalyzerApp()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
