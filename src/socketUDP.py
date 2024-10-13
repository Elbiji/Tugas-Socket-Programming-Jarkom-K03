from socket import *

serverPort = 50000
serverIP ="192.168.6.57"
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

Clients = {}
Passkey = "123"

print("Server is running . . . .")

while True:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)
        decoded_message = message.decode()

        if clientAddress not in Clients:
            if (decoded_message == Passkey):
                serverSocket.sendto("OK".encode(),(clientAddress))
                username, clientAddress = serverSocket.recvfrom(2048)
                Clients[clientAddress] = username.decode()
                print(f"Client {clientAddress} just joined with {Passkey}")
                print(f"Client {clientAddress} set their username as {Clients[clientAddress]}")
            else:
                serverSocket.sendto("Wrong Passkey".encode(),(clientAddress))
                print(f"Client {clientAddress} gives wrong passkey access denied")
        else:
            username = Clients[clientAddress]
            print(f"Message from {Clients[clientAddress]}: {decoded_message}")
            for user in Clients:
                if user != clientAddress:
                    serverSocket.sendto(f"{username}: {decoded_message}".encode(), user)

    except ConnectionError as e:
        print(f"Connection reset by {clientAddress}: {e}")
        continue

