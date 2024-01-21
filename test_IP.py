# 测试脚本

# 导入提取IP地址的函数
from extract_ips import extract_ips

# 定义测试文本
test_text = "Sample text with IPv6 address: 2001:db8::1 and IPv4 address: 192.168.1.1. Another IPv6 address: 2001:db8::2."

# 调用提取IP地址的函数
result = extract_ips(test_text)

# 打印提取的IP地址
print("Extracted IP Addresses:")
for i, ip in enumerate(result, start=1):
    print(f"{i}. {ip}")
