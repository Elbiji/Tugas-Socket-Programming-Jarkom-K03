
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
    
def receive_message():
    while True:
        try:
            message, _ = clientSocket.recvfrom(2048)
            encMessage = message.decode()
            decMessage = decrypt(encMessage,-5,cont)
            print("\n" + decMessage)
        except:
            break


while True: #
    passkey = input("Masukkan Passkey: ")
    clientSocket.sendto(passkey.encode(),(serverName,serverPort))
    Response, _ =clientSocket.recvfrom(2048)
    if Response.decode() == 'OK':
        print("Passkey benar, kamu sudah masuk chatroom")
        break
    else:
        print(Response.decode())

username = input("Masukkan nama anda: ")
clientSocket.sendto(username.encode(), (serverName,serverPort))

threading.Thread(target=receive_message, daemon=True).start()

while True:
    message = input("")
    cont = True
    encMessage = encrypt(message,5,cont)
    cont =False
    clientSocket.sendto(encMessage.encode(),(serverName,serverPort))


