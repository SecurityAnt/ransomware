import tkinter
import time
from logging import root
from tkinter import messagebox, ttk

from tkinter import PhotoImage
from tkinter.ttk import Label
from PIL import Image, ImageTk

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


if __name__ == "__main__":

    window=tkinter.Tk()
    window.title("ransomware")
    window.state('zoomed')  # maximize the window
    height = window.winfo_height()  # ...
    width = window.winfo_width()
    window.configure(background="black")

    #버튼클릭시 복호화될수 있게
    def dec():
        pw=str(password.get())
        # Add the path to a GIF to make the example working
        l = AnimatedGIF(window, "thanos1.gif")
        l.pack()
        label5.destroy()
        #window.destroy()


    label1=tkinter.Label(window, text="타노스 랜섬웨어에 감염되었다.",fg="red",bg="black", font='Helvetica 14 bold')
    label1.pack()
    label2=tkinter.Label(window, text="1시간 안에 돈을 보내주지 않으면 파일이 삭제된다.", fg="red",bg="black", font='Helvetica 18 bold')
    label2.pack()
    label3=tkinter.Label(window, text="국민 786102-00-040854", fg="red",bg="black", font='Helvetica 18 bold')
    label3.pack()

    label4=tkinter.Label(window, text="password:",fg="red",bg="black", font='Helvetica 14 bold')
    label4.pack()
    password= tkinter.Entry(window)
    password.pack()

    pwbutton= tkinter.Button(window, text="복호화",command=dec)
    pwbutton.pack()

    image = tkinter.PhotoImage(file="face.png")

    label5 = tkinter.Label(window, image=image)
    label5.pack()

    window.mainloop()