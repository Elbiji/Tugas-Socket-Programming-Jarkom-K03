
from socket import *
import threading

serverName = "192.168.1.7"
serverPort = 50000
clientSocket = socket(AF_INET,SOCK_DGRAM)
cont = False

def encrypt(message, shift,cont): #+5
    mark =':'
    encrypted_message = ""
    for char in message:
        if (char == mark or cont):
            cont = True
            if (char.isalpha()):
                # Shift within the bounds of uppercase and lowercase letters
                start = ord('A') if char.isupper() else ord('a')
                encrypted_message += chr((ord(char) - start + shift) % 26 + start)
            else:
                encrypted_message += char
        else:
            encrypted_message += char  # Non-alphabetical characters remain unchanged
    return encrypted_message

def decrypt(message,shift,cont):#-5
    return encrypt(message,shift,cont)  # Decrypt by shifting backwards

def validation():
    while True:
        try:
            ip = str(input("Masukkan IP Tujuan: "))
            inet_aton(ip)
            port = int(input("Masukkan Port Tujuan: "))
            if port < 1024 or port > 65535:
                    raise ValueError("Port number must be between 1024 and 65535")
            return ip, port
        except OSError:
            print("Invalid IP address format, please try again.")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")  

def receive_message():
    while True:
        try:
            message, _ = clientSocket.recvfrom(2048)
            encMessage = message.decode()
            decMessage = decrypt(encMessage,-5,cont)
            print("\n" + decMessage)
        except:
            break




def login():
    print("\n"*3)
    print("========================LOGIN========================")
    while True: #
        passkey = input("Masukkan Passkey: ")
        clientSocket.sendto(passkey.encode(),(serverName,serverPort))
        Response, _ =clientSocket.recvfrom(2048)
        if Response.decode() == 'OK':
            print("Passkey benar, kamu sudah masuk chatroom")
            username()
            break
        else:
            print(Response.decode())
def username():
    print("\n"*3)
    print("========================LOGIN========================")
    while True:
            username = input("Masukkan nama anda: ")
            clientSocket.sendto(username.encode(), (serverName,serverPort))
            receive_message, _ = clientSocket.recvfrom(2048)
            if receive_message.decode() == "Berhasil":
                print("Username accepted, joining the chatroom...")
                break
            else:
                print(receive_message.decode())

def handle():
    print("\n"*3)
    print("=======================CHATROOM=======================")
    while True:
        message = input("")
        if message.lower() == 'exit':
            clientSocket.sendto(message.encode(),(serverName,serverPort))
            break
        clientSocket.sendto(encrypt(message,5,True).encode(),(serverName,serverPort))

serverName, serverPort = validation()
clientSocket.connect((serverName, serverPort))
print(f"Connected to server {serverName} on port {serverPort}")
login()

threading.Thread(target=receive_message, daemon=True).start()

handle()
print("=======================BYE BYE!=======================")
clientSocket.close()

