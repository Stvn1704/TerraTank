import pygame
import socket
import math
import os
import threading
import json
from clases import Jugador

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.player_id = None
        self.connected = False
        self.lock = threading.Lock()
        self.player_name = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False

    def send(self, data):
        try:
            if self.connected and self.socket:
                self.socket.sendall(json.dumps(data).encode("utf-8"))
        except (socket.error, BrokenPipeError) as e:
            print(f"Error sending data: {e}")
            self.reconnect()

    def receive(self):
        try:
            if self.connected and self.socket:
                data = self.socket.recv(4096)
                if data:
                    return json.loads(data.decode("utf-8"))
        except Exception as e:
            print(f"Error receiving data: {e}")
            self.reconnect()
        return None

    def reconnect(self):
        print("Attempting to reconnect...")
        self.connected = False
        if self.socket:
            self.socket.close()
        
        if self.connect():
            print("Reconnected successfully")
            if self.player_name:
                self.send({"type": "new_player", "name": self.player_name})
        else:
            print("Reconnection failed")

    def close(self):
        self.connected = False
        if self.socket:
            self.socket.close()
class Projectile:
        def __init__(self, x, y, angle, max_distance=600):
            self.map_x = x
            self.map_y = y
            self.angle = angle
            self.speed = 25
            self.start_x = x
            self.start_y = y
            self.max_distance = max_distance
            self.traveled_distance = 0

        def update(self):
            self.map_x += self.speed * math.cos(self.angle)
            self.map_y += self.speed * math.sin(self.angle)
            self.traveled_distance = math.sqrt((self.map_x - self.start_x) ** 2 + 
                                            (self.map_y - self.start_y) ** 2)
            return self.traveled_distance < self.max_distance

        def draw(self, surface, offset_x, offset_y):
            screen_x = self.map_x - offset_x
            screen_y = self.map_y - offset_y
            if 0 <= screen_x <= surface.get_width() and 0 <= screen_y <= surface.get_height():
                pygame.draw.circle(surface, WHITE, (int(screen_x), int(screen_y)), 5)
# Game constants and variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
screen_width, screen_height = 1280, 720
HOST, PORT = 'localhost', 8000

