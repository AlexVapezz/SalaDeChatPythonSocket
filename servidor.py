import socket
import threading
import sys

#Pasamos la ip de nuestro host y el puerto que utilizara el socket mediante los argumentos pasados en el script
host = sys.argv[1] #127.0.0.1
port = int(sys.argv[2]) #55555

#Le pasamos dos parámetros: AF_INET(Indicamos que es de tipo internet) y SOCK_STREAM(Indicamos el protocolo TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Pasamos los datos de conexion y hacemos que el servidor escuche a los clientes
server.bind((host, port))
server.listen()

#Para comprobar que se ha conectado he decidido añadir un mensaje por consola
print(f"El servidor esta online en {host}:{port}")

#Creamos las listas de clientes, donde guardaremos los clientes que se iran conectando, y
#la lista de usuarios, donde guardaremos sus nombres de usuario.
clients = []
usernames = []


#<----------------------------------------------------FUNCIONES----------------------------------------------------->


#Creamos la funcion compartir, que se encargara de compartir el mensaje publicado a todos los usuarios
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)


#A continuación crearemos una funcion encargada de manejar los mensajes de cada cliente
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024) #Establecemos el limite de peso del mensaje
            broadcast(message, client) #Compartimos el mensaje e indicamos quien lo comparte
        except:
            index = clients.index(client) #Obtenemos la posicion del cliente dentro de la lista
            username = usernames[index] #Accedemos a su nombre de usuario mediante el indice obtenido

            # Una vez se desconecte, mostramos un mensaje en el servidor
            broadcast(f"Servidor: {username} se ha desconectado".encode('utf-8'), client)
            clients.remove(client) #Eliminamos el cliente de la lista de clientes
            usernames.remove(username) #Eliminamos el nombre de usuario de la lista de usuarios
            client.close()
            break


#Creamos una funcion para recibir y aceptar los mensajes y las conexiones
def receive_connections():
    while True:
        client, address = server.accept() #Aceptamos la conexion

        client.send("@username".encode("utf-8")) #A continuacion obtenemos el nombre de usuario
        username = client.recv(1024).decode('utf-8')

        clients.append(client) #Añadimos el cliente a la lista
        usernames.append(username) #Añadimos su nombre de usuario a la lista

        #Muestro un mensaje para indicar que el usuario se conecto
        print(f"{username} conectado en {str(address)}")

        #Muestro un mensaje para indicar que el usuario se unio al chat
        message = f"Servidor: {username} Se ha unido al chat!".encode("utf-8")
        broadcast(message, client) #Compartimos el mensaje
        client.send("Bienvenido al servidor!".encode("utf-8")) #Muestro cuando me conecto al servidor

        #Vamos a crear un hilo para ejecutar la funcion manejar_mensajes para cada uno de los clientes
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()