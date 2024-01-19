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
                    message = self.fetch_ip_info(ip_address)
                else:
                    message = '离线模式（ToDo）'

                self.display_information(message)

    def extract_ips(self, text):
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:?:(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}\b'

        ipv4_addresses = re.findall(ipv4_pattern, text)
        ipv6_addresses = re.findall(ipv6_pattern, text)

        return ipv4_addresses + ipv6_addresses

    def fetch_ip_info(self, ip_address):
        api_url = f"https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr?ip={ip_address}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            ip_info = response.json().get("data", {})
            message = self.parse_ip_info(ip_info)
            return message

        except requests.RequestException as e:
            return f"Failed to fetch info for IP Address {ip_address}. Error: {e}"

    def parse_ip_info(self, ip_info):
        addr = ip_info.get("addr", "")
        country = ip_info.get("country", "")
        province = ip_info.get("province", "")
        city = ip_info.get("city", "")
        isp = ip_info.get("isp", "")

        result = f"地址: {addr}\n国家: {country}\n地址：{province} {city}\nISP: {isp}"
        return result

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
