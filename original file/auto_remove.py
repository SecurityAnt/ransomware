import getpass
import shutil
import os

def auto_remove():
    username = getpass.getuser()#컴퓨터 사용자 이름
    print(username)

    #나중에 exe파일 만들면 파일 이름 바꿔야함!1
    file = os.path.join(r'C:\Users', username, 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\tkintertest.exe')
    print(file)

    #파일 존재시 삭제
    if os.path.isfile(file):
        os.remove(file)
    else:
        print('삭제 할 파일이 없습니다.')

auto_remove()