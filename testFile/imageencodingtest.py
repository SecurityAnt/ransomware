import base64

# /////////////////////////////////////////////////////////////////////////////바이너리로 변환하기

# gif 테스트 https://frhyme.github.io/python-lib/imgs_to_gif/ <- 이미지 -> gif 변환 링크 : 시도하려고 하고있었

encoded_string = ''
with open("../ui/thanos1.gif", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

print(encoded_string)#print string to copy it (see step 2)

#이 방식으로는 안됨
with open("./newgif.gif",'wb') as gif_file:
    gif_file.write(encoded_string)


# png 테스트

# b_face = []
#
# with open("../ui/face.png", 'rb') as infile:
#     b_face = infile.read()

#print(b_face)

# //////////////////////////////////////////////////////////////////////////////gui에 출력하기
import tkinter
from testFile import thanos


tk = tkinter.Tk()


# png 테스트
#img =tkinter.PhotoImage(data=b_face)

#l = tkinter.Label(tk,image=img)
#l.pack()

# gif 테스트
l_thanos = thanos.AnimatedGIF(tk, "newgif.gif")


tk.mainloop()