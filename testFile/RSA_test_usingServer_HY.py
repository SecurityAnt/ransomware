from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#개인키 읽어와서 return
def ReadPEM():
    h = open("","r") #파일로 저장했던 개인키 불러오기 PEM 파일 경로로 넣기
    privateKey = RSA.import_key(h.head())
    h.close();
    return privateKey;

def rsa_enc(msg):
    privateKey = ReadPEM()
    publicKey = privateKey.publickey()

    encryptor = PKCS1_OAEP.new(publicKey)
    encrypted = encryptor.encrypt(msg)

    return encrypted

def rsa_dec(msg):
    privateKey = ReadPEM()

    decryptor = PKCS1_OAEP.new(privateKey)
    decrypted = decryptor.decrypt(msg)

    return decrypted

if __name__ == '__main__':
    msg = bytes("abcd", "utf8") #나중에 AES 키로 변경해야 함.
    ENCtext = rsa_enc(msg)
    DECtext = rsa_dec(ENCtext)

    print(ENCtext)
    print(DECtext)