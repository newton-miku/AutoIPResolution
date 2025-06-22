@echo off
rem 编译程序
chcp 936
taskkill /im IP地址解析.exe /f
pipenv run pyinstaller.exe .\IP地址解析.spec
cd dist
python newver.py
rem 设置新版本号
pyi-set_version.exe .\file_version_info.txt .\IP地址解析.exe 

pause
