#Burger Dog
import random
import pygame

#init pygame
pygame.init()

GAME_FOLDER = "C:/Users/ASUS/Desktop/doc/burger_dog"

#create a window (display surface)
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#colors
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
ORANGE = pygame.Color(255,127, 0)
GREEN = pygame.Color(0,255,0)

#actors
#1) dog
dog_left = pygame.image.load(GAME_FOLDER + '/dog.png')
dog_right = pygame.transform.flip(dog_left.copy(),True, False)
dog = dog_left
dog_rect = dog.get_rect()
dog_rect.centerx= WINDOW_WIDTH//2
dog_rect.bottom = WINDOW_HEIGHT
dog_velocity = 5

#2) burger
burger_y = -100
burger_velocity = 5
burger = pygame.image.load(GAME_FOLDER + '/burger.png')
burger_rect = burger.get_rect()
burger_rect.center = (WINDOW_WIDTH//2, burger_y)


#game values
score = 0
lives = 3
consecutive_catches = 0
game_status = 1

#font and texts
font_big = pygame.font.Font(GAME_FOLDER + '/SunnyspellsRegular.otf', 60)
font_small = pygame.font.Font(GAME_FOLDER + '/SunnyspellsRegular.otf', 40)

title = font_big.render('Burger Dog', True, ORANGE)
title_rect = title.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.centery = 40

player_score = font_small.render('Score: ' + str(score), True, ORANGE)
player_score_rect = player_score.get_rect()
player_score_rect.centery = 40
player_score_rect.left = 50

player_lives = font_small.render('Lives: ' + str(lives), True, ORANGE)
player_lives_rect = player_lives.get_rect()
player_lives_rect.centery = 40
player_lives_rect.right = WINDOW_WIDTH - 50

game_over = font_big.render('Game Over!!!', True, RED)
game_over_rect = game_over.get_rect()
game_over_rect.centerx = WINDOW_WIDTH//2
game_over_rect.centery = WINDOW_HEIGHT//2 - 50

game_replay = font_small.render('R: Replay, Q: Quit', True, GREEN)
game_replay_rect = game_replay.get_rect()
game_replay_rect.centerx = WINDOW_WIDTH//2
game_replay_rect.centery = WINDOW_HEIGHT//2 + 50

#sound
woof = pygame.mixer.Sound(GAME_FOLDER + '/woof.mp3')
woof.set_volume(0.5)

loss = pygame.mixer.Sound(GAME_FOLDER + '/loss.wav')
loss.set_volume(0.5)

pygame.mixer.music.load(GAME_FOLDER + '/instrumental.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#main game loop
running = True
clock = pygame.time.Clock()
FPS = 60
while running:
    #Fetch and process the events (user actions)
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN and game_status == 0:
            if ev.key == pygame.K_q:
                running = False
            elif ev.key == pygame.K_r:
                lives = 3
                player_lives = font_small.render('Lives: ' + str(lives), True, ORANGE)
                score = 0
                player_score = font_small.render('Score: ' + str(score), True, ORANGE)

                dog_velocity = 5
                dog_rect.centerx = WINDOW_WIDTH//2
                dog_rect.bottom = WINDOW_HEIGHT

                burger_rect.centerx = random.randint(20, WINDOW_WIDTH - 20)
                burger_rect.centery = burger_y

                game_status = 1
                pygame.mixer.music.play(-1)

    #pour BLACK color on the window
    window.fill(BLACK, (0,0, WINDOW_WIDTH, WINDOW_HEIGHT))

    #blit the HUD
    window.blit(title, title_rect)
    window.blit(player_score, player_score_rect)
    window.blit(player_lives, player_lives_rect)
    pygame.draw.line(window, ORANGE, (0, 80), (WINDOW_WIDTH, 80), 5)

    if game_status == 1:
        #Read the keyboards actions for continuous movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dog = dog_left
            if dog_rect.left > 0:
                dog_rect.left -= dog_velocity
        elif keys[pygame.K_RIGHT]:
            dog = dog_right
            if dog_rect.right <WINDOW_WIDTH:
                dog_rect.right += dog_velocity
        if keys[pygame.K_UP]:
            if dog_rect.top > 80:
                dog_rect.top -= dog_velocity
        elif keys[pygame.K_DOWN]:
            if dog_rect.bottom < WINDOW_HEIGHT:
                dog_rect.bottom += dog_velocity

        #burger fall
        burger_rect.bottom += burger_velocity

        #may be taken/eaten
        if dog_rect.colliderect(burger_rect):
            #taken/eaten
            woof.play()
            dog_velocity= dog_velocity + 0.5 if dog_velocity < 8 else dog_velocity
            score += WINDOW_HEIGHT - dog_rect.top
            player_score = font_small.render('Score: ' + str(score), True, ORANGE)

            burger_rect.centerx = random.randint(20, WINDOW_WIDTH - 20)
            burger_rect.centery = burger_y
            consecutive_catches+=1
            if consecutive_catches == 5:
                dog_velocity= 10 #turbo boost
                consecutive_catches = 0

        #may be dropped
        elif burger_rect.bottom > WINDOW_HEIGHT:
            #burger dropped
            loss.play()
            consecutive_catches = 0
            burger_rect.centerx = random.randint(20, WINDOW_WIDTH-20)
            burger_rect.centery = burger_y

        #gradual drop in velocity
        dog_velocity-= 0.005
        if dog_velocity <= 0:
            lives-=1
            player_lives = font_small.render('Lives: ' + str(lives), True, ORANGE)
            if lives == 0:
                game_status = 0
                pygame.mixer.music.stop()
            else:
                dog_velocity = 5
                dog_rect.centerx = WINDOW_WIDTH//2
                dog_rect.bottom = WINDOW_HEIGHT
                burger_rect.centerx = random.randint(20, WINDOW_WIDTH-20)
                burger_rect.centery = burger_y


        #blit the actors
        window.blit(dog, dog_rect)
        if burger_rect.top > 80:
            window.blit(burger, burger_rect)

    elif game_status== 0:
        window.blit(game_over, game_over_rect)
        window.blit(game_replay, game_replay_rect)

    #update the display
    pygame.display.update()

    #clock regulates the loop iteration at FPS
    #* By this the gaming experience is the same across low-high end CPU's
    #* The game utilizes optimum CPU and battery
    #* Doesnt affect systems multitasking by grabbing more CPU power
    clock.tick(FPS)

#quit pygame
pygame.quit()