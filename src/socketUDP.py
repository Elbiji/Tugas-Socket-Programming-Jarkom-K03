from socket import *
import threading
import queue
import time


serverPort = 50000
serverIP = "192.168.6.57"
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

Clients = {}
passkey_status = {} 
Passkey = "12345"
message_queue = queue.Queue()  
login_queue = queue.Queue()
passkey_queue = queue.Queue()

def receive():
    while True:
        try:
            time.sleep(1) # Delay to avoid racing conditions
            message, clientAddress = serverSocket.recvfrom(2048)
            decoded_message = message.decode()
            if clientAddress not in passkey_status or not passkey_status[clientAddress]:
                passkey_queue.put((clientAddress,decoded_message))
            elif clientAddress not in Clients:  
                login_queue.put((clientAddress, decoded_message))
            else:  
                message_queue.put((clientAddress, decoded_message))
        except Exception as e:
            print(f"Error receiving message: {e}")

def broadcast(message, senderaddress):
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
        del passkey_status[clientAddress]
        broadcast(f"{username} has left the chatroom", clientAddress)

def setup_username(clientAddress):
    while True:
        if not login_queue.empty():
            login_address, decoded_message = login_queue.get()
            if login_address == clientAddress and  decoded_message not in Clients.values():
                Clients[clientAddress] = decoded_message
                print(f"Client {clientAddress} joined with username: {decoded_message}")
                broadcast(f"{decoded_message} has joined the session", clientAddress)
                serverSocket.sendto("Berhasil".encode(), clientAddress)
                return decoded_message
            else:
                serverSocket.sendto("Username sudah dipakai".encode(), clientAddress)

def handle():
    while True:
        try:
            if not passkey_queue.empty():
                clientAddress, decoded_message = passkey_queue.get()

                if clientAddress not in Clients:
                    # Passkey
                    if decoded_message == Passkey:
                        serverSocket.sendto("OK".encode(), clientAddress)
                        passkey_status[clientAddress] = True
                        print(f"Client {clientAddress} entered the right passkey access granted")
                        setup_username(clientAddress)
                    else:
                        passkey_status[clientAddress] = False
                        serverSocket.sendto("Wrong Passkey".encode(), clientAddress)
                        print(f"Client {clientAddress} gives wrong passkey access denied")
        except Exception as e:
            print(f"An error occurred while handling message: {e}")
            continue

def handlechat():
    while True:
        try:
            if not message_queue.empty():
                clientAddress, decoded_message = message_queue.get()

                if clientAddress in Clients:
                    username = Clients[clientAddress]

                    if decoded_message.lower() == "exit":
                        print(f"{username} has requested to leave the chatroom")
                        remove(clientAddress)
                        continue

                    print(f"Message from {username}: {decoded_message}")
                    broadcast(f"{username}: {decoded_message}", clientAddress)
        except Exception as e:
            print(f"An error occured: {e}")


print("Server running . . .")


t1 = threading.Thread(target=receive)  
t2 = threading.Thread(target=handle)
t3 = threading.Thread(target=handlechat)
 

t1.start()
t2.start()
t3.start()


t1.join()
t2.join()
t3.join()
