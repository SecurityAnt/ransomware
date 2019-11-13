#파이썬 한글 인코딩 문제를 해결하기 위함
#맨처음 시도는 그냥 문자열을 삽입해둔 상태에서 진행
#다음에는 텍스트 파일을 읽어보고 확인하는걸로
#다음에는 사진 파일을 읽어올 수 있는지 확인
import sys
from PIL import Image

def simple_str():
    print("")
    print("---START simple_str")
    english = "english = hi everyone"
    korean = "korean = 안녕 여러분"
    number = "number = 01094243045"
    mixall = "mixall = asdfghjk \n짱구는 \'부리부리부리부리\'\n2019-11-13"

    print("  >>오리지날")
    print(english)
    print(korean)
    print(number)
    print(mixall)

    print("  >>인코딩")
    print(english.encode())
    print(korean.encode())
    print(number.encode())
    print(mixall.encode())

    print("  >>디코딩")
    print(english.encode().decode())
    print(korean.encode().decode())
    print(number.encode().decode())
    print(mixall.encode().decode())

    print("  >>인코딩 그냥 하고 디코딩 utf-8으로 출력하면")
    print(english.encode().decode('utf-8'))
    print(korean.encode().decode('utf-8'))
    print(number.encode().decode('utf-8'))
    print(mixall.encode().decode('utf-8'))

    print("  >>인코딩 그냥 하고 디코딩 utf-8으로 출력하면")
    print(english.encode().decode('utf-8'))
    print(korean.encode().decode('utf-8'))
    print(number.encode().decode('utf-8'))
    print(mixall.encode().decode('utf-8'))

    print("---END simple_str")

def text_file(in_filename):
    print("")
    print("---START text_file")
    tmp = b''
    with open(in_filename, 'rb') as infile:
        tmp = infile.read()

    print(tmp)
    print(tmp.decode(encoding='utf-8'))
    #print(tmp.decode(encoding='ascii'))

    print("---END text_file")

def main():
    print(sys.stdin.encoding)
    print(sys.stdout.encoding)

    simple_str()
    #text_file('encoding_test.txt')

    '''
        if(english.encoding=='utf-8'):
        print('utf-8')
    if (english.encoding == 'ascii'):
        print('ascii')
    if (english.encoding == 'CP949'):
        print('CP949')
        '''

main()

