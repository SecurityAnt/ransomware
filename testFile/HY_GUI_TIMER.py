from tkinter import *

def newWindow():
    Toplevel(window)

window = Tk()
window.title("ransomware")
window.state('zoomed')  # maximize the window

window.configure(background="black")

btn = Button(window, text='누르세요',  command = newWindow)
btn.pack()


window.mainloop()
