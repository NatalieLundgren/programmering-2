import socket
import threading

# lokal address och port
HOST = '127.0.0.1'
PORT = 54328

#ange chattnamn
nickname= input ("Välj ett chattnamn:")

# ansluter klienter till servern
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# tar emot meddelande från servern
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message== 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ett fel har uppstått")
            client.close()
            break
# skriver och skickar meddelande till servern
def write():
    while True:
        message= f'{nickname}:  {input("")}'
        client.send(message.encode('utf-8'))

#tar emot tråd för att ta emot meddelande
receive_thread = threading.Thread(target=receive)
#starta en tråd för att ta emot meddelande
receive_thread.start()

# skapar en tråd för att skicka och skriva meddelande
write_thread = threading.Thread(target=write)
#startar en tråd
write_thread.start()