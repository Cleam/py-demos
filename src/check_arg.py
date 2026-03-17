#! /usr/bin/env python3

import sys

# sys.argv 是一个列表，存放了你输入的命令行参数
# sys.argv[0] 是脚本名
# sys.argv[1] 是你传进来的第一个参数

if len(sys.argv) > 1:
    threshold = sys.argv[1]
    print(f"收到指令：检查阈值设定为 {threshold}%")
else:
    print("提示：你没有输入阈值，使用默认值 90%")
