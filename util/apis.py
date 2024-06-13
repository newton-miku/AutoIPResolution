# -*- coding:utf-8 -*-
'''
@Author: nEwt0n_m1ku
@contact: cto@ddxnb.cn
@Time: 2024/01/21 0021 14:36
@version: 1.0
'''
import requests
from requests.exceptions import SSLError

from util.trans2CHN import country_code_to_name, province_to_pinyin, city_to_pinyin, translate_city_names, net_type
from util.extract_ips import extract_ips


# import emoji
#
# def get_flag_emoji(country_code):
#     country_code = country_code.upper()
#     flag_emoji = ''.join(chr(127397 + ord(char)) for char in country_code)
#     flag_emoji = get_flag_emoji_1(emoji.demojize(flag_emoji).strip(':'))
#     print(flag_emoji)
#     return flag_emoji
#
# def get_flag_emoji_1(country_code):
#     # 转换国家代码为大写
#     country_code = country_code.upper()
#     # 使用emoji库来生成国旗emoji
#     flag_emoji = emoji.emojize(f":flag_{country_code.lower()}:")
#     print(emoji.emojize(':grinning_face_with_big_eyes:'))
#     print(emoji.emojize(':flag_china:'))
#     return flag_emoji

def parse_ip_info_ipinfo_io_OL(ip_info):
    ip = ip_info.get('ip', '')
    hostname = ip_info.get('hostname', '')
    city = ip_info.get('city', '')
    region = ip_info.get('region', '')
    country = ip_info.get('country', '')
    loc = ip_info.get('loc', '')
    org = ip_info.get('org', '')
    postal = ip_info.get('postal', '')
    timezone = ip_info.get('timezone', '')

    asn = ip_info.get('asn', {})
    asn_info = {
        'asn': asn.get('asn', ''),
        'name': asn.get('name', ''),
        'domain': asn.get('domain', ''),
        'route': asn.get('route', ''),
        'type': asn.get('type', ''),
    }

    company = ip_info.get('company', {})
    company_info = {
        'name': company.get('name', ''),
        'domain': company.get('domain', ''),
        'type': company.get('type', ''),
    }

    privacy = ip_info.get('privacy', {})
    privacy_info = {
        'vpn': privacy.get('vpn', False),
        'proxy': privacy.get('proxy', False),
        'tor': privacy.get('tor', False),
        'relay': privacy.get('relay', False),
        'hosting': privacy.get('hosting', False),
        'service': privacy.get('service', ''),
    }

    abuse = ip_info.get('abuse', {})
    abuse_info = {
        'address': abuse.get('address', ''),
        'country': abuse.get('country', ''),
        'email': abuse.get('email', ''),
        'name': abuse.get('name', ''),
        'network': abuse.get('network', ''),
        'phone': abuse.get('phone', ''),
    }

    segments = company_info['name'].split(": ")
    result = f"IP: {ip}\n" \
             f"国家(地区): {country_code_to_name.get(country, country)}\n" \
             f"地址：{country_code_to_name.get(country, country)}\t{province_to_pinyin.get(region, region)}\t{city_to_pinyin.get(city, city)}\n" \
             f"ASN类型: {net_type.get(asn_info['type'].upper(), asn_info['type'])}\n" \
             f"ISP: {translate_city_names(company_info['name'])}"
    # f"ISP: {company_info['name']}"
    print(result)
    return result


def fetch_ip_info_ipinfo_io_OL(ip_address):
    api_url = f"https://ipinfo.io/widget/demo/{ip_address}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        ip_info = response.json().get("data", {})
        # message = parse_ip_info(ip_info)
        message = parse_ip_info_ipinfo_io_OL(ip_info)
        return message

    except SSLError as ssl_err:
        # 尝试禁用SSL验证（仅限测试目的，不建议在生产环境中使用）
        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()
            ip_info = response.json().get("data", {})
            # message = parse_ip_info(ip_info)
            message = parse_ip_info_ipinfo_io_OL(ip_info)
            return message
        except requests.RequestException as e:
            return f"解析{ip_address}失败. 错误: {e} (尝试禁用SSL验证后仍然失败)\n"

    except requests.RequestException as e:
        return f"解析{ip_address}失败. 错误: {e}"


def parse_ip_info_ipstack(ip_info):
    ip = ip_info.get('ip', '')
    country_code = ip_info.get('country_code', '')
    country_name = ip_info.get('country_name', '')
    region_code = ip_info.get('region_code', '')
    region_name = ip_info.get('region_name', '')
    city = ip_info.get('city', '')
    asn_info = ip_info.get('connection', {}).get('asn', '')
    isp = ip_info.get('connection', {}).get('isp', '')
    timezone = ip_info.get('time_zone', {}).get('code', '')
    currency_code = ip_info.get('currency', {}).get('code', '')
    currency_name = ip_info.get('currency', {}).get('name', '')
    latitude = ip_info.get('latitude', '')
    longitude = ip_info.get('longitude', '')

    # Format the output message
    result = f"IP地址: {ip}\n" \
             f"国家(地区): {country_name}\n" \
             f"地址: {region_name} {city}\n" \
             f"ASN: {asn_info}\n" \
             f"ISP: {isp}\n" \
             f"货币: {currency_code}\n" \
             f"经度: {longitude}\n" \
             f"纬度: {latitude}\n\n"

    print(result)
    return result


