import os
import socket
import hashlib
import base64
import sys
import time
from Crypto import Random
from Crypto.Cipher import AES

# Authentication: SHA256
# Encryption: AES256
## ================== OPTIONS ================== ##
HOST = "localhost"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
Encryption_Pass = ""  # AES256 Encryption Password For Messages
## ============================================= ##



class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def Pass_Converter(PASS):
    secret_thing = hashlib.sha256()
    secret_thing.update(PASS.encode())
    ENC_Auth = secret_thing.hexdigest()
    return ENC_Auth


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



clear()
AES_HASH = AESCipher(Encryption_Pass)
Authenticated = False



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        input("Server Is Not Active!\nPress Enter To EXit...")
        sys.exit()
    while True:
        if not Authenticated:
            data = s.recv(1024)
            # PASS = input(data.decode())
            PASS = input("Password: ")
            ENC_Auth = Pass_Converter(PASS)
            s.send(ENC_Auth.encode())
            if s.recv(1024).decode() == "Welcome":
                clear()
                print("Welcome To The Server...")
                print('listening on port:', s.getsockname()[1])
                
                Authenticated = True

            else:
                Authenticated = False
                input("Wrong Password...\nPress Enter To EXit...")
                clear()
                sys.exit()
        else:
            try:
                data = s.recv(1024)
                data_dec = AES_HASH.decrypt(data.decode())
                if data_dec == "KEEPALIVE":
                    pass
                else:
                    print(data_dec)
            except ValueError:
                s.close()
                break
print("Connection Closed...")
