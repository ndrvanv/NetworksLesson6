#!/bin/python3
import socket
import threading

# Connection Data
# Данные для подключения
host = '127.0.0.54'
port = 1067

# Starting Server / Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames / Списки клиентов и их псевдонимов
clients = []
nicknames = []

# Sending Messages To All Connected Clients / Отправка сообещения
# всем подключившимся клиентам
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients / Отправка сообщений от клиентов
def handle(client):
    while True:
        try:
            # Broadcasting Messages / Рассылка сообщений
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients / Удаление и закрытие клиентов
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function / Получение и функция прослушивания
def receive():
    while True:
        # Accept Connection / Принятие подключения
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname / Запрос и сохранение псевдонима
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname / Вывод и рассылка псевдонима
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client / Запуск потока обработки от клиента
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
