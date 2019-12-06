import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()
score_value = 0
clock = pygame.time.Clock()

#Creating a screen
backgroundImage = pygame.image.load("images/background.jpg")
groundImage = pygame.image.load("images/ground.png")
groundImage = pygame.transform.scale(groundImage,(800,50))
screen = pygame.display.set_mode((800,650))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

mixer.music.load('images/background.wav')
mixer.music.play(-1)

running = True

#PLAYER Plane
playerImg = pygame.image.load("images/player1.png")
playerImg = pygame.transform.scale(playerImg,(64,64))
playerImgStrong = pygame.image.load("images/player3.png")
playerImgStrong = pygame.transform.scale(playerImgStrong,(64,64))
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
bulletY = -50
bulletState = "ready"
bulletSpeed = 3
#change in x direction
bulletChangeX = 0
#change in y direction
bulletChangeY = 0

def bullet(x,y):
    screen.blit(bulletImg,(x,y))

#TEXT

fontScore = pygame.font.Font('fonts/game_over.ttf',60)
fontGO = pygame.font.Font('fonts/game_over.ttf',180)
testX = 10
testY = 10

def show_score(x,y):
    score = fontScore.render("Score : "+str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))



#ENEMY
numOfEnemy = 6

enemyPower = []
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
enemySpeed = 1

def respawn(i):
    enemyX[i] = random.randint(0,735)
    enemyY[i]=random.randint(50,150)
    enemyChangeX[i] = abs(enemyChangeX[i])  +  0.5
    enemyPower = random.randint(1,30)

for i in range(numOfEnemy):
    enemyPower.append(random.randint(1,30))
    enemyImg.append(pygame.image.load("images/enemy1.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
#change in x direction
    enemyChangeX.append(enemySpeed)
#change in y direction
    enemyChangeY.append(40)
    respawn(i)



def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#Collision Detection
def isCollision(enemyX,enemyY):
    if bulletX > enemyX and bulletX < enemyX+64 and bulletY <= enemyY+64 and bulletY > enemyY+32:
        return True
    return False

def isCollisionPlayer():
    for i in range(numOfEnemy):

        if playerX > enemyX[i] - 64 and playerX < enemyX[i] + 64 and playerY > enemyY[i] - 64 and playerY < enemyY[i] + 64:
                return True

    return False


#game loop
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
                    bullet_Sound = mixer.Sound('images/laser.wav')
                    bullet_Sound.play()



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
    if(playerY<200):
        playerY = 200



#Controlling the enemy movement
    for i in range(numOfEnemy):
        enemyX[i] += enemyChangeX[i]
        if(enemyX[i]>736):
            enemyChangeX[i] = -enemyChangeX[i]
            enemyY[i] += enemyChangeY[i]
        if(enemyX[i]<0):
            enemyChangeX[i] = -enemyChangeX[i]
            enemyY[i] += enemyChangeY[i]

        if enemyY[i]>540:
            bulletState = "fired"
            playerX =370
            playerY = 480
            bulletY = -50
            enemyY = [800,800,800,800,800,800]
            enemySpeed = [0,0,0,0,0,0]


#Check Collision
        if isCollision(enemyX[i],enemyY[i]):

            bulletChangeY = -bulletSpeed
            explosion = mixer.Sound('images/explosion.wav')
            explosion.play()
            respawn(i)
            bulletState = "ready"
            bulletY = -50
            score_value += 1
            print(score_value)

        if isCollisionPlayer():

            bulletState = "fired"
            playerX =370
            playerY = 480
            bulletY = -50
            enemyY = [800,800,800,800,800,800]
            enemySpeed = [0,0,0,0,0,0]


#Controlling Bullet movement

    if bulletY <= 0:
        bulletState = "ready"
        bulletY = -50

    if(bulletState == "fired") :
        bulletY += bulletChangeY



    screen.fill((0,0,0))
    screen.blit(backgroundImage,(0,0))
    screen.blit(groundImage,(0,600))
    for i in range(numOfEnemy):
        enemy(enemyX[i],enemyY[i],i)
    player(playerX,playerY)
    show_score(10,10)
    bullet(bulletX,bulletY)
    pygame.display.update()
