import pygame
import socket
import random

FPS = 60
WIDTH_ROOM = 4000
HEIGHT_ROOM = 4000
WIDTH_SERVER_WINDOWS = 300
HEIGHT_SERVER_WINDOWS = 300
START_PLAYER_SIZE = 50
COLORS = {
    '1': (255,255,0),
    '2': (255,0,0),
    '3': (0,255,0),
    '4': (0,255,250),
    '5': (255,255,0),
    '6': (255,100,0),
          }

def find(s):
    temp = None
    for i in range(len(s)):
        if s[i] == '<':
            temp = i
        if s[i] == '>' and temp != None:
            temp2 = i
            res = s[temp+1:temp2]
            res = list(map(int, res.split(',')))
            return res
    return ''

class Player():
    def __init__(self, conn, addr, x, y, r, color):
        self.conn = conn
        self.addr = addr
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.error = 0
        self.abs_speed = 10
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
    
    def change_speed(self, v):
        if (v[0] == 0) and (v[1] == 0):
            self.speed_x = 0
            self.speed_y = 0
        else:
            lenv = (v[0]**2 + v[1]**2)**0.5
            v = (v[0] / lenv, v[1] / lenv)
            v = (v[0] * self.abs_speed, v[1] * self.abs_speed)
            self.speed_x, self.speed_y = v[0], v[1]
        

mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
mainSocket.bind(('localhost', 8008))
mainSocket.setblocking(0)
mainSocket.listen(5)

pygame.init()
screen = pygame.display.set_mode((WIDTH_SERVER_WINDOWS, HEIGHT_SERVER_WINDOWS))
clock = pygame.time.Clock()
players = []
serverWorks = True
while serverWorks:
    clock.tick(FPS)
    try:
        newSocket, addr = mainSocket.accept()
        print("Игрок подключился, ", addr)
        newSocket.setblocking(0)
        newPlayer = Player(newSocket,
                           addr,
                           random.randint(0, WIDTH_ROOM),
                           random.randint(0, HEIGHT_ROOM),
                           START_PLAYER_SIZE,
                           str(random.randint(1, 6)))
        players.append(newPlayer)
    except:
        pass

    for player in players:
        try:
            data = player.conn.recv(1024)
            data = data.decode()
            data = find(data)
            player.change_speed(data)
        except:
            pass
        player.update()

    for player in players:
        try:
            player.conn.send('Новое состояние игры'.encode())
            player.error = 0
        except:
            player.error += 1

    for player in players:
        if player.error == 200:
            player.conn.close()
            players.remove(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            serverWorks = False

    screen.fill('BLACK')
    for player in players:
        x = round(player.x * WIDTH_SERVER_WINDOWS / WIDTH_ROOM)
        y = round(player.y * HEIGHT_SERVER_WINDOWS / HEIGHT_ROOM)
        r = round(player.r * WIDTH_SERVER_WINDOWS / WIDTH_ROOM)
        c = COLORS[player.color]
        pygame.draw.circle(screen, c, (x, y), r)
    pygame.display.update()

pygame.quit()
mainSocket.close()
