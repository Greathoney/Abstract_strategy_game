import sys
import pygame
from pygame.locals import *

font = 'myfont.ttf'

colorRed = (255, 0, 0)
colorBlue = (0, 0, 255)
colorWhite = (255, 255, 255)
colorGray = (127, 127, 127)
colorBlack = (0, 0, 0)

leftMouse = 1
rightMouse = 3

resolution = (1280, 720)
FPS = 60
clock = pygame.time.Clock()

boardPositionVertex = ((450, 50), (820, 50), (1005, 370.43), (820, 690.86), (450, 690.86), (265, 370.43), (450, 50))
boardPositionEdge = []
boardPositionAll = []
for i in range(6):
    boardPositionEdgeElement = []
    startPoint_X = boardPositionVertex[i][0]
    endPoint_X = boardPositionVertex[i+1][0]
    startPoint_Y = boardPositionVertex[i][1]
    endPoint_Y = boardPositionVertex[i+1][1]
    gap_X = (endPoint_X - startPoint_X) / 8
    gap_Y = (endPoint_Y - startPoint_Y) / 8
    for j in range(8):
        newEdgePoint = (startPoint_X + gap_X * j, startPoint_Y + gap_Y * j)
        boardPositionEdgeElement.append(newEdgePoint)
    boardPositionEdge.append(boardPositionEdgeElement)

boardPositionAll.append(boardPositionEdge[0])
boardPositionAll[0].append(boardPositionEdge[1][0])
correction_X = boardPositionEdge[0][0][1] / 2
correction_Y = boardPositionEdge[1][2][1] - boardPositionEdge[1][1][1]
for i in range(8):
    boardPositionAllElement = []
    startPoint_X = boardPositionEdge[5][7-i][0]
    endPoint_X = boardPositionEdge[1][i][0]
    Point_Y = boardPositionEdge[5][7-i][1]
    gap_X = (endPoint_X - startPoint_X + correction_X) / (i + 9)
    for j in range(i + 10):
        newEdgePoint = (startPoint_X + gap_X * j, Point_Y)
        boardPositionAllElement.append(newEdgePoint)
    boardPositionAll.append(boardPositionAllElement)
for i in range(7):
    boardPositionAllElement = []
    startPoint_X = boardPositionEdge[4][7-i][0]
    endPoint_X = boardPositionEdge[2][i][0]
    gap_X = (endPoint_X - startPoint_X + correction_X) / (16 - i)
    Point_Y = boardPositionEdge[2][i][1]
    for j in range(16 - i):
        newEdgePoint = (startPoint_X + gap_X * j, Point_Y + correction_Y)
        boardPositionAllElement.append(newEdgePoint)
    boardPositionAll.append(boardPositionAllElement)
boardPositionAll.append(boardPositionEdge[3][:-1])
boardPositionAll[-1].append(boardPositionEdge[3][7])
boardPositionAll[-1].append(boardPositionEdge[4][0])

pygame.init()
pygame.display.set_caption("Mirror and Razor")
screen = pygame.display.set_mode(resolution)



razor = []
mirror = []

current = 'menu'
currentGame = 'razor'
currentGameSetting = 'position'

while True:
    leftMouseClicked = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == leftMouse:
            leftMouseClicked = True
        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos

    screen.fill(colorBlack)

    if current == 'menu':
        if leftMouseClicked and 610 < mousePos[0] < 670 and  400 < mousePos[1] < 440:
            current = 'game'
            continue
        if leftMouseClicked and 610 < mousePos[0] < 670 and 460 < mousePos[1] < 500:
            pygame.quit()
            sys.exit()

        fontTitle = pygame.font.Font(font, 50)
        textTitle = fontTitle.render('Mirror and Razor', True, colorWhite)
        textTitleRect = textTitle.get_rect()
        textTitleRect.center = (640, 320)
        screen.blit(textTitle, textTitleRect)

        fontPlay = pygame.font.Font(font, 20)
        if 610 < mousePos[0] < 670 and 400 < mousePos[1] < 440:
            textPlay = fontPlay.render('Play', True, colorRed)
        else:
            textPlay = fontPlay.render('Play', True, colorWhite)
        textPlayRect = textPlay.get_rect()
        textPlayRect.center = (640, 420)
        screen.blit(textPlay, textPlayRect)

        fontExit = pygame.font.Font(font, 20)
        if 610 < mousePos[0] < 670 and 460 < mousePos[1] < 500:
            textExit = fontExit.render('Exit', True, colorRed)
        else:
            textExit = fontExit.render('Exit', True, colorWhite)
        textExitRect = textExit.get_rect()
        textExitRect.center = (640, 480)
        screen.blit(textExit, textExitRect)

    elif current == 'game':
        pygame.draw.aalines(screen, colorWhite, False, boardPositionVertex)

        for i in range(3):
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[i][0],
                               boardPositionEdge[i + 3][0])
        for i in range(7):
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[0][i + 1], boardPositionEdge[2][7 - i])
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[5][i + 1], boardPositionEdge[3][7 - i])
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[1][i + 1], boardPositionEdge[5][7 - i])
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[2][i + 1], boardPositionEdge[4][7 - i])
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[0][i + 1], boardPositionEdge[4][7 - i])
            pygame.draw.aaline(screen, colorGray, boardPositionEdge[1][i + 1], boardPositionEdge[3][7 - i])

        for i in boardPositionAll:
            for j in i:
                if j[0] - 5 < mousePos[0] < j[0] + 5 and j[1] - 5 < mousePos[1] < j[1] + 5:
                    pygame.draw.circle(screen, colorGray, (round(j[0]), round(j[1])), 10, 0)
                if j in mirror:
                    pygame.draw.circle(screen, colorBlue, (round(j[0]), round(j[1])), 16, 2)
                elif j in razor:
                    pygame.draw.circle(screen, colorRed, (round(j[0]), round(j[1])), 16, 2)
                pygame.draw.circle(screen, colorWhite, (round(j[0]), round(j[1])), 5, 0)

        fontOrder = pygame.font.Font(font, 30)
        if currentGame == 'razor':
            textOrder = fontOrder.render('Razor turns', True, colorWhite)
        else:
            textOrder = fontOrder.render('Mirror turns', True, colorWhite)
        textPlayOrder = textOrder.get_rect()
        textPlayOrder.center = (1100, 100)
        screen.blit(textOrder, textPlayOrder)

        if currentGame == 'razor':
            for i in boardPositionAll:
                for j in i:
                    if currentGameSetting = 'position':
                        if leftMouseClicked and j[0] - 5 < mousePos[0] < j[0] + 5 and j[1] - 5 < mousePos[1] < j[1] + 5:
                            if not (j in razor and j in mirror):
                                razor.append(j)
                                currentGame = 'mirror'

        elif currentGame == 'mirror':
            for i in boardPositionAll:
                for j in i:
                    if leftMouseClicked and j[0] - 5 < mousePos[0] < j[0] + 5 and j[1] - 5 < mousePos[1] < j[1] + 5:
                        if not (j in razor and j in mirror):
                            mirror.append(j)
                            currentGame = 'razor'





    pygame.display.flip()
    clock.tick(FPS)