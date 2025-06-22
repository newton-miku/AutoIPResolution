import maxminddb

# 替换为你的MaxMind DB文件路径
mmdb_file = 'C:\\Users\\13165\\desktop\\country_asn.mmdb'

# 打开MaxMind DB文件
with maxminddb.open_database(mmdb_file) as reader:
    # 查询IP地址
    ip_address = '240e:f:a00b::6'  # 要查询的IP地址
    # ip_address = '45.152.65.222'  # 要查询的IP地址
    try:
        # 查询IP地址的信息
        result = reader.get(ip_address)
        if result:
            print(result)
        else:
            print(f"No data found for IP address: {ip_address}")
    except maxminddb.InvalidDatabaseError as err:
        print(f"Invalid MaxMind DB file: {err}")
    except ValueError as err:
        print(f"Invalid IP address format: {err}")
