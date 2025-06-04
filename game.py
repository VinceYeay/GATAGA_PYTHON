##########################################
# Importation des modules
import pygame
import time
import random

##########################################
# Paramètres du jeu

WIDTH = 540
HEIGHT= 700
FPS = 60
HP = 10

PLAYER_SPEED = 5
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 10
MAX_BULLETS = 10000000
YELLOW_HP = 10

SCALE = 2

BG_SPEED = 5

ENEMIE_DELAY = 1800
ENEMIE_SPEED = 5
ENEMIE_HP = 3

##########################################
# Initialisation de pygame

# Module
pygame.init()

# Écran et dimensions
pygame.display.set_caption("Space shooters")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Horloge
clock = pygame.time.Clock()



##########################################
# Couleurs
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,150,255)

##########################################
# Chargement des images

# Fond d'écran
bg_image = pygame.image.load("images/backgrounds/bg5.png")
background = bg_image.get_rect()

background2 = bg_image.get_rect()

# Vaisseau du joueur
yellow_image = pygame.image.load("images/players/ship2.png")
width = yellow_image.get_width()
height = yellow_image.get_height()
yellow_image = pygame.transform.scale(yellow_image, (width * SCALE, height * SCALE))
yellow = yellow_image.get_rect()

# Ennemis
meteor_1 = pygame.image.load("images/assets/meteor.png")
meteor_2 = pygame.image.load("images/assets/meteor2.png")
ennemi_1 = pygame.image.load("images/ennemies/ennemi1.png")
ennemi_2 = pygame.image.load("images/ennemies/ennemi2.png")

##########################################
# Création des formes


##########################################
# Création des listes
# Liste des bullets
yellow_bullets = []

# Liste des images des ennemis
ennemis_image = [meteor_1, meteor_2, ennemi_1, ennemi_2]

# Liste des ennemis
moving_enemies = []

##########################################
# Polices d'écriture

pygame.font.init() # Initialisation

# Hp
hp_font = pygame.font.SysFont("twcengras",60)

# Gagnant
final_font = pygame.font.SysFont("franklingothicheavy", 120)

# Décompte
countdown_font = pygame.font.SysFont("twcengras",275)

# Nouvelle partie?
new_game_font = pygame.font.SysFont("franklingothicheavy",70)

# Chronomètre
timer_font = pygame.font.SysFont("twcengras",60)

##########################################
# Définitions des fonctions


