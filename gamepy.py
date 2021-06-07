import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

# background image load
background = pygame.image.load('sky.jpg')
background2 = pygame.image.load('Nightsky.jpg')

# background sound
mixer.music.load('back.mp3')
mixer.music.play(-1)

# plane image config
player_img = pygame.image.load('plane.png')
playerx = 366
playery = 500
playerx_change = 0
playery_change = 0

# cloud movement
cloud_img = []
cloudx = []
cloudy = []
cloudx_change = []
cloudy_change = []
no_cloud = 4
for i in range(no_cloud):
    cloudx.append(random.randint(0, 736))
    cloud_img.append(pygame.image.load('cloud2.png'))
    cloudy.append(random.randint(20, 100))
    cloudx_change.append(0.4)
    cloudy_change.append(0)

# fighter plane movement
fight_img = []
fightx = []
fighty = []
fightx_change = []
fighty_change = []
num_eminies = 6
for i in range(num_eminies):
    fight_img.append(pygame.image.load('flight.png'))
    fightx.append(random.randint(0, 736))
    fighty.append(random.randint(0, 300))
    fightx_change.append(1)
    fighty_change.append(30)

# bullet movement
bullet_img = pygame.image.load('bullet.png')
bulletx = 0
bullety = 500
bulletx_change = 0
bullety_change = 3
bullet_state = "ready"

# scoring
score = 0
font = pygame.font.Font('freesansbold.ttf', 36)
textx = 10
texty = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 60)

# for changing the day night
change = False


def player(x, y):
    screen.blit(player_img, (x, y))


def cloud(x, y, i):
    screen.blit(cloud_img[i], (x, y))


def fight(x, y, i):
    screen.blit(fight_img[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bullet_img, (x+16, y+10))


def collide(fightx, fighty, bulletx, bullety):
    dist = math.sqrt(math.pow(fightx-bulletx, 2) + math.pow(fighty-bullety, 2))
    if dist < 27:
        return True
    else:
        return False


def scoring(x, y):
    score_ = font.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(score_, (x, y))


def game_over(score):
    screen.fill(pygame.Color("white"))
    over_text = over_font.render("GAME OVER", True, ((255, 0, 0)))
    screen.blit(over_text, (130, 300))
    final = over_font.render("SCORE: "+str(score), True, ((255, 0, 0)))
    screen.blit(final, (130, 200))


# main function
while True:
    screen.fill(pygame.Color("blue"))  # the backgound
    if score % 10 == 0 and score != 0:
        change = not(change)
    if change:
        screen.blit(background, (0, 0))  # background image for morning
    else:
        screen.blit(background2, (0, 0))  # background image for night sky

    # all the keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -2
            if event.key == pygame.K_RIGHT:
                playerx_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # get the current x coordinate
                    bullet_sound = mixer.Sound('bullet.mp3')
                    bullet_sound.play()
                    bulletx = playerx
                    bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # managing the events

    # 1. player movement
    playerx += playerx_change
    if playerx < 0:
        playerx = 0
    if playerx > 736:
        playerx = 736

    # 2. cloud movement
    for i in range(no_cloud):
        cloudx[i] += cloudx_change[i]
        if cloudx[i] < 0:
            cloudx_change[i] = 0.3
            cloudy[i] += cloudy_change[i]
            if cloudy[i] > 600:
                cloudy[i] = random.randint(20, 200)
        elif cloudx[i] > 736:
            cloudx_change[i] = -0.3
            cloudy[i] += cloudy_change[i]
            if cloudy[i] > 600:
                cloudy[i] = random.randint(20, 200)
        cloud(cloudx[i], cloudy[i], i)  # calling the cloud

    # 3. bullet movement
    if bullety < 0:  # restoring the bullet to the plane after it disappears from the screen
        bullety = 500
        bullet_state = "ready"

    if bullet_state is "fired":     # to continue seeing the shot bullet travell, after triggered via sapcebar
        bullet(bulletx, bullety)    # or else the bullet disappears
        # this will show the bullet travell by changing the y coordinate
        bullety -= bullety_change

    # 4. fighter jet movement
    for i in range(num_eminies):

        # game over condition -if the planes reaches a particular point we call it over
        if fighty[i] > 430:
            for j in range(num_eminies):
                fighty[i] = 2000
            game_over(score)
            break

        # fixing the enemy fighter jet movement
        fightx[i] += fightx_change[i]      # move horizontally
        if fightx[i] < 0:                  # at left most side
            fighty[i] += fighty_change[i]   # changes vertical level
            fightx_change[i] = 1            # starts moving towards right
            # if vertical position is too low then reset the enemy to the top of the screen but this is optional as this end condition
            if fighty[i] > 600:
                fighty[i] = random.randint(0, 300)
        elif fightx[i] > 736:           # at right most side
            fighty[i] += fighty_change[i]   # changes vertical level
            fightx_change[i] = -1           # starts moving towards right
            # if vertical position is too low then reset the enemy to the top of the screen but this is optional as this end condition
            if fighty[i] > 600:
                fighty[i] = random.randint(0, 300)

        # 5. collision of bulet with the particular fighter jet
        collision = collide(fightx[i], fighty[i], bulletx, bullety)
        if collision:
            explode_sound = mixer.Sound('explode.wav')
            explode_sound.play()
            bullety = 500
            bullet_state = "ready"
            score += 1
            fightx[i] = random.randint(0, 736)
            fighty[i] = random.randint(0, 200)

        fight(fightx[i], fighty[i], i)  # calling the fighter plane

    player(playerx, playery)  # callig the player function
    scoring(textx, texty)
    pygame.display.update()
