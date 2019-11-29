import pygame
import random
import math

#initialize pygame
pygame.init()
score = 0

#Creating a screen
backgroundImage = pygame.image.load("images/background.jpg")
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#PLAYER Plane
playerImg = pygame.image.load("images/player1.png")
playerImg = pygame.transform.scale(playerImg,(64,64))
playerX =370
playerY = 480

playerSpeed = 2
#change in x direction
playerChangeX = 0
#change in y direction
playerChangeY = 0

def player(x,y):
    screen.blit(playerImg,(x,y))

#Bullet Plane
bulletImg = pygame.image.load("images/bullet.png")
bulletImg = pygame.transform.scale(bulletImg,(20,20))
bulletX =370
bulletY = 800
bulletState = "ready"
bulletSpeed = 3
#change in x direction
bulletChangeX = 0
#change in y direction
bulletChangeY = 0

def bullet(x,y):
    screen.blit(bulletImg,(x,y))

#ENEMY
enemyImg = pygame.image.load("images/enemy1.png")
enemyX =random.randint(0,735)
enemyY =random.randint(50,150)
def respawn():
    global enemyX
    enemyX=random.randint(0,735)
    global enemyY
    enemyY=random.randint(50,150)

respawn()

enemySpeed = 1
#change in x direction
enemyChangeX = enemySpeed
#change in y direction
enemyChangeY = 40

def enemy(x,y):
    screen.blit(enemyImg,(x,y))

#Collision Detection
def isCollision(enemyX,enemyY):
    if bulletX > enemyX and bulletX < enemyX+64 and bulletY <= enemyY+64 and bulletY > enemyY+32:
        return True
    return False

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Checking which key is pressed and changing the speed accordingly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChangeX = -playerSpeed
            if event.key == pygame.K_RIGHT:
                playerChangeX = playerSpeed
            if event.key == pygame.K_UP:
                playerChangeY = -playerSpeed
            if event.key == pygame.K_DOWN:
                playerChangeY = playerSpeed
            if event.key == pygame.K_SPACE:
                if bulletState == 'ready':

                    bulletX = playerX+22
                    bulletY = playerY-10
                    bulletState = "fired"
                    bulletChangeY = -bulletSpeed



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChangeX = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerChangeY = 0

#adding the x nd y according to the speed
    playerX += playerChangeX
    playerY += playerChangeY

#Constraing the spaceship
    if(playerX>736):
        playerX = 736
    if(playerX<0):
        playerX = 0
    if(playerY>536):
        playerY = 536
    if(playerY<0):
        playerY = 0

#Controlling the enemy movement
    if(enemyX>736):
        enemyChangeX = -enemySpeed
        enemyY += enemyChangeY
    if(enemyX<0):
        enemyChangeX = enemySpeed
        enemyY += enemyChangeY

    enemyX += enemyChangeX

#Controlling Bullet movement

    if bulletY <= 0:
        bulletState = "ready"
        bulletY = 800

    if(bulletState == "fired") :
        bulletY += bulletChangeY

#Check Collision
    if isCollision(enemyX,enemyY):
        respawn()
        bulletState = "ready"
        bulletY = 800
        score += 1
        print(score)

    screen.fill((0,0,0))
    screen.blit(backgroundImage,(0,0))
    player(playerX,playerY)
    enemy(enemyX,enemyY)
    bullet(bulletX,bulletY)
    pygame.display.update()
