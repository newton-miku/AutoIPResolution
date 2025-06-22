# coding=utf-8
import subprocess
 
def cmd1():
    try:
        cmd = 'start cmd /k ping www.baidu.com'
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print("Command execution failed: " + str(e))
 
cmd1()
