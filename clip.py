import threading
import time
from tkinter import Tk, Text, Scrollbar, END, W, N, S, E

import pyperclip
import pystray
from PIL import Image
from pystray import MenuItem as item
from win11toast import toast

from getpath import get_all_res_path
from util.apis import analyze_ip


def clipboard_monitor():
    previous_clipboard_data = pyperclip.paste()

    while not exit_flag:
        current_clipboard_data = pyperclip.paste()

        if current_clipboard_data != previous_clipboard_data:
            # Clipboard content has changed
            print("Clipboard content changed: ", current_clipboard_data)

            messages = analyze_ip(current_clipboard_data)
            for message in messages:
                dis_info_to_all(message, icoPath)

            # Update the previous clipboard data
            previous_clipboard_data = current_clipboard_data

        # Check every 2 seconds
        time.sleep(1)


def dis_info_to_all(message, ico_path):
    display_information(message)
    toast("IP查询监控", message, lambda args: show_window(), str(ico_path))


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
