import pygame
import math
import random

from pygame import mixer

'''Initialize pygame''' 
pygame.init() #Always be there

'''Create a screen'''
screen = pygame.display.set_mode((800,600))

'''Background sound'''
mixer.music.load("background.mp3")
mixer.music.play(-1)


'''Title and Icon'''
pygame.display.set_caption("Alien Attack Developed by Aatif Ahmad ")
icon = pygame.image.load("spaceshuttle.png")
pygame.display.set_icon(icon)

sad_face = pygame.image.load("sad.png")
 
'''Adding the player'''
playerImg = pygame.image.load("spaceshuttle.png")
playerX = 370
playerY = 480
playerX_change = 0

'''Enemy'''
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0,740))
    enemyY.append(random.randint(0,140))
    enemyX_change.append(1.2)
    enemyY_change.append(50)

'''ready - you can't see the bullet on screen.'''
'''fire - the bullet is currently moving.'''

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

'''Score'''
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX = 10
textY = 10

game_overX = 160
game_overY = 200

'''Game Over Text'''

game_over_font = pygame.font.Font("freesansbold.ttf",80)

def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(0,0,0))
    screen.blit(score,(x,y))

def game_over_text(x,y):
    over_text = game_over_font.render("GAME OVER",True,(255,0,0))
    screen.blit(over_text,(x,y))
    screen.blit(sad_face,(390,280))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 14,y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX),2) + math.pow((enemyY - bulletY),2))
    if distance < 27:
        return True
    else:
        return False

'''Game loop'''
running = True
while running:

    screen.fill((225,100,100))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        '''If keystroke is pressed check whether its right or left'''

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.2

            if event.key == pygame.K_RIGHT:
                playerX_change = 1.2

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("gun_shoot.mp3")
                bullet_sound.play()
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    '''Checking the boundary of player'''

    if (playerX + playerX_change) <=736 and (playerX + playerX_change) >=0:
        playerX += playerX_change
    else:
        playerX += 0

    for i in range(num_of_enemies):

        '''Game Over'''
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(game_overX,game_overY)
            break

        enemyX[i] += enemyX_change[i]
        '''Checking the boundaries of enemy'''

        if (enemyX[i] + enemyX_change[i]) >= 736:
            enemyX_change[i] = -1.2
            enemyY[i] += enemyY_change[i]

        elif (enemyX[i] + enemyX_change[i]) <= 0:
            enemyX_change[i] = 1.2
            enemyY[i] += enemyY_change[i]

        '''Check Collision'''
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision == True:
            explosion_sound = mixer.Sound("bad-explosion-6855.mp3")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0,740)
            enemyY[i] = random.randint(0,140)

        enemy(enemyX[i],enemyY[i],i)

    '''Bullet Movement'''
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update() #This is always there