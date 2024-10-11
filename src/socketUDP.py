from socket import *
import time
import random
import threading
import queue

serverPort = 50000
serverIP ="***"
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))
print("Server bilangan acak")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(str(message.decode())+" dari:"+str(clientAddress))
    bilAcak = random.randint(6,20)
    time.sleep(1)
    serverSocket.sendto(str(bilAcak).encode(),clientAddress)
