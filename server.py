import socket
import threading
import os

class Server:
    
    #Constructor de la clase ========================================
    def __init__(self, host, port):
        os.system('clear')
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    
    #Inicializador del script ========================================
    def start(self):
        self.server_socket.listen(5)
        print("Servidor escuchando en {}:{}".format(self.host, self.port))
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_name = client_socket.recv(1024).decode("utf-8")


                print("\n\nNueva conexión de {}:{}".format(client_address[0], client_address[1]))
                print("Participante: {}".format(client_name))

                #Añadimos el nuevo participante a la lista
                self.clients.append({"name": client_name, "socket": client_socket})


                client_thread = threading.Thread(target = self.handle_client, args=(client_socket,))
                client_thread.start()


        except KeyboardInterrupt:
            os.system('clear')
            print("Servidor detenido.")
            self.server_socket.close()

        except OSError as err:
            os.system('clear')
            print("error:", err)
            self.server_socket.close()










    #Obtener datos  del mensaje y determinar qué metodo procesa la salida del mensaje: ==========================
    def handle_client(self, client_socket):
        #encuentra quien envia el msj===================
        for client in self.clients:
            if client["socket"] == client_socket:
                sender_name = client["name"] + ": "
                break


        while True:
            data = client_socket.recv(1024)


            if not data:
                break

            message = data.decode("utf-8")

            if message.startswith("@"):
                recipient, message = message.split(":", 1)
                recipient = recipient[1:]
                

                print(recipient)

                if recipient == "server": #consola del servidor
                    self.send_message_to_server(sender_name, message)
                
                else: #consola de participante específico
                    self.send_message_to_client(sender_name, recipient, message)
            
            else: #consola de todos los participantes
                self.broadcast(message, client_socket)

        client_socket.close()
        self.clients.remove(client_socket)




#Metodos para imprimir en consola ya sea la del server, cliente1, cliente2, ....
    def send_message_to_server(self, sender_name, message):
        print(sender_name, message)

            
    
    def send_message_to_client(self, sender_name, recipient, message):
        for client in self.clients:
            if client["name"] == recipient:
                client["socket"].send(message.encode("utf-8"))
                break


    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client["socket"] != sender_socket:
                client["socket"].send(message.encode("utf-8"))





#Bloque de entrada e inicio del script =========================================
if __name__ == "__main__":
    server = Server('127.0.0.1', 9999)
    server.start()