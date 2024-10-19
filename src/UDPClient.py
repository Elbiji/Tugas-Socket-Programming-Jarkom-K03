
from socket import *
import threading

serverName = " 192.168.1.7"
serverPort = 5000
clientSocket = socket(AF_INET,SOCK_DGRAM)

def encrypt(message): #+5
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            # Shift within the bounds of uppercase and lowercase letters
            start = ord('A') if char.isupper() else ord('a')
            encrypted_message += chr((ord(char) - start + 5) % 26 + start)
        else:
            encrypted_message += char  # Non-alphabetical characters remain unchanged
    return encrypted_message

def decrypt(message):#-5
    return encrypt(message, -5)  # Decrypt by shifting backwards
    
def receive_message():
    while True:
        try:
            encMessage, _ = clientSocket.recvfrom(2048)
            decMessage = decrypt(encMessage.decode())
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
    encMessage = encrypt(message)
    clientSocket.sendto(encMessage.encode(),(serverName,serverPort))


