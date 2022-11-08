import pygame
from characters import *

pygame.init()

# GAME WINDOW
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street-fighter.io")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Define the cooldown before the game starts
start_cooldown = 0
update_timer = pygame.time.get_ticks()
intro_font = pygame.font.Font("freesansbold.ttf", 64)


# LOAD BACKGROUND IMAGES
bg_image = pygame.image.load(r"Images/Background Images/background_image.jpg").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_bg_image = pygame.image.load("Images/Background Images/pixel art game menu.jpg").convert_alpha()
menu_bg_image = pygame.transform.scale(menu_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


# GAME COUNTDOWN 
game_countdown = 3
game_countdown_font = pygame.font.Font("freesansbold.ttf", 60)




################################## SpreadSheet Annotations ###############################

# index 0 = width, index 1 = height, index 2 = scale factor to increase size
KNIGHT_SCALE = 4
KNIGHT_OFFSET = [45, 35]
KNIGHT_DATA = [120, 80, KNIGHT_SCALE, KNIGHT_OFFSET]


# Load spreadsheets
knight = pygame.image.load(r"Images/SpreadSheets/knight sprite sheet.png").convert_alpha()

# define number of steps in each animation
KNIGHT_ANIMATION_STEPS = [10, 10, 10, 10, 6, 6, 4, 3, 3, 2, 1]

# Instances of fighter classes
fighter_1 = Fighter(1, 360, 370, False, KNIGHT_DATA, knight, KNIGHT_ANIMATION_STEPS)
fighter_2 = Fighter(2, 720, 370, True, KNIGHT_DATA, knight, KNIGHT_ANIMATION_STEPS)

############################################################################################
# Variables
playing = False


# Functions

def draw_healthbar(health, x, y):
    ratio = health / 100
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    pygame.draw.rect(screen, RED, (x, y, 400, 40))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 40))


def draw_bg(image):
    screen.blit(image, (0, 0))


def draw_text(font, sentence, text_col, x, y):
    text = font.render(sentence, True, text_col )
    screen.blit(text, (x, y))

def draw_rectangles(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    return rect




############################################ RUNNING THE GAME ##################################################

running = True

while running:
    # Refresh at 60 FPS
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # I know it's wrong, but I can't use the jump function in characters.py as it causes input lag and doesn't
    # record the events properly, I would try to find a way through pygame.key.get_pressed()

    # Player 1
        if playing and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                if fighter_1.jump[1] == False:
                    if fighter_1.jump[0] == False:
                        fighter_1.jump[0] = True
                    else:
                        fighter_1.jump[1] = True
                    fighter_1.vel_y = -30

    # Player 2
        if playing and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                if fighter_2.jump[1] == False:
                    if fighter_2.jump[0] == False:
                        fighter_2.jump[0] = True
                    else:
                        fighter_2.jump[1] = True
                    fighter_2.vel_y = -30

    mouse_press = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()


    if playing:

        # Draw images
        draw_bg(bg_image)

        # Draw health-bars
        draw_healthbar(fighter_1.health, 150, 20)
        draw_healthbar(fighter_2.health, 790, 20)

        # Draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if start_cooldown <= 0:
          # Writing the bullshit for the temp_countdown
            temp_countdown = (game_countdown * 60 * 1000 - (pygame.time.get_ticks() - game_countdown_timer)) / 1000 # Turn to seconds
            temp_countdown = f"{temp_countdown // 60 : .0f} : {temp_countdown % 60 : .0f }"

          
            # Draw the countdown on the screen
            draw_text(game_countdown_font, temp_countdown, (255, 0, 0), 680, 15)
          
          
            # Move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)

        else:
            if (pygame.time.get_ticks() - update_timer) >= 1000:
                update_timer = pygame.time.get_ticks()
                start_cooldown -= 1
            draw_text(intro_font, f"{start_cooldown + 1}", (255, 0, 0), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5)

        # Update the character animation
        fighter_1.update()
        fighter_2.update()

    else:
        draw_bg(menu_bg_image)
        rect_0 = draw_rectangles(390, 200, 500, 80)
        rect_1 = draw_rectangles(525, 295, 210, 50)
        rect_2 = draw_rectangles(510, 345, 245, 55)
        rect_3 = draw_rectangles(580, 400, 120, 43)

        pygame.draw.rect(screen, (190, 90, 180), rect_0, 5)
        pygame.draw.rect(screen, (255, 0, 0), rect_1, 5)
        pygame.draw.rect(screen, (0, 74, 83), rect_2, 5)
        pygame.draw.rect(screen, (75, 15, 19), rect_3, 5)

        if 390 <= mouse_pos[0] <= 890 and 200 <= mouse_pos[1] <= 280:
            if mouse_press[0] == True:
                playing = True
                game_countdown_timer = pygame.time.get_ticks()
        if 580 <= mouse_pos[0] <= 700 and 400 <= mouse_pos[1] <= 443:
            if mouse_press[0] == True:
                running = False
        


    # Update the screen
    pygame.display.update()

# Get out of pygame
pygame.quit()
