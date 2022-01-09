import re
import sys
import threading
import time
import hashlib
import socket
import os
from Crypto import Random
import base64
from Crypto.Cipher import AES

secret_thing = hashlib.sha256()

# Authentication: SHA256
# Encryption: AES256
## ================== OPTIONS ================== ##
HOST = "localhost"
PORT = 8080
Auth_PASS = ""
PASS_PHRASE = ""
## ============================================= ##
global EXIT_Validation
global EXIT_Connections
EXIT_Validation = 0
EXIT_Connections = 0
CONNECTIONS = {}
secret_thing.update(Auth_PASS.encode())
ENC_Auth = secret_thing.hexdigest()
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

my_socket.bind((HOST, PORT))
my_socket.listen()



def t():
    current_time = time.localtime()
    ctime = time.strftime('%H:%M:%S', current_time)
    return '[' + ctime + ']'


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


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def ShowClients():
    NUM = 0
    if len(CONNECTIONS) != 0:
        for client in CONNECTIONS:
            NUM += 1
            address = client[0]
            port = client[1]
            print(f"{NUM}) IP: {address} PORT: {port}")
    else:
        print("[-] No Client Available!")


def MessageClient(IP, PORT, Message):
    if len(CONNECTIONS) != 0:
        ENC_AES = AES_HASH.encrypt(Message)
        for client in CONNECTIONS:
            Ipaddress = client[0]
            IpPort = client[1]
            CONN = CONNECTIONS[client]
            if IP.strip() == Ipaddress and PORT.strip() == str(IpPort):
                CONN.send(ENC_AES)
                print("[+] Message Sent...")
    else:
        print("[-] No Client Available!")


def MessageAll(Message):
    ENC_AES = AES_HASH.encrypt(Message)
    for client in CONNECTIONS:
        CONNECTIONS[client].send(ENC_AES)
    print("[+] Message Sent To All Clients...")


def Validate_Connections():
    global EXIT_Validation
    DISCONNECTED = []
    KEEP_ALIVE = "KEEPALIVE"
    KEEP_ALIVE = AES_HASH.encrypt(KEEP_ALIVE)
    while EXIT_Validation != 1:
        time.sleep(1)
        for Client in CONNECTIONS:
            try:
                if EXIT_Validation != 1:
                    CONNECTIONS[Client].send(KEEP_ALIVE)
                else:
                    break
            except:
                DISCONNECTED.append(Client)
        for Client in DISCONNECTED:
            del CONNECTIONS[Client]
        DISCONNECTED.clear()
    print("Braked Validating")


def Connections():
    global EXIT_Connections
    my_socket.settimeout(5)
    Welcome = "Welcome".encode()
    while EXIT_Connections != 1:
        try:
            conn, addr = my_socket.accept()
            if conn:
                conn.send(b"Pass: ")
                PASS = conn.recv(1024)
                if PASS.decode() == ENC_Auth:
                    # When Auth Completed #
                    CONNECTIONS[addr] = conn
                    print(f"\n{t()} new connection from {addr} Connection: {len(CONNECTIONS)}")
                    conn.send(Welcome)
                else:
                    conn.close()
        except:
            pass
    print("Braked Connections")


def Selector():
    global EXIT_Validation
    global EXIT_Connections
    while True:
        options = """
       |===========================|
       |1) Show Clients            |
       |2) Message To <Client IP>  |
       |3) Message To All          |
       |4) Exit                    |
       |===========================|
        \n>"""
        try:
            OP = input(options)
            clear()
            if OP == "1":
                ShowClients()
            elif OP == "2":
                if len(CONNECTIONS) != 0:
                    ShowClients()
                    print()
                    IP = input("IP: ")
                    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", IP):
                        PORT = input("PORT: ")
                        if re.match(
                                r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$",
                                PORT):
                            Message = input("Message: ")
                            MessageClient(IP=IP, PORT=PORT, Message=Message)
                        else:
                            print("Wrong PORT!")
                    else:
                        print("Wrong IP Address!")
                else:
                    print("[-] No Client Available!")

            elif OP == "3":
                if len(CONNECTIONS) != 0:
                    Message = input("Message: ")
                    MessageAll(Message)
                else:
                    print("[-] No Client Available!")
            elif OP == "4":
                clear()
                EXIT_Validation = 1
                time.sleep(0.5)
                EXIT_Connections = 1
                print("Waiting 5 Seconds To Close All Threads")
                time.sleep(5)
                input("Press Enter To Close...")
                clear()
                sys.exit()
            elif OP == "clear" or OP == "cls":
                clear()
            else:
                input("\n[-] Wrong Option!")
        except KeyboardInterrupt:
            clear()
            EXIT_Validation = 1
            time.sleep(0.5)
            EXIT_Connections = 1
            print("Waiting 5 Seconds To Close All Threads")
            time.sleep(5)
            input("Press Enter To Close...")
            clear()
            sys.exit()


if __name__ == "__main__":
    clear()
    AES_HASH = AESCipher(PASS_PHRASE)
    Conn = threading.Thread(target=Connections)
    Validate = threading.Thread(target=Validate_Connections)
    Conn.start()
    Validate.start()

    Selector()
