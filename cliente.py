import socket
import threading
from datetime import datetime
import sys

#Guardamos el input en una variable para mostrarlo más adelante
username = input("Por favor, introduzca su usuario: ")

#Pasamos la ip de nuestro host y el puerto que utilizara el socket mediante los argumentos pasados en el script
host = sys.argv[1] #127.0.0.1
port = int(sys.argv[2]) #55555

#Le pasamos dos parámetros: AF_INET(Indicamos que es de tipo internet) y SOCK_STREAM(Indicamos el protocolo TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conectamos el cliente al servidor en cuestion
client.connect((host, port))

#Obtenemos la fecha y hora actuales
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


#<----------------------------------------------------FUNCIONES----------------------------------------------------->


#Creamos una funcion encargada de recibir los mensajes
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8') #Decodificamos la información
            #Mandamos el mensaje pidiendo el usuario
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("Ups! Ha ocurrido un error...")
            client.close
            break


#Creamos una funcion encargada de escribir los mensajes para todos los usuarios conectados
def write_messages():
    while True:
        message = f"{username} {dt_string}: {input('')}"
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()