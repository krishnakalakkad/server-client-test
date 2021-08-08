import threading
import socket


host = '127.0.0.1' # localhost

port = 32332

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientlist = []
nicknamelist = []


def broadcast(message):
    for client in clientlist:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clientlist.index(client)
            clientlist.remove(client)
            client.close()
            nickname = nicknamelist[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknamelist.remove(nickname)
            break


def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode('ascii')
        nicknamelist.append(nickname)
        clientlist.append(client)

        print(f"nickname of the client is {nickname}!")
        broadcast(f'{nickname} has joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()