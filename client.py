import socket
import threading
import json

HOST = 'localhost'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

player_id = input("Introduce tu ID de jugador: ")
client_socket.send(player_id.encode('utf-8'))

def receive_updates():
    """Recibir las actualizaciones del servidor sobre las posiciones"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            data = json.loads(message)
            print(f"Actualización de jugadores: {data}")
            # Aquí puedes actualizar las posiciones en el minimapa o el juego
        except:
            break

def send_position(x, y):
    """Enviar la posición del avión al servidor"""
    data = {'type': 'move', 'x': x, 'y': y}
    client_socket.send(json.dumps(data).encode('utf-8'))

# Iniciar el hilo que recibe actualizaciones del servidor
receive_thread = threading.Thread(target=receive_updates)
receive_thread.start()

# Aquí va la lógica para enviar la posición del jugador cuando se mueva
while True:
    x = input("Introduce nueva posición X: ")
    y = input("Introduce nueva posición Y: ")
    send_position(x, y)
