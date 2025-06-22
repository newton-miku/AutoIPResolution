import requests

url = 'http://ipcity.market.alicloudapi.com/ip/city/query'
headers = {
    'Authorization': 'APPCODE 0458686f0e70423a8a8fc3eb3d5f61ad',
}

# 设置请求参数，这里的ip和coordsys需要替换成你的实际值
params = {
    'ip': '1.12.225.197',
}

# 发送GET请求
response = requests.get(url, headers=headers, params=params, verify=False)

# 输出响应信息
print(f"Status Code: {response.status_code}")
print("Response Headers:")
for key, value in response.headers.items():
    print(f"{key}: {value}")
print("Response Body:")
print(response.text)
