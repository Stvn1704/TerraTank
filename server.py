import random
import socket
import threading
import math
import json
import time
import uuid  # For generating unique IDs
import socket

# Variables globales para manejar los jugadores y proyectiles
players = {}
projectiles = []
clients = [] # Lista de clientes conectados
lock = threading.Lock()  # Evita que varios hilos accedan a la vez a los datos compartidos

# Constantes del servidor
HOST = 'localhost'
PORT = 8000

def clean_up_player(player_id):
    global players, projectiles
    with lock:
        if player_id in players:
            del players[player_id]
        projectiles = [p for p in projectiles if p["owner"] != player_id]

def handle_new_player(player_id, message):
    global players
    with lock:
        if player_id not in players:
            unique_id = str(uuid.uuid4())  # Generate unique ID
            players[unique_id] = {
                "id": unique_id,  # Store the unique ID
                "x": random.randint(0, 500),
                "y": random.randint(0, 500),
                "angle": random.randint(0, 360),
                "is_alive": True,
                "name": message.get("name", f"Player_{unique_id}")
            }
            print(f"Nuevo jugador conectado: {players[unique_id]}")
            return unique_id  # Return the unique ID
    return None

def update_player_position(player_id, message):
    global players
    with lock:
        if player_id in players:
            players[player_id]["x"] = message["x"]
            players[player_id]["y"] = message["y"]
            players[player_id]["angle"] = message["angle"]

            

def add_projectile(player_id, message):
    global projectiles
    with lock:
        projectiles.append({
            "x": message["x"],
            "y": message["y"],
            "angle": message["angle"],
            "owner": player_id,
            "max_distance": 600,
            "traveled_distance": 0
        })

def get_game_state():
    with lock:
        return {
            "players": players,
            "projectiles": projectiles
        }

def handle_client(client_socket, addr):
    global projectiles, players
    player_unique_id = None
    clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            message = json.loads(data)
            
            if message["type"] == "new_player":
                player_unique_id = handle_new_player(player_unique_id, message)
                # Send the unique ID back to the client
                response = {
                    "type": "player_id",
                    "id": player_unique_id
                }
                client_socket.sendall(json.dumps(response).encode("utf-8"))
            elif message["type"] == "position" and player_unique_id:
                update_player_position(player_unique_id, message)
            elif message["type"] == "shot" and player_unique_id:
                message["owner"] = player_unique_id  # Use the unique ID for projectile ownership
                add_projectile(player_unique_id, message)
            
            game_state = get_game_state()
            for client in clients:
                try:
                    client.sendall(json.dumps(game_state).encode("utf-8"))
                except:
                    print(f"Error al enviar datos al cliente {client}.")

            with lock:
                projectiles = []
        except Exception as e:
            print(f"Error en la conexión con {addr}: {e}")
            break
    
    if player_unique_id:
        clean_up_player(player_unique_id)
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()
    print(f"Conexión cerrada con {addr}")

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    run_server()