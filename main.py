import socket
import pygame


WIDTH_SCREEN = 1000
HEIGHT_SCREEN = 800

#Подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 8008))

pygame.init()
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption('agar.agar')

oldV = (0, 0)
V = (0, 0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        V = (pos[0] - WIDTH_SCREEN//2, pos[1] - HEIGHT_SCREEN//2)
    if ((V[0])**2 + (V[1])**2) <= 50**2:
        V = (0, 0)
    if V != oldV:
        oldV = V
        message = '<' + str(V[0]) + ', ' + str(V[1]) + '>'
        sock.send(message.encode())
    data = sock.recv(1024)
    data = data.decode()

    screen.fill('gray25')
    pygame.draw.circle(screen, (255, 6, 6), (WIDTH_SCREEN//2, HEIGHT_SCREEN//2), 50)
    pygame.display.update()
pygame.quit()
