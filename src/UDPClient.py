from socket import *
import random
import string
import time

serverName = ""
serverPort = 50000
clientSocket = socket(AF_INET,SOCK_DGRAM)
message = input("Masukan nama anda:")
clientSocket.sendto(message.encode(),(serverName,serverPort))
while True:
    pesan, serverAddress = clientSocket.recvfrom(2048)
    message ="Permintaan acak"
    clientSocket.sendto(message.encode(),(serverName,serverPort))
    print("Bilangan Acak dari server("+str(serverAddress)+"): "+str(pesan.decode()))
