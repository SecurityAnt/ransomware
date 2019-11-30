import os

path = os.getcwd()

extlist = \
    ['doc', 'docx', 'txt', 'hwp', 'ppt', 'pptx', 'xlsx', 'xls', 'pdf',
     'jpg', 'jpeg', 'png', 'gif',
     'mp3', 'wav', 'wma',
     'psd', 'pdd', 'ai', 'dwg', 'dxf', '3dm','antdd']

def search_dir(file_list,dir_path):
    for name in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path,name)):
            for i in extlist:
                if name.endswith(i):
                    file_list.append(os.path.join(dir_path,name))
        elif os.path.isdir(os.path.join(dir_path,name)):
            search_dir(file_list,os.path.join(dir_path,name))

def test():
    file_list = []
    search_dir(file_list, path)
    for i in file_list:
        print(i)

test()

class Test:
    def test(self):
        file_list = []
        search_dir(file_list, path)
        for i in file_list:
            print(i)

    def search_dir(self,file_list, dir_path):
        for name in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, name)):
                for i in extlist:
                    if name.endswith(i):
                        file_list.append(os.path.join(dir_path, name))
            elif os.path.isdir(os.path.join(dir_path, name)):
                search_dir(file_list, os.path.join(dir_path, name))


test = Test()
test.test()

