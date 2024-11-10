import socket
import threading

# lokal adress och port
HOST = '127.0.0.1'
PORT = 54328

# sparar client och chattare i listor
clients = []
nicknames=[]

# TCP socket
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT))
server.listen()

# gör så att alla chattare får meddelanden
def broadcast (message):
    for client in clients:
        client.send(message)


def handle (client):
    while True:
        try: # chattaren skickar ut meddelanden
            message= client.recv(1024)
            broadcast(message)
        except: # tar bort en chattare
            index = clients.index(client)
            clients.remove (client)
            client.close()
            nickname= nicknames[index]
            broadcast(f'{nickname} lämnade chatten'.encode('utf-8')) # utf-8 gör så att man tex kan använda åäö
            nicknames.remove(nickname)
            break

# tar emot nya klienter
def receive():
    while True: # accepterar en ny klient och ger en address
        client, adress = server.accept()
        print(f"Connected with'{str(adress)}")

        # fråga om klienten kan uppge ett chattnamn
        client.send('NICK'.encode('utf-8'))
        nickname= client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        # skriver ut den nya chattaren namn, att den kom in i chatten samt att den är uppkopplad.
        print(f'Chattarens namn är:{nickname}.')
        broadcast(f'{nickname} kom in i chatten!'.encode('utf-8'))
        client.send('Kopplades upp till servern'.encode('utf-8'))

        # skapar en ny tråd för den nya chattaren
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# visar att servern lyssnar.
print("Servern Lyssnar..")
receive()