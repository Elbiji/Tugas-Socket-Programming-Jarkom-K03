from socket import *
import threading

serverName = "192.168.6.57"
serverPort = 50000
clientSocket = socket(AF_INET,SOCK_DGRAM)

def receive_message():
    while True:
        try:
            message, _ = clientSocket.recvfrom(2048)
            print("\n" + message.decode())
        except:
            break


while True:
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
    clientSocket.sendto(message.encode(),(serverName,serverPort))