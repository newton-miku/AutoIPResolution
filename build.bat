@echo off
rem �������
chcp 936
pyinstaller.exe .\IP��ַ����.spec
cd dist
python newver.py
rem �����°汾��
pyi-set_version.exe .\file_version_info.txt .\IP��ַ����.exe

pause
