import socket
import threading
import json

# Almacena jugadores conectados
players = {}

# Función para manejar la comunicación con cada cliente
def handle_client(client_socket, address):
    player_id = None  # Inicializa player_id fuera del bloque try
    try:
        # Recibir el nombre del jugador
        player_id = client_socket.recv(1024).decode('utf-8')
        players[player_id] = client_socket  # Almacenar el socket del jugador
        print(f"Jugador conectado: {player_id} desde {address}")

        while True:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if not data:
                break  # Salir si no se reciben más datos

            # Procesar el mensaje (aquí puedes añadir la lógica de movimiento)
            message = json.loads(data.decode('utf-8'))
            print(f"Recibido de {player_id}: {message}")

            # Aquí puedes manejar la lógica del juego, como actualizar posiciones

    except ConnectionResetError:
        print(f"Conexión perdida con el cliente: {address}")
    except Exception as e:
        print(f"Error en el manejo del cliente {player_id}: {e}")
    finally:
        # Asegurarse de eliminar al jugador de la lista
        if player_id in players:
            del players[player_id]
        client_socket.close()
        print(f"Jugador desconectado: {player_id}")

# Configuración del servidor
server_address = ('localhost', 5555)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print(f"Servidor escuchando en {server_address[0]}:{server_address[1]}")

while True:
    client_socket, address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()

