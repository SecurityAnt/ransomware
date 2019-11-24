import os
#w자기자신도 삭제!!!
def remove():
    #최종파일이름 바꾸기
    dst=os.path.join(os.getcwd(),'remove.py')
    if os.path.isfile(dst):
        os.remove(dst)

remove()