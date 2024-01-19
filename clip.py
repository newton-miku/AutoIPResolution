import re
import threading
import time
from tkinter import Tk, Text, Scrollbar, END, RIGHT, Y, W, N, S, E
import requests

import pyperclip
import pystray
from PIL import Image
from pystray import MenuItem as item, Menu
from win10toast import ToastNotifier

import re


def extract_ips(text):
    # 正则表达式匹配IPv4地址
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # 正则表达式匹配IPv6地址
    ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:?:(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}\b'

    # 提取匹配的IP地址
    ipv4_addresses = re.findall(ipv4_pattern, text)
    ipv6_addresses = re.findall(ipv6_pattern, text)

    return ipv4_addresses + ipv6_addresses


def parse_ip_info(ip_info):
    addr = ip_info.get("addr", "")
    country = ip_info.get("country", "")
    province = ip_info.get("province", "")
    city = ip_info.get("city", "")
    isp = ip_info.get("isp", "")

    result = f"地址: {addr}\n国家: {country}\n地址：{province} {city}\nISP: {isp}"
    return result


def clipboard_monitor():
    previous_clipboard_data = pyperclip.paste()

    while not exit_flag:
        current_clipboard_data = pyperclip.paste()

        if current_clipboard_data != previous_clipboard_data:
            # Clipboard content has changed
            print("Clipboard content changed: ", current_clipboard_data)

            ip_addresses = extract_ips(current_clipboard_data)

            # Display a Windows toast notification
            if ip_addresses:
                for ip_address in ip_addresses:
                    api_url = f"https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr?ip={ip_address}"

                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
                        print(f"尝试解析{ip_address}")
                        response = requests.get(api_url, headers=headers)
                        response.raise_for_status()  # Raises HTTPError for bad responses

                        ip_info = response.json().get("data", {})
                        message = parse_ip_info(ip_info)
                        print(message)
                        display_information(message)
                        ToastNotifier().show_toast("IP查询监控", message, icon_path="res/原神H.ico", duration=3)

                    except requests.RequestException as e:
                        print(f"Failed to fetch info for IP Address {ip_address}. Error: {e}")

            # Update the previous clipboard data
            previous_clipboard_data = current_clipboard_data

        # Check every 2 seconds
        time.sleep(1)


def display_information(message):
    # 更新 Tkinter 窗口中的信息
    text_widget.config(state="normal")
    text_widget.insert(END, message + "\n\n")
    text_widget.config(state="disabled")
    text_widget.yview(END)
    # 检查滚动条是否可见
    update_scrollbar_visibility()


def update_scrollbar_visibility():
    # 根据文本框是否需要滚动来隐藏或显示滚动条
    if text_widget.get(1.0, "end-1c") == "":
        scrollbar.grid_remove()  # 隐藏滚动条
    else:
        scrollbar.grid(row=0, column=1, sticky=N + S)  # 显示滚动条


def quit_action(icon, item):
    global exit_flag
    exit_flag = True
    icon.stop()
    win.destroy()


def show_window(icon, item):
    win.deiconify()


def on_exit():
    win.withdraw()


exit_flag = False
toaster = ToastNotifier()

menu = (
    item('显示', show_window),
    item('退出', quit_action)
)
toaster = ToastNotifier()
toaster._show_toast = toaster.show_toast  # 保存原始的 show_toast 方法

# 使用 threaded=False 禁用 WinToaster 的图标
toaster.show_toast = lambda title, msg, duration=5, icon_path=None: toaster._show_toast(title, msg, duration, icon_path,
                                                                                        threaded=False)

image = Image.open("res/原神H.png")
icon = pystray.Icon("name", image, "IP地理位置查询", menu)
win = Tk()
win.title("IP地址解析")
win.geometry("330x175")

# 添加一个 Text 控件用于显示信息
text_widget = Text(win, wrap="word", width=40, height=10, state="disabled")
text_widget.grid(row=0, column=0, padx=10, pady=10, sticky=W + N + S + E)

# 添加一个滚动条
scrollbar = Scrollbar(win, command=text_widget.yview)
scrollbar.grid(row=0, column=1, sticky=N + S)

# 在垂直方向上配置 rowconfigure，以允许滚动条伸缩
win.rowconfigure(0, weight=1)

# 重新定义点击关闭按钮的处理
win.protocol('WM_DELETE_WINDOW', on_exit)

# 启动剪贴板监控线程
threading.Thread(target=clipboard_monitor, daemon=True).start()

# 启动托盘图标
threading.Thread(target=icon.run, daemon=True).start()

win.mainloop()
