# -*- coding:utf-8 -*-
'''
@Author: nEwt0n_m1ku
@contact: cto@ddxnb.cn
@Time: 2024/01/21 0021 14:55
@version: 1.0
'''
import os
import sys


# 获取资源文件路径
def get_current_path():
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return basedir


def get_all_res_path():
    basedir = get_current_path()
    pngPath = os.path.join(basedir, 'res\\原神H.png')
    icoPath = os.path.join(basedir, 'res\\原神H.ico')
    return pngPath, icoPath


if __name__ == '__main__':
    pngPath, icoPath = get_all_res_path()
    print(pngPath, icoPath)
