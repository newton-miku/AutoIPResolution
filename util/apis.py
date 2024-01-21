# -*- coding:utf-8 -*-
'''
@Author: nEwt0n_m1ku
@contact: cto@ddxnb.cn
@Time: 2024/01/21 0021 14:36
@version: 1.0
'''
import requests

from util.extract_ips import extract_ips


def parse_ip_info_bili(ip_info):
    addr = ip_info.get("addr", "")
    country = ip_info.get("country", "")
    province = ip_info.get("province", "")
    city = ip_info.get("city", "")
    isp = ip_info.get("isp", "")

    result = f"IP: {addr}\n国家: {country}\n地址：{province} {city}\nISP: {isp}"
    return result


def parse_ip_info(ip_info):
    try:
        if "result" in ip_info:
            # For parse_ip_info_ShuMai format
            result = ip_info.get("result", {})
            order_no = ip_info.get("orderNo", "")
            continent = result.get("continent", "")
            owner = result.get("owner", "")
            tz = result.get("timezone", "")
            country = result.get("country", "")
            province = result.get("prov", "")
            city = result.get("city", "")
            isp = result.get("isp", "")

        elif "addr" in ip_info:
            # For parse_ip_info_bili format
            order_no = ""
            continent = ""
            owner = ""
            tz = ""
            country = ip_info.get("country", "")
            province = ip_info.get("province", "")
            city = ip_info.get("city", "")
            isp = ip_info.get("isp", "")

        else:
            print(ip_info)
            raise ValueError("未知的数据格式")

        # Common fields
        addr = ip_info.get("addr", "")

        # You can add more common fields or handle them differently as needed
        if province == city:
            result_string = f"IP: {addr}\n国家: {country} {tz}\n地址：{province}\nISP: {isp}"
        else:
            result_string = f"IP: {addr}\n国家: {country} {tz}\n地址：{province} {city}\nISP: {isp}"
        return result_string

    except KeyError as e:
        return f"解析错误: 缺少关键字段 {e}"
    except Exception as e:
        return f"解析错误: {e}"


def fetch_ip_info_bili(ip_address):
    api_url = f"https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr?ip={ip_address}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        ip_info = response.json().get("data", {})
        message = parse_ip_info(ip_info)
        # message = parse_ip_info_bili(ip_info)
        return message

    except requests.RequestException as e:
        return f"解析{ip_address}失败. 错误: {e}"


def parse_ip_info_ShuMai(ip_info):
    try:
        data = ip_info["data"]
        result = data.get("result", {})

        order_no = data.get("orderNo", "")
        continent = result.get("continent", "")
        owner = result.get("owner", "")
        tz = result.get("timezone", "")
        country = result.get("country", "")
        province = result.get("prov", "")
        city = result.get("city", "")
        isp = result.get("isp", "")

        # You can add more fields as needed

        result_string = f"IP: {ip_info.get('addr', '')}\n国家: {country} {tz}\n地址：{province} {city}\nISP: {isp}"
        return result_string

    except KeyError as e:
        return f"解析错误: 缺少关键字段 {e}"
    except Exception as e:
        return f"解析错误: {e}"


def fetch_ip_info_ShuMai(ip_address):
    url = 'https://ipcity.market.alicloudapi.com/ip/city/query'
    headers = {
        'Authorization': 'APPCODE 0458686f0e70423a8a8fc3eb3d5f61ad',
    }

    # 设置请求参数，这里的ip和coordsys需要替换成你的实际值
    params = {
        'ip': f"{ip_address}",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        ip_info = response.json().get("data", {})
        if ip_info is not None:
            # 添加额外字段
            ip_info['addr'] = f"{ip_address}"

            message = parse_ip_info(ip_info)
            return message
        else:
            return f"解析{ip_address}失败. 错误: 未获取到有效的IP信息"

    except requests.RequestException as e:
        return f"解析{ip_address}失败. 错误: {e}"


def analyze_ip(data_text, add_ip=False, mode="在线模式（B站源）"):
    ip_addresses = extract_ips(data_text)

    messages = []
    if ip_addresses:
        for ip_address in ip_addresses:
            # 根据下拉框选择解析模式
            if mode == "在线模式（B站源）":
                message = fetch_ip_info_bili(ip_address)
            elif mode == "在线模式（数脉API-收费）":
                message = fetch_ip_info_ShuMai(ip_address)
            else:
                # 离线模式（ToDo）
                message = "该模式正在开发"

            # Add IP address to the message
            if add_ip:
                message_with_ip = {"ip_address": ip_address, "message": message}
                messages.append(message_with_ip)
            else:
                messages.append(message)
    else:
        messages.append("未检测到有效IP地址")
    # print(messages)
    return messages



if __name__ == '__main__':
    results = analyze_ip(
        "Sample text with IPv6 address: 240e:bf:b800:4300:1::15 and IPv4 address: 223.5.5.5. Another IPv6 "
        "address:171.214.10.140, 119.84.174.67 2001:da8:4017:9002::3.", "在线模式（数脉API-收费）")
    for i in results:
        print(i, "\n")
