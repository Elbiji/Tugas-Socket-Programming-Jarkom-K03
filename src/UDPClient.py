from socket import *
import threading

clientSocket = socket(AF_INET,SOCK_DGRAM)

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
            print( message.decode())
        except:
            break

def login():
    print("\n"*3)
    print("========================LOGIN========================")
    while True: 
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
    print("=======================USERNAME=======================")
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
        clientSocket.sendto(message.encode(),(serverName,serverPort))

serverName, serverPort = validation()
clientSocket.connect((serverName, serverPort))
print(f"Connected to server {serverName} on port {serverPort}")
login()


threading.Thread(target=receive_message, daemon=True).start()
handle()
print("=======================BYE BYE!=======================")
clientSocket.close()
  
