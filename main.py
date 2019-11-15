from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random  #RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP #RSA 최신버전(보안더좋음)
import glob
import os

def list_files(path, ext):
    filelist=[]
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path,name)):
            if name.endswith(ext):
                filelist.append(name)
    print("filelist: ", filelist)
    return filelist

def get_tmp(in_filename):
    tmp = b''
    with open(in_filename, 'rb') as infile:
        tmp = infile.read()
    return tmp

def enc(key, in_filename, out_filename=None):

    #RSA(최신버전인 PKCS1_OAEP)를 이용한 AES키를 public key 로 암호화
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    cipher = PKCS1_OAEP.new(rsa_key)
    ciphertext = cipher.encrypt(key)

    print("\nRSA를 통한 key 암호화문 : \n",ciphertext,"\n")
    #/////////////////////////////////////////////////


    print("---START ENCRYPTION : AES")
    mode = AES.MODE_CBC
    iv = b'Sixteen byte iv3'

    # enc의 결과로 나오는 파일 이름을 정한다
    if not out_filename:
        out_filename = in_filename + '.antdd'

    # 먼저, 바이너리 형식으로 파일을 읽어온다
    # 읽어온 것은 data로 저장

    with open(in_filename, 'rb') as infile:
        # 일단 읽어온 것을 출력해보자
        data = infile.read()

        print("1. Plain Message was: ")
        print(data)

        # 패딩에 대한 부분
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length

        print("2. After Padding Message was: ")
        print(data)

        with open(out_filename, 'wb') as outfile:
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


def dec(x, key, in_filename, out_filename):

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    print(out_filename)

    print("---START DECRYPTION : AES")

    mode = AES.MODE_CBC
    iv = b'Sixteen byte iv3'

    with open(in_filename, 'rb') as infile:
        e_data = infile.read()

        print("1. Cipher was: ")
        print(e_data)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(key, mode, iv)
            d_data = decryptor.decrypt(e_data)

            print("2. before unpadding d_data")
            print(d_data)

            # 패딩 처리한 부분을 다시 지워준다
            # d_data = e_data[:-x[-1]] 에서 x[-1]의 값은 100
            # 바이트 크기로 인식하기 때문에 d->ascii->100
            d_data = d_data[:d_data.rfind(x[-1]) + 1]

            #####print("어쩌구 후 d_data: ", d_data.decode('ascii'))
            ##target의 내용이 한글인 경우 에러발생
            #아스키코드로 진행된 경우

            print("3. after unpadding d_data")
            #print(d_data.decode(encoding='utf-8'))

            outfile.write(d_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    # 읽을 때 rb가 아니라 r로 읽으면
    # UnicodeDecodeError: 'cp949' codec can't decode byte 0xed in position 7: illegal multibyte sequence
    with open(out_filename, 'rb') as result:
        print("4. decryption result is: ", out_filename)
        print(result.read())

    print("---END DECRYPTION : AES")

def text(key, in_filename):

    print("TEXT FILE AES TEST")
    x = get_tmp(in_filename)
    enc(key, in_filename, out_filename=None)
    print("")
    dec(x, key, in_filename, out_filename=None)#in_filename은 복호화의 대상 파일이니 antdd 여야함

def image(key, in_filename):

    print("IMAGE FILE AES TEST")
    x = get_tmp(in_filename)
    enc(key, in_filename, out_filename=None)
    print("")
    dec(x, key, in_filename, out_filename=None)#in_filename은 복호화의 대상 파일이니 antdd 여야함

def main():
    key = b'Sixteen byte key'

    enc_targetlist = list_files(os.getcwd(), '.txt')
    for enc_target in enc_targetlist:
        enc(key, enc_target, out_filename=None)

    print("")
    dec_targetlist = list_files(os.getcwd(), '.antdd')
    for dec_target in dec_targetlist:
        x=get_tmp(os.path.splitext(dec_target)[0])
        dec(x, key, dec_target, out_filename=None) #x 없어야함

    #해당 파일들은 확인 끝남
    #text(key, 'target.txt')
    #text(key, '컴보.docx')
    #image(key, 'family.jpg')
    #image(key, '짱구얌.png')

main()
