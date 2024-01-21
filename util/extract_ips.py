import re

def extract_ips(text):
    # 同时匹配IPv4和IPv6的正则表达式
    combined_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:?:(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # 提取匹配的IP地址
    matched_ips = re.findall(combined_pattern, text)

    return matched_ips
# def extract_ips(text):
#     # 正则表达式匹配IPv4地址
#     ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
#
#     # 正则表达式匹配IPv6地址
#     ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:?:(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}\b'
#
#     # 提取匹配的IP地址
#     ipv4_addresses = re.findall(ipv4_pattern, text)
#     ipv6_addresses = re.findall(ipv6_pattern, text)
#
#     return ipv4_addresses + ipv6_addresses