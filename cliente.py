import socket
import threading
import os

class Client:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.name.encode("utf-8"))



    def send_message(self, message):
        self.client_socket.send(message.encode("utf-8"))



    def receive_message(self):
        while True:

            data = self.client_socket.recv(1024)
            
            if not data:
                break
            
            #print(data.decode("utf-8"))

            message = data.decode("utf-8")
            print(message)







if __name__ == "__main__":
    os.system('clear')
    client_name = input("Ingresa tu nombre: ")
    print("====================\n")
    client = Client('127.0.0.1', 9999, client_name)

    receive_thread = threading.Thread(target=client.receive_message)
    receive_thread.start()

    while True:
        message = input()
        if message == "exit":
            break
        client.send_message(message)

    client.client_socket.close()
