import socket
import threading
import math
import json
import time

# Estructuras para almacenar jugadores y proyectiles
players = {}
projectiles = []
lock = threading.Lock()  # Evita que varios hilos accedan a la vez a los datos compartidos

# Manejar la conexión de un cliente
def handle_client(client_socket, addr):
    global projectiles, players, lock
    player_id = str(addr[1])  # Usa el puerto del cliente como un ID único
    with lock:
        players[player_id] = {"x": 0, "y": 0, "angle": 0, "is_alive": True, "name": f"Player_{player_id}"}

    try:
        while True:
            # Recibir mensaje del cliente
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            # Procesar datos del cliente
            message = json.loads(data)
            with lock:
                if message["type"] == "new_player":
                    # Registrar nuevo jugador
                    players[player_id] = {
                        "x": 0,
                        "y": 0,
                        "angle": 0,
                        "is_alive": True,
                        "name": message.get("name", f"Player_{player_id}")
                    }
                    print(f"Nuevo jugador conectado: {players[player_id]}")
                
                elif message["type"] == "position":
                    # Actualizar posición del jugador
                    if player_id in players:
                        players[player_id]["x"] = message["x"]
                        players[player_id]["y"] = message["y"]
                        players[player_id]["angle"] = message["angle"]
                        print(f"posición player: {players[player_id]}")

                elif message["type"] == "shot":
                    
                    # Agregar un nuevo proyectil
                    projectiles.append({
                        "x": message["x"],
                        "y": message["y"],
                        "angle": message["angle"],
                        "owner": player_id,
                        "max_distance": 600,  # Distancia máxima del proyectil
                        "traveled_distance": 0
                    })

            # Enviar el estado del juego al cliente
            with lock:
                game_state = {
                    "players": players,
                    "projectiles": projectiles
                }
            client_socket.sendall(json.dumps(game_state).encode("utf-8"))
            projectiles = []
            

    except Exception as e:
        print(f"Error manejando cliente {addr}: {e}")
    finally:
        # Limpiar datos al desconectar
        with lock:
            if player_id in players:
                del players[player_id]
        client_socket.close()
        print(f"Conexión cerrada con {addr}")

# Bucle principal del servidor
def run_server():
    server_ip = "127.0.0.1"
    port = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, port))
    server.listen()
    print(f"Server listening on {server_ip}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()



        time.sleep(1 / 60)  # Actualización a 60 FPS

# Iniciar servidor y bucle de juego
if __name__ == "__main__":
    run_server()
