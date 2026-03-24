#! /usr/bin/env python3

import os
import json

# log_line = '{"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "message": "系统巡检完成", "details": {"cpu_usage": 45, "memory_usage": 70}}'

# # 将字符串转为Python字典
# log_data = json.loads(log_line)

# print(f"日志时间: {log_data['timestamp']}")
# print(f"日志级别: {log_data['level']}")
# print(f"日志消息: {log_data['message']}")
# print(f"CPU使用率: {log_data['details']['cpu_usage']}%")
# print(f"内存使用率: {log_data['details']['memory_usage']}%")

# # 注意这个细节
# if log_data["details"]["cpu_usage"] > 80:
#     print("警告：CPU使用率过高！")

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
server_log_path = os.path.join(current_dir, "mock", "server.log")

server_logs = {}
with open(server_log_path, "r", encoding="utf-8") as f:
    for line in f:
        # 将每一行日志字符串转为Python字典
        log_entry = json.loads(line)
        # 获取日志中的IP地址
        ip = log_entry["ip"]

        # 统计每个IP地址出现的次数
        if ip in server_logs:
            server_logs[ip] += 1
        else:
            server_logs[ip] = 1

print("服务器访问统计：")
for ip, count in server_logs.items():
    print(f"{ip}: {count}次访问")
