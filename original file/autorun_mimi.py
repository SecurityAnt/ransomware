import getpass
import shutil
import os

def autorun():
    username = getpass.getuser()#컴퓨터 사용자 이름
    print(username)
    src = os.path.join(os.getcwd(), 'tkintertest.exe');
    #목적지는 항상 일치
    dst = os.path.join(r'C:\Users', username,'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    print(src)
    print(dst)
    shutil.copy2(src, dst)

autorun()