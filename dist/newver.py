import re
from datetime import datetime, timedelta

# 读取file_version_info.txt文件
file_path = "file_version_info.txt"
with open(file_path, "r", encoding="utf-8") as file:
    file_content = file.read()

# 提取原始的ProductVersion和FileVersion
pattern_product_version = r"ProductVersion', '(\d+\.\d+\.\d+\.\d+)'"
pattern_file_version = r"FileVersion', '(\d+\.\d+\.\d+\.\d+)'"

match_product_version = re.search(pattern_product_version, file_content)
match_file_version = re.search(pattern_file_version, file_content)

if match_product_version and match_file_version:
    current_product_version = match_product_version.group(1)
    current_file_version = match_file_version.group(1)
else:
    print("无法提取当前版本号。")
    exit(1)

# 计算新的版本号
current_datetime = datetime.now()
new_version = current_datetime.strftime('%Y.%m.%d.%H%M')

# 更新文件内容
new_content = re.sub(pattern_product_version, f"ProductVersion', '{new_version}'", file_content)
new_content = re.sub(pattern_file_version, f"FileVersion', '{new_version}'", new_content)

# 将更新后的内容写回文件
with open(file_path, "w", encoding="utf-8") as file:
    file.write(new_content)

print(f"文件版本信息已更新：{new_version}")