def init_game() :
    global running, yellow_hp, game_paused, time_passed, enemie_hp

     # Initialisation des variables
    running = True
    yellow_hp = YELLOW_HP
    game_paused = False
    time_passed = 0
    enemie_hp = ENEMIE_HP


    yellow_bullets.clear()


    # Positionnement initial des vaisseaux
    yellow.center = ( WIDTH//2 , HEIGHT - 50)

    # Positionnement des background
    background.topleft = (0,0)
    background2.x = background.x
    background2.bottom = background.top

    # Timer
    countdown()

def countdown():
    global game_paused
    for i in range(3, 0, -1):
        count_text = countdown_font.render(str(i), True, WHITE)
        count_rect = count_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(bg_image, (0,0))    
        screen.blit(count_text, count_rect)
        pygame.display.flip()
        time.sleep(1)
    game_paused = False

def time_of_game():
    global game_paused
    for i in range(3, 0, -1):
        timer_text = timer_font.render(str(i), True, WHITE)
        timer_rect = timer_text.get_rect(center=(100,10))
        screen.blit(bg_image, (0,0))    
        screen.blit(timer_text, timer_rect)
        pygame.display.flip()
        time.sleep(1)
    game_paused = False


def control_players() :
    keys = pygame.key.get_pressed() 

    if game_paused == False :

        # Contrôle du joueur

        if keys[pygame.K_LEFT] and yellow.left > 0:
            yellow.x = yellow.x - PLAYER_SPEED
        if keys[pygame.K_RIGHT] and yellow.right < WIDTH:
         yellow.x = yellow.x + PLAYER_SPEED
        # if keys[pygame.K_UP] and yellow.top > 0:
        #     yellow.y = yellow.y - PLAYER_SPEED
        # if keys[pygame.K_DOWN] and yellow.bottom < WIDTH:
        #     yellow.y = yellow.y + PLAYER_SPEED



def move_bullets():
    if game_paused == False :

        # Balles vertes
        for bullet in yellow_bullets :
            bullet.y -= BULLET_SPEED

            if bullet.left > WIDTH :
                yellow_bullets.remove(bullet)



def move_bg():

    global score

    # Déplacement des backgrounds
    background.y += BG_SPEED
    background2.y += background2.y + BG_SPEED

    if background.bottom > HEIGHT : 
        background2.bottom = 0

    if background.top >= HEIGHT :
        background.bottom = 0

    # background2.bottom = background.top 
    # background2.bottomleft = (0,0)

    # if background2.top >= HEIGHT : 
    #     background2.bottom = 0



def handle_events():
    global running

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS :
                bullet_left = pygame.Rect(yellow.topleft, (BULLET_WIDTH, BULLET_HEIGHT))
                bullet_right = pygame.Rect(yellow.topright, (BULLET_WIDTH, BULLET_HEIGHT))
                yellow_bullets.append(bullet_left)
                yellow_bullets.append(bullet_right)


            if event.key == pygame.K_y and game_paused == True :
                init_game()
            if event.key == pygame.K_n and game_paused == True :
                running = False

def lose_hp() :
    global yellow_hp

    for bullet in yellow_bullets :
        if bullet.colliderect(yellow) :
            yellow_hp = yellow_hp - 1
            yellow_bullets.remove(bullet)





def show_winner(player,color):

    # Gagnant
    winner_text = winner_font.render(player + "LOST", True, color)
    winner_rect = winner_text.get_rect()
    winner_rect.center = (WIDTH//2,HEIGHT//2 - 100)
    screen.blit(winner_text, winner_rect)


    # Affichage de la nouvelle partie
    new_game = new_game_font.render(str("Nouvelle partie?"), True, BLUE)
    new_game_rect = new_game.get_rect()
    new_game_rect.center = (WIDTH//2, 420)
    screen.blit(new_game, new_game_rect)

    new_game = new_game_font.render(str("Y/N"), True, BLUE)
    new_game_rect = new_game.get_rect()
    new_game_rect.center = (WIDTH//2, 500)
    screen.blit(new_game, new_game_rect)


def moving_enemies():
    for monster in moving_enemies :
        enemie["rect"].y += ENEMIE_SPEED

        if enemie["rect"].top > HEIGHT :
            moving_enemies.remove(enemie)



def create_new_ennemies() :
    global time_passed

    # Aller chercher le temps actuel
    current_time = pygame.time.get_ticks()

    # Séquence de conditions selon le temps passé
    if current_time - time_passed >= ENEMIE_DELAY :

        # Choix d'une image d’un ennemi
        enemie = random.choice(ennemis_image)

        # Création du rectangle de mêmes dimensions que l'image
        enemie_rect = enemie.get_rect()

        # Positionnement du rectangle en haut de la fenêtre
        enemie_rect.midbottom = random.randrange(75, WIDTH-75), 0

        # Création d'un dictionnaire de l’ennemi et ajout à moving_enemies
        moving_enemies.append({"image" : enemie, "rect" : enemie_rect})

        # Réinitialisation du temps
        time_passed = current_time + 5
 


def draw():
    global game_paused

    # Fond d'écran  
    # screen.blit(bg_image, background)

    # Vaisseau vert
    screen.blit(yellow_image, yellow)

    # Background
    screen.blit(bg_image, background)
    screen.blit(bg_image, background2)


    # Dessin des balles
    for bullet in yellow_bullets :
        pygame.draw.rect(screen, YELLOW, bullet)

    # Les ennemis
    for enemie in moving_enemies :
        screen.blit(enemie["image"], enemie["rect"])

    # Texte à l'écran
    # Vies du joueur
    yellow_hp_text = hp_font.render(str(yellow_hp), True, YELLOW)
    yellow_hp_rect = yellow_hp_text.get_rect()
    yellow_hp_rect.topleft = (10,10)
    screen.blit(yellow_hp_text, yellow_hp_rect)


    # Affichage des vies 
    if yellow_hp == 0 :
        show_winner("YELLOW", YELLOW)
        game_paused = True
        countdown.stop()


    # Affichage du temps
    timer_text = hp_font.render(str(clock), True, YELLOW)
    timer_rect = timer_text.get_rect()
    timer_rect.topleft = (100,10)
    screen.blit(timer_text, timer_rect)

    # Actualisation de l'écran
    pygame.display.flip()


##########################################
##########################################
# Boucle principale du jeu

# Initialisation de la partie
init_game()

while running == True :

    # Contrôle de la vitesse de la boucle
    clock.tick(FPS)


    # Appel des différentes fonctions
    handle_events()
    control_players()
    move_bullets()
    lose_hp()
    move_bg() 
    create_new_ennemies()
    moving_enemies()


    # Appel de la fonction draw()
    draw()


pygame.quit()