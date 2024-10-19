from socket import *
import threading
import queue
import time

# Server setup
serverPort = 50000
serverIP = "192.168.6.57"
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

# Global variables
Clients = {}
Passkey = "12345"
message_queue = queue.Queue()  # Queue to store received messages for processing

def receive():
    while True:
        try:
            time.sleep(1)
            message, clientAddress = serverSocket.recvfrom(2048)
            decoded_message = message.decode()
            message_queue.put((clientAddress, decoded_message))
        except Exception as e:
            print(f"Error receiving message: {e}")

def broadcast(message, senderaddress=None):
    for user in Clients:
        if user != senderaddress:
            try:
                serverSocket.sendto(message.encode(), user)
            except OSError as e:
                print(f"Error sending message to {user}: {e}")

def remove(clientAddress):
    if clientAddress in Clients:
        username = Clients[clientAddress]
        print(f"Removing client {username}({clientAddress}) from the chatroom")
        del Clients[clientAddress]
        broadcast(f"{username} has left the chatroom", clientAddress)

def handle():
    while True:
        try:
            if not message_queue.empty():
                clientAddress, decoded_message = message_queue.get()

                if clientAddress not in Clients:
                    # Passkey
                    if decoded_message == Passkey:
                        serverSocket.sendto("OK".encode(), clientAddress)

                        # Username
                        while True:
                            username, clientAddress = serverSocket.recvfrom(2048)
                            username = username.decode()

                            if username not in Clients.values():
                                Clients[clientAddress] = username
                                print(f"Client {clientAddress} joined with username: {username}")
                                broadcast(f"{username} has joined the session", clientAddress)
                                serverSocket.sendto("Berhasil".encode(), clientAddress)
                                break
                            else:
                                serverSocket.sendto("Username sudah dipakai".encode(), clientAddress)
                    else:
                        serverSocket.sendto("Wrong Passkey".encode(), clientAddress)
                        print(f"Client {clientAddress} gives wrong passkey access denied")
                else:
                    # Existing client message
                    username = Clients[clientAddress]

                    if decoded_message.lower() == "exit":
                        print(f"{username} has requested to leave the chatroom")
                        remove(clientAddress)
                        continue

                    print(f"Message from {username}: {decoded_message}")
                    broadcast(f"{username}: {decoded_message}", clientAddress)

        except Exception as e:
            print(f"An error occurred while handling message: {e}")
            continue


print("Server running . . .")


t1 = threading.Thread(target=receive)  
t2 = threading.Thread(target=handle)   

t1.start()
t2.start()

t1.join()
t2.join()