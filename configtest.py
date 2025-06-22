# -*- coding:utf-8 -*-
'''
@Author: nEwt0n_m1ku
@contact: cto@ddxnb.cn
@Time: 2024/06/14 0014 17:56
@version: 1.0
'''
import os
import configparser


def create_config_file(filename, content):
    # 获取用户主目录
    user_home = os.path.expanduser("~")

    # 构建配置文件路径
    config_dir = os.path.join(user_home, ".config")
    config_file_path = os.path.join(config_dir, filename)

    # 创建配置目录（如果不存在）
    os.makedirs(config_dir, exist_ok=True)

    # 创建并写入配置文件
    with open(config_file_path, "w") as config_file:
        config_file.write(content)

    print(f"配置文件已创建: {config_file_path}")
    return config_file_path


def read_and_print_config(filename):
    # 获取用户主目录
    user_home = os.path.expanduser("~")

    # 构建配置文件路径
    config_file_path = os.path.join(user_home, ".config", filename)

    # 检查配置文件是否存在
    if not os.path.exists(config_file_path):
        print(f"配置文件不存在: {config_file_path}")
        return

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # 打印配置文件内容
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")


# 示例配置内容
config_content = """
[settings]
theme = dark
autostart = true
"""

# 创建配置文件
config_file_path = create_config_file("my_config.ini", config_content)

# 读取并打印配置文件内容
read_and_print_config("my_config.ini")