def play(nombre):
    # Initialize pygame and screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TerraPlane Multijugador")

    # Load and scale background
    background_image = pygame.image.load('fondo_nuevo.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width * 2, screen_height * 2))
    background_width, background_height = background_image.get_width(), background_image.get_height()

    # Game state variables
    players = {}
    projectiles = []
    projectiles_local = []
    frames = []
    frame_index = 0
    last_shot_time = 0
    shoot_cooldown = 100
    offset_x = offset_y = 0
    players_lock = threading.Lock()

    # Initialize the client
    client = Client(HOST, PORT)
    client.connect()

    # Get player name and create player
    client.player_name = nombre
    Jugador1 = Jugador(client.socket.getsockname()[1], nombre)

    # Game functions
    def update_remote_players(server_data):
        global players
        with players_lock:
            for player_id, player_data in server_data.items():
                if str(player_id) == str(client.player_id):
                    continue
                if player_id not in players:
                    players[player_id] = Jugador(player_data["id"], player_data["name"])
                players[player_id].x = player_data["x"]
                players[player_id].y = player_data["y"]
                players[player_id].angle = player_data["angle"]

    def update_projectiles(server_projectiles):
        global projectiles
        projectiles = [Projectile(proj["x"], proj["y"], proj["angle"], proj["max_distance"]) 
                    for proj in server_projectiles]

    def handle_events():
        global last_shot_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= shoot_cooldown:
                    create_projectile(event)
                    last_shot_time = current_time
        return True

    def create_projectile(event):
        global projectiles_local
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - screen_width//2, mouse_y - screen_height//2
        angle = math.atan2(dy, dx)
        projectile_x = screen_width//2 + offset_x + 60 * math.cos(angle)
        projectile_y = screen_height//2 + offset_y + 60 * math.sin(angle)
        projectiles_local.append(Projectile(projectile_x, projectile_y, angle))
        client.send({
            "type": "shot",
            "x": projectile_x,
            "y": projectile_y,
            "angle": angle,
            "owner": client.player_id
        })

    def update_players():
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1
        if dx != 0 or dy != 0:
            move_player(dx * 25, dy * 25)

    def move_player(dx, dy):
        global offset_x, offset_y
        safety_margin = 100
        
        new_offset_x = offset_x + dx
        new_offset_y = offset_y + dy
        
        if 0 <= new_offset_x <= background_width - screen_width:
            offset_x = new_offset_x
        if 0 <= new_offset_y <= background_height - screen_height:
            offset_y = new_offset_y
            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - screen_height//2, mouse_x - screen_width//2)
        
        client.send({
            "type": "position",
            "x": screen_width//2 + offset_x,
            "y": screen_height//2 + offset_y,
            "angle": angle
        })

    def mini_map():
        mini_map_width, mini_map_height = 200, 200
        mini_map_rect = pygame.Rect(20, screen_height - mini_map_height - 20, 
                                mini_map_width, mini_map_height)
        
        pygame.draw.rect(screen, BLACK, mini_map_rect, 2)
        
        mini_map_scale_x = mini_map_width / background_width
        mini_map_scale_y = mini_map_height / background_height
        
        mini_map_background = pygame.transform.scale(
            background_image,
            (int(background_width * mini_map_scale_x),
            int(background_height * mini_map_scale_y))
        )
        screen.blit(mini_map_background, mini_map_rect.topleft)
        
        mini_map_pos_x = ((screen_width//2 + offset_x) / background_width) * mini_map_width + mini_map_rect.x
        mini_map_pos_y = ((screen_height//2 + offset_y) / background_height) * mini_map_height + mini_map_rect.y
        
        mini_map_pos_x = max(mini_map_rect.x, min(mini_map_pos_x, mini_map_rect.right))
        mini_map_pos_y = max(mini_map_rect.y, min(mini_map_pos_y, mini_map_rect.bottom))
        
        pygame.draw.circle(screen, GREEN, (int(mini_map_pos_x), int(mini_map_pos_y)), 5)

    def load_frames():
        global frames
        frame_directory = "Movimiento"
        new_frame_size = (Jugador1.size, Jugador1.size)
        for filename in sorted(os.listdir(frame_directory)):
            if filename.endswith('.gif'):
                frame = pygame.image.load(os.path.join(frame_directory, filename))
                frames.append(pygame.transform.scale(frame, new_frame_size))
        print(f"Se han cargado {len(frames)} cuadros.")

    def draw_remote_players():
        with players_lock:
            for player_id, player in players.items():
                if str(player_id) != str(client.player_id):
                    rotated_image = pygame.transform.rotate(frames[frame_index], 
                                                        -math.degrees(player.angle))
                    rotated_rect = rotated_image.get_rect(
                        center=(player.x - offset_x, player.y - offset_y))
                    screen.blit(rotated_image, rotated_rect.topleft)

    def render():
        global frame_index

        screen.blit(background_image, (-offset_x, -offset_y))

        if frames:
            frame_index = (frame_index + 1) % len(frames)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - screen_height // 2, mouse_x - screen_width // 2)

            # Dibujar el avión
            rotated_image = pygame.transform.rotate(frames[frame_index], -math.degrees(angle))
            rotated_rect = rotated_image.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(rotated_image, rotated_rect.topleft)

            # Crear y dibujar hitbox
            hitbox_points = create_hitbox(screen_width // 2, screen_height // 2, angle)
            draw_hitbox(screen, hitbox_points)



        draw_remote_players()

        for projectile in projectiles:
            if projectile.update():
                projectile.draw(screen, offset_x, offset_y)
                check_collision_with_bullets()
                
            

        mini_map()
    def receive_data_from_server():
        while True:
            data = client.receive()
            if data:
                if data.get("type") == "player_id":
                    client.player_id = data["id"]
                    print(f"Received player ID: {client.player_id}")
                elif "players" in data:
                    update_remote_players(data.get("players", {}))
                if "projectiles" in data:
                    update_projectiles(data.get("projectiles", []))

    def create_hitbox(x, y, angle, size=60):
        """
        Crea una hitbox cuadrada alrededor del avión.
        """
        half_size = size // 2
        # Coordenadas relativas del cuadrado antes de rotar
        points = [
            (-half_size, -half_size),  # Esquina superior izquierda
            (half_size, -half_size),  # Esquina superior derecha
            (half_size, half_size),   # Esquina inferior derecha
            (-half_size, half_size)   # Esquina inferior izquierda
        ]

        # Rotar el cuadrado según el ángulo
        rotated_points = [
            (
                x + px * math.cos(angle) - py * math.sin(angle),
                y + px * math.sin(angle) + py * math.cos(angle)
            )
            for px, py in points
        ]

        return rotated_points

    def draw_hitbox(surface, points, color=(255, 0, 0)):
        """
        Dibuja la hitbox cuadrada para depuración.
        """
        pygame.draw.polygon(surface, color, points, 2)


    def check_collision_with_bullets():
        """
        Verifica si alguna bala golpea la hitbox cuadrada.
        """
        global projectiles, offset_x, offset_y, screen_height, screen_width
        x1 = screen_width // 2 + offset_x
        y1 = screen_height // 2 + offset_y
        
        for projectile in projectiles:
            bullet_pos = (projectile.map_x, projectile.map_y)
            
            # Corregir las condiciones de colisión usando "and"
            if (x1 - 30 < projectile.map_x < x1 + 30) and (y1 - 30 < projectile.map_y < y1 + 30):
                print("¡Colisión detectada!")
                Jugador1.recibir_daño(10)
                projectiles.remove(projectile)  # Eliminar bala tras colisión


    def main():
        try:
            load_frames()
            client.send({"type": "new_player", "name": client.player_name})

            threading.Thread(target=receive_data_from_server, daemon=True).start()

            running = True
            while running:
                running = handle_events()
                update_players()
                render()
                pygame.display.flip()

                if Jugador1.vida <= 0:
                    print("¡Has sido derrotado!")
                    client.send({
                        "type": "position",
                        "x": 0,
                        "y": 0,
                        "angle":0,
                        "is_alive":False
                    })
                    running = False

        except Exception as e:
            print(f"Error en el bucle del juego: {e}")
        finally:
            pygame.quit()
            client.close()

    if __name__ == "__main__":
        main()