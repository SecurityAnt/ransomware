import tkinter
from tkinter.ttk import *
from PIL import Image, ImageTk

setTime = 5
'''
class ExampleApp(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.label = Label(self, text="", width=10)
        self.label.pack()
        self.remaining = 0
        self.countdown(10)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(3, self.countdown)
'''

#frame쓰지말고 그냥해봐야될듯 _tkinter.TclError: unknown option "-fg" Error

class GUI():
    global getPW

    # window setting
    window = tkinter.Tk()
    window.root = tkinter.Tk()
    window.title("ransomware")
    window.state('zoomed')  # maximize the window
    window.resizable(False, False)
    window.configure(background="black")

     # 좌우 프레임으로 전체 화면 나눔
    leftFrame = Frame(window, relief="flat")
    leftFrame.pack(side="left", fill="both", expand=True)
    rightFrame = Frame(window, relief="flat")
    rightFrame.pack(side="right", fill="both", expand=True)

    # setting LeftFrame(Content)
    label1 = Label(leftFrame, text="타노스 랜섬웨어에 감염되었다.", fg="green", bg="black", font='Helvetica 14 bold')
    label2 = Label(leftFrame, text="파일을 정상적으로 복원하려면.", fg="green", bg="black", font='Helvetica 14 bold')
    label3 = Label(leftFrame, text="국민 123456-00-987654", fg="green", bg="black", font='Helvetica 18 bold')
    label4 = Label(leftFrame, text="으로 입급해라", fg="green", bg="black", font='Helvetica 14 bold')
    password = Entry(leftFrame)
    #getPW = password.get()  # 사용자가 입력한 pw
    #pwbutton = tkinter.Button(leftFrame, text="입력", command=self.clickBtn)

    '''
    ##Timer
    timer = Label(self.leftFrame, text="")
    timer.pack()
    timer.remaining = 0
    self.countdown(setTime)
    '''

    label1.pack()
    label2.pack()
    label3.pack()
    label4.pack()

    '''
    password.pack()
    pwbutton.pack()
    '''

    # setting RightFrame(Image)
    thanosImage = ImageTk.PhotoImage(self.rightFrame, file='face.png')
    imgLabel = Label(image=thanosImage)
    imgLabel.pack(side="center")


    # time countdown 함수
    def countdown(timer, remaining=None):
        if remaining is not None:
            timer.remaining = remaining

        elif timer.remaining == 0:
            timer.label.configure(text="파일이 절반 삭제됩니다.")
            # 파일 절반 삭제 함수 호출

        else:
            timer.label.configure(text="%d" % timer.remaining)
            timer.remaining = timer.remaining - 1
            timer.after(0, timer.countdown)

    # 버튼클릭시 복호화될수 있게
    # key 맞을때만 파괴하도록 수정해야 함
    def clickBtn(self):
        pw = getPW
        self.destroy()


if __name__ == "__main__":

    #app = ExampleApp()
    #app.mainloop()

    gui = GUI()
    gui.mainloop()  # gui 실행



    ''''
    # Add the path to a GIF to make the example working
    l = AnimatedGIF(window, "thanos1.gif")
    l.pack()
    '''
