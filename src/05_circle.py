#! /usr/bin/env python3

while True:
    user_query = input("请输入你的问题，输入“quit”退出：")
    if user_query.lower() == "quit":
        print("再见！")
        break

    print(f"你输入的问题是：{user_query}")
