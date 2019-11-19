import os
import shutil

def list_files(path, ext=None):
    filelist=[]
    print("os.listdir(): ", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path,name)):
            if name.endswith('.py'):
                continue
            if (ext == None):
                filelist.append(name)
            elif name.endswith(ext):
                filelist.append(name)

    print("filelist: ", filelist)
    return filelist

file = "tkintertest.exe"
src = os.getcwd()
dst = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
src_file = os.path.join(src, file)
dst_file = os.path.join(dst, file)

list_files(src)

print(src_file)
print(dst_file)
shutil.copyfile(src_file, dst_file)

