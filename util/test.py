# -*- coding:utf-8 -*-
'''
@Author: nEwt0n_m1ku
@contact: cto@ddxnb.cn
@Time: 2024/01/21 0021 15:11
@version: 1.0
'''


def parse_ip_info(ip_info):
    try:
        if "data" in ip_info and "result" in ip_info["data"]:
            # For parse_ip_info_ShuMai format
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

        elif "data" in ip_info and "addr" in ip_info["data"]:
            ip_info = ip_info["data"]
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
            raise ValueError("未知的数据格式")

        # Common fields
        addr = ip_info.get("addr", "")

        # You can add more common fields or handle them differently as needed

        result_string = f"IP: {addr}\n国家: {country} {tz}\n地址：{province} {city}\nISP: {isp}"
        return result_string

    except KeyError as e:
        return f"解析错误: 缺少关键字段 {e}"
    except Exception as e:
        return f"解析错误: {e}"


# Example usage:
ip_info_shumai = {
    "msg": "成功",
    "success": "true",
    "code": 200,
    "data": {
        "orderNo": "169703776398135646",  # 订单号
        "result": {
            "continent": "亚洲",  # 大洲
            "owner": "中国联通",  # 所属机构
            "country": "中国",  # 国家
            "lng": "120.208335",  # 经度
            "adcode": "330100",  # 行政编码
            "city": "杭州市",  # 城市
            "timezone": "UTC+8",  # 时区
            "isp": "中国联通",  # 运营商
            "accuracy": "城市",  # 精度
            "source": "数据挖掘",  # 采集方式
            "asnumber": "4837",  # 自治域编码
            "areacode": "CN",  # 国家编码
            "zipcode": "310002",  # 邮编
            "radius": "129.2092",  # 定位半径
            "prov": "浙江省",  # 省份
            "lat": "30.255611"  # 纬度
        }
    }
}

ip_info_bili = {
    "code": 0,
    "msg": "",
    "message": "",
    "data": {
        "addr": "223.5.5.5",
        "country": "ALIDNS.COM",
        "province": "ALIDNS.COM",
        "city": "",
        "isp": "阿里云",
        "latitude": "",
        "longitude": ""
    }
}

print(parse_ip_info(ip_info_shumai), "\n")
print(parse_ip_info(ip_info_bili), "\n")
