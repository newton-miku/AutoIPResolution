import threading
import time
import tkinter as tk
from tkinter import Tk, Text, Scrollbar, END, W, N, S, E, ttk, StringVar

import pyperclip
import pystray
from PIL import Image
from pystray import MenuItem as item
from win11toast import toast

import sv_ttk  # Import the sv_ttk module

from util.apis import analyze_ip
from getpath import get_all_res_path


def manual_analyze_ip(data_text):
    mode = mode_var.get()
    messages = analyze_ip(data_text, mode=mode)
    for message in messages:
        display_information(message)


def clipboard_monitor():
    previous_clipboard_data = pyperclip.paste()

    while not exit_flag:
        current_clipboard_data = pyperclip.paste()

        if current_clipboard_data != previous_clipboard_data:
            mode = mode_var.get()
            results = analyze_ip(current_clipboard_data, True, mode)
            previous_clipboard_data = current_clipboard_data
            if "未检测到有效IP地址" in results:
                continue
            global icoPath
            totalcount = 0
            for result in results:
                if totalcount >= 4:
                    break
                ip_address = result.get("ip_address", "N/A")
                message = result.get("message", "No message")
                dis_info_to_all(message, icoPath, ip_address)
                totalcount += 1

        time.sleep(1)


def dis_info_to_all(message, ico_path, addr=None):
    display_information(message)
    if addr is not None:
        title = "IP查询监控-" + addr
    else:
        title = "IP查询监控"
    toast(title, message, lambda args: show_window(), str(ico_path), duration="short", app_id="IP查询监控")


def clear_text():
    text_widget.config(state="normal")
    text_widget.delete(1.0, END)
    text_widget.config(state="disabled")


def display_information(message):
    text_widget.config(state="normal")
    text_widget.insert(END, message + "\n\n")
    text_widget.config(state="disabled")
    text_widget.yview(END)


def quit_action(icon):
    global exit_flag
    exit_flag = True
    icon.stop()
    win.destroy()


def show_window():
    win.deiconify()


def on_exit():
    win.withdraw()


exit_flag = False

menu = (
    item('显示', show_window),
    item('退出', quit_action)
)

pngPath, icoPath = get_all_res_path()
image = Image.open(pngPath)
icon = pystray.Icon("name", image, "IP地理位置查询", menu)


def create_window():
    # 声明全局变量
    global win, ip_entry, text_widget, scrollbar, mode_var, mode_dropdown, clear_button
    win = Tk()
    win.title("IP地址解析")
    win.geometry("350x550")  # 扩大窗口大小以适应内容

    # 设置窗口透明度
    win.attributes("-alpha", 0.85)

    # 设置主题
    sv_ttk.set_theme("dark")

    # 创建主框架
    main_frame = ttk.Frame(win, padding=10)
    main_frame.pack(fill="both", expand=True)

    # 创建输入区域框架
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill="x", padx=10, pady=10)

    # IP地址输入框
    ip_entry = ttk.Entry(input_frame, font=("Arial", 12))
    ip_entry.pack(side="left", fill="x", expand=True)
    ip_entry.bind('<Return>', lambda event: manual_analyze_ip(ip_entry.get()))

    # 查询按钮
    analyze_button = ttk.Button(input_frame, text="查询", command=lambda: manual_analyze_ip(ip_entry.get()))
    analyze_button.pack(side="left", padx=(5, 0))

    # 创建文本显示区域框架
    text_frame = ttk.Frame(main_frame)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 文本显示区域
    text_widget = Text(text_frame, wrap="word", font=("Arial", 10), state="disabled", background="#333",
                       foreground="#FFF")
    text_widget.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # 滚动条
    scrollbar = Scrollbar(text_frame, command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    text_widget['yscrollcommand'] = scrollbar.set

    # 创建按钮区域框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill="x", padx=10, pady=10)

    # 模式选择下拉菜单
    mode_var = StringVar(win)
    mode_var.set("在线模式（B站源）")
    modes = ["在线模式（B站源）",
             "在线模式（ipinfo.io-限速）",
             "在线模式（ipstack）",
             "离线模式"]
    mode_dropdown = ttk.Combobox(button_frame, textvariable=mode_var, values=modes, state="readonly",
                                 width=15)  # 保持宽度不变
    mode_dropdown.pack(side="left", fill="x", expand=True)

    # 清空按钮
    clear_button = ttk.Button(button_frame, text="清空", command=clear_text)
    clear_button.pack(side="left", padx=(5, 0))

    # 设置窗口关闭事件
    win.protocol('WM_DELETE_WINDOW', on_exit)


threading.Thread(target=clipboard_monitor, daemon=True).start()
threading.Thread(target=icon.run, daemon=True).start()

create_window()
win.mainloop()
