import os
import re
import sys
import threading
import time
import tkinter as tk
from tkinter import Tk, Text, Scrollbar, END, W, N, S, E, ttk, StringVar

import pyperclip
import pystray
import requests
from PIL import Image
from pystray import MenuItem as item
from win10toast import ToastNotifier


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


def fetch_ip_info(ip_address):
    api_url = f"https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr?ip={ip_address}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        ip_info = response.json().get("data", {})
        message = parse_ip_info(ip_info)
        return message

    except requests.RequestException as e:
        return f"Failed to fetch info for IP Address {ip_address}. Error: {e}"

def mannul_analyze_ip(dataText):
    messages = analyze_ip(dataText)
    clear_text()
    for message in messages:
        display_information(message)

def analyze_ip(dataText):
    ip_addresses = extract_ips(dataText)

    messages = []
    if ip_addresses:
        for ip_address in ip_addresses:
            # 根据下拉框选择解析模式
            global mode_var
            mode = mode_var.get()
            if mode == "在线模式":
                message = fetch_ip_info(ip_address)
            else:
                # 离线模式（ToDo）
                message = "Mode not implemented yet"
            messages.append(message)
    else:
        messages.append("未检测到有效IP地址")
    # print(messages)
    return messages


def clipboard_monitor():
    previous_clipboard_data = pyperclip.paste()

    while not exit_flag:
        current_clipboard_data = pyperclip.paste()

        if current_clipboard_data != previous_clipboard_data:
            print("Clipboard content changed: ", current_clipboard_data)
            messages = analyze_ip(current_clipboard_data)
            global icoPath
            for message in messages:
                DisInfo_toAll(message, icoPath)
            # win.after(0, DisInfo_toAll, message, icoPath)  # 在主线程中调度任务
            previous_clipboard_data = current_clipboard_data

        time.sleep(1)


def DisInfo_toAll(message, icoPath):
    display_information(message)
    ToastNotifier().show_toast("IP查询监控", message, icon_path=str(icoPath), duration=3)


def set_theme():
    style = ttk.Style()
    # 更改主题名称，你可以选择其他主题，比如"clam"、"alt"等
    style.theme_use("clam")

def clear_text():
    text_widget.config(state="normal")
    text_widget.delete(1.0, END)
    text_widget.config(state="disabled")
def display_information(message):
    # 更新 Tkinter 窗口中的信息
    text_widget.config(state="normal")
    text_widget.insert(END, message + "\n\n")
    text_widget.config(state="disabled")
    text_widget.yview(END)
    # 检查滚动条是否可见
    # update_scrollbar_visibility()


def update_scrollbar_visibility():
    # 根据文本框是否需要滚动来隐藏或显示滚动条
    if text_widget.get(1.0, "end-1c") == "":
        scrollbar.grid_remove()  # 隐藏滚动条
    else:
        scrollbar.grid(row=1, column=2, sticky=N + S, rowspan=2, padx=(0, 10), pady=10)  # 调整 y 轴上的位置和高度


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
# 获取资源文件路径
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)
pngPath = os.path.join(basedir, 'res\\原神H.png')
icoPath = os.path.join(basedir, 'res\\原神H.ico')
print(pngPath, icoPath)

image = Image.open(pngPath)
icon = pystray.Icon("name", image, "IP地理位置查询", menu)
win = Tk()
win.title("IP地址解析")
win.geometry("400x400")


# 手动查询IP地址框
ip_entry = tk.Entry(win)
ip_entry.grid(row=0, column=0, padx=10, pady=10, sticky=W + E)
# 绑定回车键事件
ip_entry.bind('<Return>', lambda event: mannul_analyze_ip(ip_entry.get()))

# Add a button to trigger IP analysis
analyze_button = tk.Button(win, text="查询", command=lambda: mannul_analyze_ip(ip_entry.get()))
analyze_button.grid(row=0, column=1, padx=10, pady=10, sticky=W + E)

# 添加一个 Text 控件用于显示信息
text_widget = Text(win, wrap="word", width=40, height=10, state="disabled")
text_widget.grid(row=1, column=0, padx=10, pady=10, sticky=W + N + S + E)

# 添加一个滚动条
scrollbar = Scrollbar(win, command=text_widget.yview)
scrollbar.grid(row=1, column=2, sticky=N + S, rowspan=2, padx=(0, 10), pady=10)  # 调整 y 轴上的位置和高度

# 下拉框
mode_var = StringVar(win)
mode_var.set("在线模式")  # 设置默认为在线模式
modes = ["在线模式", "离线模式"]  # 模式列表
mode_dropdown = ttk.Combobox(win, textvariable=mode_var, values=modes, state="readonly")
mode_dropdown.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky=W + E)

# 在垂直方向上配置 rowconfigure，以允许滚动条伸缩
win.rowconfigure(1, weight=1)

# 调整行列及大小
win.columnconfigure(0, weight=1)
win.columnconfigure(1, weight=1)
win.columnconfigure(2, weight=0)  # 不需要滚动条占用额外空间

# 重新定义点击关闭按钮的处理
win.protocol('WM_DELETE_WINDOW', on_exit)
# 在创建窗口后调用设置主题的函数
set_theme()

# 启动剪贴板监控线程
threading.Thread(target=clipboard_monitor, daemon=True).start()

# 启动托盘图标
threading.Thread(target=icon.run, daemon=True).start()

win.mainloop()
