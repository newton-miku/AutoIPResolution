import threading
import time
import tkinter as tk
from tkinter import Tk, Text, Scrollbar, END, W, N, S, E, ttk, StringVar

import pyperclip
import pystray
from PIL import Image
from pystray import MenuItem as item
from win11toast import toast

from util.apis import analyze_ip
from getpath import get_all_res_path


def manual_analyze_ip(data_text):
    global mode_var
    mode = mode_var.get()
    messages = analyze_ip(data_text, mode)
    # clear_text()
    for message in messages:
        display_information(message)


def clipboard_monitor():
    previous_clipboard_data = pyperclip.paste()

    while not exit_flag:
        current_clipboard_data = pyperclip.paste()

        if current_clipboard_data != previous_clipboard_data:
            print("Clipboard content changed: ", current_clipboard_data)
            global mode_var
            mode = mode_var.get()
            results = analyze_ip(current_clipboard_data, True, mode)
            global icoPath
            for result in results:
                ip_address = result.get("ip_address", "N/A")
                message = result.get("message", "No message")
                dis_info_to_all(message, icoPath, ip_address)
            previous_clipboard_data = current_clipboard_data

        time.sleep(1)


def dis_info_to_all(message, ico_path, addr=None):
    display_information(message)
    if addr is not None:
        title = "IP查询监控-" + addr
    else:
        title = "IP查询监控"
    toast(title, message, lambda args: show_window(), str(ico_path), duration="short", app_id="IP查询监控")


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
print(pngPath, icoPath)
image = Image.open(pngPath)
icon = pystray.Icon("name", image, "IP地理位置查询", menu)
win = Tk()
win.title("IP地址解析")
win.geometry("400x400")

# 手动查询IP地址框（输入框）
ip_entry = tk.Entry(win)
ip_entry.grid(row=0, column=0, padx=10, pady=10, sticky=W + E)
# 绑定回车键事件
ip_entry.bind('<Return>', lambda event: manual_analyze_ip(ip_entry.get()))

# 添加查询按钮
analyze_button = tk.Button(win, text="查询", command=lambda: manual_analyze_ip(ip_entry.get()))
analyze_button.grid(row=0, column=1, padx=10, pady=10, sticky=W + E)

# 添加一个 Text 控件用于显示信息
text_widget = Text(win, wrap="word", width=40, height=10, state="disabled")
text_widget.grid(row=1, column=0, padx=10, pady=10, sticky=W + N + S + E)

# 添加一个滚动条
scrollbar = Scrollbar(win, command=text_widget.yview)
scrollbar.grid(row=1, column=1, sticky=N + S, rowspan=2, padx=(0, 10), pady=10)  # 调整 y 轴上的位置和高度

# 下拉框
mode_var = StringVar(win)
mode_var.set("在线模式（B站源）")  # 设置默认为在线模式
modes = ["在线模式（B站源）", "离线模式"]  # 模式列表
# modes = ["在线模式（B站源）", "在线模式（数脉API-收费）", "离线模式"]  # 模式列表
mode_dropdown = ttk.Combobox(win, textvariable=mode_var, values=modes, state="readonly", width=5)  # 调整width属性
mode_dropdown.grid(row=2, column=0, padx=10, pady=10, sticky=W + E)

# 添加清空按钮
clear_button = tk.Button(win, text="清空", command=clear_text)
clear_button.grid(row=2, column=1, padx=10, pady=10, sticky=W + E)

# 在垂直方向上配置 rowconfigure，以允许滚动条伸缩
win.rowconfigure(1, weight=1)

# 调整行列及大小
win.columnconfigure(0, weight=1)
win.columnconfigure(1, weight=1)
win.columnconfigure(2, weight=0)  # 不需要滚动条占用额外空间

win.attributes("-alpha", 0.85)  # 根据需要调整透明度值

# 重新定义点击关闭按钮的处理
win.protocol('WM_DELETE_WINDOW', on_exit)
# 在创建窗口后调用设置主题的函数
set_theme()

# 启动剪贴板监控线程
threading.Thread(target=clipboard_monitor, daemon=True).start()

# 启动托盘图标
threading.Thread(target=icon.run, daemon=True).start()

win.mainloop()
