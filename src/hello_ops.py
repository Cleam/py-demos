#! /usr/bin/env python3

import platform
import os

# 获取系统信息
sys_info = platform.system()
current_user = os.getlogin()

print("--- 自动化巡检启动 ---")
print(f"当前操作系统: {sys_info}")
print(f"执行人员: {current_user}")

if sys_info == "Linux":
    print("检测到Linux环境，运行正常")
else:
    print("当前环境非Linux，部分功能可能受限")