def fetch_ip_info_ipstack(ip_address):
    access_key = "5110837e247b8be749dee17ceb09f193"
    api_url = f"https://api.ipstack.com/{ip_address}?access_key={access_key}&language=zh"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        ip_info = response.json()
        # message = parse_ip_info(ip_info)
        message = parse_ip_info_ipstack(ip_info)
        return message

    except SSLError as ssl_err:
        # 尝试禁用SSL验证（仅限测试目的，不建议在生产环境中使用）
        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()
            ip_info = response.json()
            # message = parse_ip_info(ip_info)
            message = parse_ip_info_ipstack(ip_info)
            return message
        except requests.RequestException as e:
            return f"解析{ip_address}失败. 错误: {e} (尝试禁用SSL验证后仍然失败)\n"

    except requests.RequestException as e:
        return f"解析{ip_address}失败. 错误: {e}"


def parse_ip_info_bili(ip_info):
    addr = ip_info.get("addr", "")
    country = ip_info.get("country", "")
    province = ip_info.get("province", "")
    city = ip_info.get("city", "")
    isp = ip_info.get("isp", "")

    result = f"IP: {addr}\n国家: {country}\n地址：{province} {city}\nISP: {isp}"

    return result


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

    except SSLError as ssl_err:
        # 尝试禁用SSL验证（仅限测试目的，不建议在生产环境中使用）
        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()
            ip_info = response.json().get("data", {})
            message = parse_ip_info(ip_info)
            return message
        except requests.RequestException as e:
            return f"解析{ip_address}失败. 错误: {e} (尝试禁用SSL验证后仍然失败)"

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
    api_url = 'https://ipcity.market.alicloudapi.com/ip/city/query'
    headers = {
        'Authorization': 'APPCODE 0458686f0e70423a8a8fc3eb3d5f61ad',
    }

    # 设置请求参数，这里的ip和coordsys需要替换成你的实际值
    params = {
        'ip': f"{ip_address}",
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        ip_info = response.json().get("data", {})
        if ip_info is not None:
            # 添加额外字段
            ip_info['addr'] = f"{ip_address}"

            message = parse_ip_info(ip_info)
            return message
        else:
            return f"解析{ip_address}失败. 错误: 未获取到有效的IP信息\n"
    except SSLError as ssl_err:
        # 尝试禁用SSL验证（仅限测试目的，不建议在生产环境中使用）
        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()
            ip_info = response.json().get("data", {})
            if ip_info is not None:
                # 添加额外字段
                ip_info['addr'] = f"{ip_address}"

                message = parse_ip_info(ip_info)
                return message
            else:
                return f"解析{ip_address}失败. 错误: 未获取到有效的IP信息\n"
        except requests.RequestException as e:
            return f"解析{ip_address}失败. 错误: {e} (尝试禁用SSL验证后仍然失败)"

    except requests.RequestException as e:
        return f"解析{ip_address}失败. 错误: {e}\n"


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
            result_string = f"IP: {addr}\n国家: {country} {tz}\n地址：{province}\nISP: {isp}\n"
        else:
            result_string = f"IP: {addr}\n国家: {country} {tz}\n地址：{province} {city}\nISP: {isp}\n"
        return result_string

    except KeyError as e:
        return f"解析错误: 缺少关键字段 {e}"
    except Exception as e:
        return f"解析错误: {e}"


def analyze_ip(data_text, add_ip=False, mode="在线模式（B站源）"):
    ip_addresses = extract_ips(data_text)

    messages = []
    if ip_addresses:
        for ip_address in ip_addresses:
            if ip_address == "127.0.0.1":
                continue
            # 根据下拉框选择解析模式
            if mode == "在线模式（B站源）":
                message = fetch_ip_info_bili(ip_address)
            elif mode == "在线模式（数脉API-收费）":
                message = fetch_ip_info_ShuMai(ip_address)
            elif mode == "在线模式（ipinfo.io-限速）":
                message = fetch_ip_info_ipinfo_io_OL(ip_address)
            elif mode == "在线模式（ipstack）":
                message = fetch_ip_info_ipstack(ip_address)
            else:
                # 离线模式（ToDo）
                message = "该模式正在开发\n"

            # Add IP address to the message
            if add_ip:
                message_with_ip = {"ip_address": ip_address, "message": message}
                messages.append(message_with_ip)
                print("添加ip信息", add_ip, message_with_ip)
            else:
                messages.append(message)
    else:
        messages.append("未检测到有效IP地址")
    # print(messages)
    return messages


if __name__ == '__main__':
    results = analyze_ip(
        "Sample text with IPv6 address: 240e:bf:b800:4300:1::15 and IPv4 address: 223.5.5.5. Another IPv6 "
        "address:171.214.10.140, 119.84.174.67 2001:da8:4017:9002::3.", mode="在线模式（ipstack）")
    for i in results:
        print(i, "\n")
