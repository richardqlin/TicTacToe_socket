import time
import sys
import pygame

import random
import socket
from pygame.locals import *

pygame.init()
pygame.mixer.init()
# d = {1:'_',2:'_',3:'_',4:'_',5:'_',6:'_',7:'_',8:'_',9:'_'}
width = 900
height = 600
screen = pygame.display.set_mode((width, height))
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
#win = pygame.mixer.Sound('win.wav')
#tie = pygame.mixer.Sound('glass_ping.wav')

pygame.draw.rect(screen, white, (int(width / 3), 0, int(width / 3), height), 1)
pygame.draw.rect(screen, white, (0, int(height / 3), width, int(height / 3)), 1)
pygame.display.update()

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",1234))

def print_board():
    for i in d:
        print(i, ":", d[i], end=' ')
        if i == 3 or i == 6:
            print()
    print()


def show_x():
    time.sleep(0.5)
    #win.play()
    screen.fill(black)
    show_text('X win.', int(width / 2.5), int(height / 3), green, 60)
    pygame.display.update()
    time.sleep(5)
    global done
    done = False


def show_o():
    time.sleep(0.5)
    #win.play()
    screen.fill(black)
    show_text('O win.', int(width / 2.5), int(height / 3), green, 60)
    pygame.display.update()
    time.sleep(5)
    global done
    done = False


def show_Tie():
    time.sleep(0.5)
    #tie.play()
    screen.fill(black)
    show_text('Tie. Game Over', int(width / 4), int(height / 3), green, 60)
    pygame.display.update()
    time.sleep(5)
    global done
    done = False


# Check for any winning combination
def checkwin(d):
    # Checking Each Row for X

    if d[3] == d[1] == d[2] == 'X' or d[6] == d[4] == d[5] == 'X' or d[9] == d[7] == d[8] == 'X':
        show_x()
        quit()
    # Checking Each Row for O
    elif d[3] == d[1] == d[2] == 'O' or d[6] == d[4] == d[5] == 'O' or d[9] == d[7] == d[8] == 'O':
        show_o()
        quit()
    # Checking Each Column for X
    elif d[1] == d[4] == d[7] == 'X' or d[2] == d[5] == d[8] == 'X' or d[1] == d[3] == d[9] == 'X':
        show_x()
        quit()
    # Checking Diagonals for X
    elif d[1] == d[5] == d[9] == 'X' or d[3] == d[5] == d[7] == 'X':
        show_x()
        quit()
    # Checking Each Column for O
    elif d[3] == d[6] == d[9] == 'O' or d[1] == d[4] == d[7] == 'O' or d[2] == d[5] == d[8] == 'O':
        show_o()
        quit()
    # Checking Diagonals for O
    elif d[1] == d[5] == d[9] == 'O' or d[3] == d[5] == d[7] == 'O':
        show_o()
        quit()


def show_text(msg, x, y, color, s):
    fontobj = pygame.font.SysFont("times.ttf", s)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))


def get_input(p, x):
    print("Player ", p, ". You are X. Please choose the box ! choose and empty box")

    if d[x] == '_':
        d[x] = p
    checkwin()
    print_board()


def drawX(box_x, box_y):
    pygame.draw.line(screen, blue, (box_x, box_y), (box_x + int(width / 3), box_y + int(height / 3)), 1)
    pygame.draw.line(screen, blue, (box_x + int(width / 3), box_y), (box_x, box_y + int(height / 3)), 1)


def drawO(box_x, box_y):
    pygame.draw.ellipse(screen, green, (box_x, box_y, int(width / 3), int(height / 3)), 1)


d = {1: '_', 2: '_', 3: '_', 4: '_', 5: '_', 6: '_', 7: '_', 8: '_', 9: '_'}
print(d)
width = 900
height = 600
screen = pygame.display.set_mode((width, height))
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
#win = pygame.mixer.Sound('win.wav')
#tie = pygame.mixer.Sound('glass_ping.wav')
pygame.display.set_caption("Client Python Game")

pygame.draw.rect(screen, white, (int(width / 3), 0, int(width / 3), height), 1)
pygame.draw.rect(screen, white, (0, int(height / 3), width, int(height / 3)), 1)

# print_board()
done = True
count = 0
player = 0
pygame.draw.rect(screen, white, (int(width / 3), 0, int(width / 3), height), 1)
pygame.draw.rect(screen, white, (0, int(height / 3), width, int(height / 3)), 1)
pygame.display.update()
x = -200
y = -200

turnX, turnO = 'x', 'o'
while done:
    # print(d)
    checkwin(d)
    if count == 9:
        show_Tie()
        break

    print('client',turnX, turnO)
    if turnX=='x':
        data = s.recv(1024).decode()
        print(data)


        data = data.split(',')

        x = int(data[0])
        y = int(data[1])
        turnX, turnO = turnO, turnX
    elif turnX=='o':
        for event in pygame.event.get():
            # Reacts to Diffrent events
            if event.type == QUIT:
                done = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                s.send((str(x) + ',' + str(y)).encode())
                turnX, turnO = turnO, turnX
                print(turnX, turnO)
    if x in range(0, 300) and y in range(0, 200):
        if d[1] == '_':
            if turnX == 'x':
                drawX(0, 0)
                d[1] = 'X'
            elif turnO == 'x':
                drawO(0, 0)
                d[1] = 'o'

    elif x in range(300, 600) and y in range(0, 200):
        if d[2] == '_':
            if turnX == 'x':
                drawX(300, 0)
                d[2] = 'X'

            elif turnO == 'x':
                drawO(300, 0)
                d[2] = 'o'
    elif x in range(600, 900) and y in range(0, 200):
        if d[3] == '_':
            if turnX == 'x':
                drawX(600, 0)
                d[3] = 'X'
            elif turnO == 'x':

                drawO(600, 0)
                d[3] = 'o'

    elif x in range(0, 300) and y in range(200, 400):
        if d[4] == '_':
            if turnX == 'x':

                drawX(0, 200)
                d[4] = 'X'
            elif turnO == 'x':
                drawO(0, 200)
                d[4] = 'o'


    elif x in range(300, 600) and y in range(200, 400):
        if d[5] == '_':
            if turnX == 'x':
                drawX(300, 200)
                d[5] = 'X'
            elif turnO == 'x':
                drawO(300, 200)
                d[5] = 'o'

    elif x in range(600, 900) and y in range(200, 400):
        if d[6] == '_':
            if turnX == 'x':
                drawX(600, 200)
                d[6] = 'X'
            elif turnO == 'x':
                drawO(600, 200)
                d[6] = 'o'
    elif x in range(0, 300) and y in range(400, 600):
        if d[7] == '_':
            if turnX == 'x':
                drawX(0, 400)
                d[7] = 'X'
            elif turnO == 'x':
                drawO(0, 400)
                d[7] = 'o'
    elif x in range(300, 600) and y in range(400, 600):
        if d[8] == '_':
            if turnX == 'x':
                drawX(300, 400)
                d[8] = 'X'
            elif turnO == 'x':
                drawO(300, 400)
                d[8] = 'o'
    elif x in range(600, 900) and y in range(400, 600):
        if d[9] == '_':
            if turnX == 'x':
                drawX(600, 400)
                d[9] = 'X'
            elif turnO == 'x':
                drawO(600, 400)
                d[9] = 'o'

  
    pygame.display.update()
pygame.quit()
