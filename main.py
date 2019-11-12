from Crypto.Cipher import AES
import os


def get_tmp(in_filename):
    tmp = b''
    with open(in_filename, 'rb') as infile:
        tmp = infile.read()
    return tmp


def enc(key, in_filename, out_filename=None):
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

        print("")
        print("Initial Message was: ", data)

        # 패딩에 대한 부분 3
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length

        print("")
        print("After Padding Message was: ", data)
        # 결과로 b'file to encrypt\r\nHello Everyone'가 나온다

        with open(out_filename, 'wb') as outfile:
            encryptor = AES.new(key, mode, iv)
            e_data = encryptor.encrypt(data)
            # 그럼 e_data도 마찬가지로 b''형식이다.
            print("")
            print("e_data Message was: ", e_data)

            outfile.write(e_data)

    # writh가 완료된 상태에서 out_file을 읽어보자
    with open(out_filename, 'rb') as result:
        print("")
        print(out_filename, "내용은", result.read())


def dec(x, key, in_filename, out_filename):
    mode = AES.MODE_CBC
    iv = b'Sixteen byte iv3'

    with open(in_filename, 'rb') as infile:
        e_data = infile.read()
        print("")
        print("Cipher was: ", e_data)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(key, mode, iv)
            d_data = decryptor.decrypt(e_data)

            print("")
            print("어쩌구 전 d_data", d_data)

            # 패딩 처리한 부분을 다시 지워준다
            # d_data = e_data[:-x[-1]] 에서 x[-1]의 값은 100
            # 바이트 크기로 인식하기 때문에 d->ascii->100
            test = str(x)[-2]
            d_data = d_data[:d_data.rfind(x[-1]) + 1]

            print("")
            #####print("어쩌구 후 d_data: ", d_data.decode('ascii'))
            ##target의 내용이 한글인 경우 에러발생
            print(d_data.decode(encoding='utf-8'))

            outfile.write(d_data)

    # writh가 완료된 상태에서 out_file을 읽어보자
    with open(out_filename, 'rb') as result:
        print("")
        print(out_filename, "내용은", result.read())


def main():
    key = b'Sixteen byte key'

    in_filename = 'target.txt'

    x = get_tmp(in_filename)

    enc(key, in_filename, out_filename='target_enc.antdd')

    print("---")
    dec(x, key, 'target_enc.antdd', out_filename='target_dec.txt')

    # data = b'testest'

    # e_cipher = AES.new(key, AES.MODE_CBC)
    # e_data = e_cipher.encrypt(data)

    # d_cipher = AES.new(key, AES.MODE_CBC, e_cipher.nonce)
    # d_data = d_cipher.decrypt(e_data)

    # print("Encryption was: ", e_data)
    # print("Original Message was: ", d_data)


main()