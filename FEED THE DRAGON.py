# created by HIMAL KUMAR SINGH

# ----------------FEED THE DRAGON-----------------
import random
import pygame

# initialize pygame
pygame.init()

# GAME VALUES

# window dimensions
WIDTH = 1200
HEIGHT = 600

# constants
FPS = 30
COIN_VELOCITY = 5
DRAGON_VELOCITY = 20
MAX_LIVES = 3
DEFAULT_SCORE = 0
BUFFER_DISTANCE = 0
FOLDER = "D:/Programming/Pygame/FEED THE DRAGON/"

# variables
current_player_lives = MAX_LIVES
current_player_score = DEFAULT_SCORE
current_coin_velocity = COIN_VELOCITY

# colors
GREEN = pygame.Color(0, 255, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

# images
background = pygame.image.load(FOLDER + "dragon night.jpg")
background_rect = background.get_rect()
background_rect.topleft = (0, 0)

dim_background = pygame.image.load(FOLDER + "dragon night dim.jpg")
dim_background_rect = dim_background.get_rect()
dim_background_rect.topleft = (0, 0)

# actors
dragon = pygame.image.load(FOLDER + "dragon.png")
dragon_rect = dragon.get_rect()
dragon_rect.right = WIDTH - 20
dragon_rect.centery = HEIGHT // 2

coin = pygame.image.load(FOLDER + "dollar.png")
coin_rect = coin.get_rect()
coin_rect.left = BUFFER_DISTANCE
coin_rect.top = random.randint(50, HEIGHT - 40)

# sounds
pickup = pygame.mixer.Sound(FOLDER + "pickup.wav")
pickup.set_volume(0.7)

loss = pygame.mixer.Sound(FOLDER + "loss.wav")
loss.set_volume(0.7)

# music
pygame.mixer.music.load(FOLDER + "background music.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# game font
game_font1 = pygame.font.Font(FOLDER + "AttackGraffiti.ttf", 32)

# texts
lives = game_font1.render('Lives : ' + str(current_player_lives), True, GREEN)
lives_rect = lives.get_rect()
lives_rect.left = 20
lives_rect.top = 10

score = game_font1.render('Score : ' + str(current_player_score), True, GREEN)
score_rect = score.get_rect()
score_rect.right = WIDTH - 20
score_rect.top = 10

title = game_font1.render('FEED THE DRAGON', True, GREEN)
title_rect = title.get_rect()
title_rect.centerx = WIDTH // 2
title_rect.top = 10

game_over = game_font1.render('..............GAME OVER..............', True, GREEN)
game_over_rect = game_over.get_rect()
game_over_rect.centerx = WIDTH // 2
game_over_rect.centery = HEIGHT // 2

restart = game_font1.render('press R to restart', True, GREEN)
restart_rect = restart.get_rect()
restart_rect.centerx = WIDTH // 2
restart_rect. centery = HEIGHT // 2 + 60

# CREATE WINDOW
display_surface = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption('FEED THE DRAGON')  # window title

# GAME CONTROL LOOP
running = True
game_status = 1
clock = pygame.time.Clock()
show = 0

while running:

    # events
    for ev in pygame.event.get():

        # if cross button is clicked or alt+F4 is pressed
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.KEYUP or ev.type == pygame.KEYDOWN:

            # moving dragon
            if game_status == 1:
                # up arrow key
                if ev.key == pygame.K_UP and dragon_rect.top >= 50:
                    dragon_rect.centery -= DRAGON_VELOCITY

                # down arrow key
                elif ev.key == pygame.K_DOWN and dragon_rect.bottom <= HEIGHT - 10:
                    dragon_rect.centery += DRAGON_VELOCITY

            # restarting game
            elif game_status == 2:
                if ev.key == pygame.K_r:
                    game_status = 1
                    pygame.mixer.music.play(-1)

                    current_player_score = DEFAULT_SCORE
                    current_player_lives = MAX_LIVES
                    current_coin_velocity = COIN_VELOCITY

                    lives = game_font1.render('Lives : ' + str(current_player_lives), True, GREEN)
                    score = game_font1.render('Score : ' + str(current_player_score), True, GREEN)

                    # placing dragon at mid right
                    dragon_rect.right = WIDTH - 20
                    dragon_rect.centery = HEIGHT // 2

                    # placing coin at start position
                    coin_rect.left = BUFFER_DISTANCE
                    coin_rect.top = random.randint(50, HEIGHT - 40)

                    show = 0

    if game_status == 1:
        # putting background image on screen
        display_surface.blit(source=background, dest=background_rect)

        # putting lives, score and title
        lives = game_font1.render('Lives : ' + str(current_player_lives), True, GREEN)
        display_surface.blit(source=lives, dest=lives_rect)

        score = game_font1.render('Score : ' + str(current_player_score), True, GREEN)
        display_surface.blit(source=score, dest=score_rect)

        display_surface.blit(source=title, dest=title_rect)

        # putting actors
        display_surface.blit(source=dragon, dest=dragon_rect)
        display_surface.blit(source=coin, dest=coin_rect)

        if coin_rect.right <= WIDTH and coin_rect.left >= BUFFER_DISTANCE:
            # moving coin
            coin_rect.right += current_coin_velocity

            if coin_rect.colliderect(dragon_rect):
                # coin is caught by dragon
                pickup.play()

                # placing coin at start
                coin_rect.left = BUFFER_DISTANCE
                coin_rect.top = random.randint(50, HEIGHT - 40)

                # increase in score by one
                current_player_score += 1

                # increasing difficulty(speed of coin)
                current_coin_velocity += 1

        elif coin_rect.right > WIDTH:
            # coin crosses window
            loss.play()

            # placing coin at start
            coin_rect.left = BUFFER_DISTANCE
            coin_rect.top = random.randint(50, HEIGHT - 40)

            # loss of one life
            current_player_lives -= 1

    # printing game over
    elif game_status == 2:
        # dim the background
        display_surface.blit(source=dim_background, dest=dim_background_rect)

        lives = game_font1.render('Lives : ' + str(current_player_lives), True, GREEN)
        display_surface.blit(source=lives, dest=lives_rect)

        score = game_font1.render('Score : ' + str(current_player_score), True, GREEN)
        display_surface.blit(source=score, dest=score_rect)

        display_surface.blit(source=game_over, dest=game_over_rect)

        if show % 5 == 0:
            # blinking effect
            display_surface.blit(source=restart, dest=restart_rect)
        show += 1

    # game over lives becomes zero
    if current_player_lives == 0:
        game_status = 2

    # refresh the display
    pygame.display.update()

    # iteration speed control
    clock.tick(FPS)

# deallocate the resources
pygame.quit()
