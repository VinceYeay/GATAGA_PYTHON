##########################################
# Importation des modules
import pygame
import random
import sys


##########################################
# Initialisation de pygame
# Module
pygame.init()

##########################################
# Paramètres du jeu
WIDTH = 540
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GALAGA")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)
PLAYER_SPEED = 5
SCALE = 2
BG_SPEED = 5
MAX_BULLETS = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 10



##########################################
# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

##########################################
# Chargement des images

# Fond d'écran
bg_image = pygame.image.load("images/backgrounds/bg5.png")
background = bg_image.get_rect()

background2 = bg_image.get_rect()

# Vaisseau du joueur
yellow_image = pygame.image.load("images/players/ship2.png")
yellow_image = pygame.transform.scale(yellow_image, (50, 50))
width = yellow_image.get_width()
height = yellow_image.get_height()
yellow_image = pygame.transform.scale(yellow_image, (width * SCALE, height * SCALE))
player_img = yellow_image  
yellow = yellow_image.get_rect()

# Ennemis
enemy_imgs = [
    pygame.image.load("images/assets/meteor.png"),
    pygame.image.load("images/assets/meteor2.png"),
    pygame.image.load("images/assets/ennemi1.png"),
    pygame.image.load("images/assets/ennemi2.png"),
]

enemy_imgs = [pygame.transform.scale(img, (50, 50)) for img in enemy_imgs]

# Boss
boss_img = pygame.Surface((100, 100))
boss_img.fill((128, 0, 128))

##########################################
# Création des listes
# Liste des bullets
yellow_bullets = []

##########################################
# Définitions des fonctions

def move_bg():

    global score

    # Déplacement des backgrounds
    background.y += BG_SPEED
    background2.y +=BG_SPEED

    if background.top >= HEIGHT:
        background.y = background2.y - background.height
    if background2.top >= HEIGHT:
        background2.y = background.y - background2.height

def create_player():
    return {
        "image": player_img,
        "rect": player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10)),
        "lives": 3,
        "projectiles": [],
        "double_shot": False,
    }

def control_players(player, keys):
    if keys[pygame.K_LEFT] and player["rect"].left > 0:
        player["rect"].x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player["rect"].right < WIDTH:
        player["rect"].x += PLAYER_SPEED
    if keys[pygame.K_UP] and player["rect"].top > 0:
        player["rect"].y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player["rect"].bottom < HEIGHT:
        player["rect"].y += PLAYER_SPEED



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

def draw_player(player):
    screen.blit(player["image"], player["rect"])
    for p in player["projectiles"]:
        pygame.draw.rect(screen, WHITE, p)

def shoot_player(player):
        offset = 15  # Distance from the center
        bullet_left = pygame.Rect(player["rect"].centerx -15, player["rect"].top, 5, 10)
        bullet_right = pygame.Rect(player["rect"].centerx + 10, player["rect"].top, 5, 10)
        player["projectiles"].append(bullet_left)
        player["projectiles"].append(bullet_right)


def create_enemy(x, y, speed=2, hp=3):
    image = random.choice(enemy_imgs)
    return {"rect": image.get_rect(topleft=(x, y)), "image": image, "speed": speed, "hp": hp}

def move_enemy(enemy, player):
    if player["rect"].centerx < enemy["rect"].centerx:
        enemy["rect"].x -= 1
    elif player["rect"].centerx > enemy["rect"].centerx:
        enemy["rect"].x += 1
    enemy["rect"].y += enemy["speed"]

def draw_enemy(enemy):
    screen.blit(enemy["image"], enemy["rect"])

def create_boss():
    return {
        "rect": boss_img.get_rect(midtop=(WIDTH // 2, 0)),
        "speed": 4,
        "hp": 30,
        "direction": 1,
        "projectiles": []
    }

def move_boss(boss):
    boss["rect"].x += boss["speed"] * boss["direction"]
    if boss["rect"].left <= 0 or boss["rect"].right >= WIDTH:
        boss["direction"] *= -1

def shoot_boss(boss):
    if random.randint(0, 30) == 0:
        boss["projectiles"].append(pygame.Rect(boss["rect"].centerx, boss["rect"].bottom, 10, 10))

def draw_boss(boss):
    screen.blit(boss_img, boss["rect"])
    for p in boss["projectiles"]:
        pygame.draw.rect(screen, RED, p)

def show_menu():
    screen.fill(BLACK)
    line1 = font.render("Appuyez sur une touche", True, WHITE)
    line2 = font.render("pour commencer", True, WHITE)
    screen.blit(line1, line1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(line2, line2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_game_over(timer):
    screen.fill(BLACK)
    game_over_text = big_font.render("GAME OVER", True, RED)
    time_text = font.render(f"Temps survécu : {timer // 60} secondes", True, WHITE)
    restart_text = font.render("Appuyez sur une touche pour recommencer", True, WHITE)
    screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(time_text, time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
    pygame.display.flip()
    wait_for_key()

def main():
    player = create_player()
    enemies = []
    boss = None
    boss_spawned = False
    score = 0
    timer = 0
    spawn_delay = 80
    show_menu()

    running = True
    while running:
        move_bg()
        screen.blit(bg_image, background)
        screen.blit(bg_image, background2)
        clock.tick(60)
        timer += 1

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot_player(player)

        control_players(player, keys)
        draw_player(player)

        for p in player["projectiles"][:]:
            p.y -= 10
            if p.bottom < 0:
                player["projectiles"].remove(p)

        if timer % spawn_delay == 0 and not boss_spawned:
            enemies.append(create_enemy(random.randint(0, WIDTH - 50), -50, speed=2 + timer // 1500, hp=2))


        if timer > 5000 and not boss_spawned:
            boss = create_boss()
            boss_spawned = True

        for e in enemies[:]:
            move_enemy(e, player)
            draw_enemy(e)

            if e["rect"].colliderect(player["rect"]):
                player["lives"] -= 1
                enemies.remove(e)
                continue

            if e["rect"].top > HEIGHT:
                player["lives"] -= 1
                enemies.remove(e)
                continue

            for p in player["projectiles"][:]:
                if e["rect"].colliderect(p):
                    e["hp"] -= 1
                    player["projectiles"].remove(p)

            if e["hp"] <= 0 and e in enemies:
                enemies.remove(e)

        if boss:
            move_boss(boss)
            shoot_boss(boss)
            draw_boss(boss)
            for p in boss["projectiles"][:]:
                p.y += 5
                if p.colliderect(player["rect"]):
                    player["lives"] -= 1
                    boss["projectiles"].remove(p)
                elif p.top > HEIGHT:
                    boss["projectiles"].remove(p)
            for p in player["projectiles"][:]:
                if boss["rect"].colliderect(p):
                    boss["hp"] -= 1
                    player["projectiles"].remove(p)
                    if boss["hp"] <= 0:
                        running = False

        life_text = font.render(f"Vies : {player['lives']}", True, WHITE)
        time_text = font.render(f"Temps : {timer // 60}", True, WHITE)
        screen.blit(life_text, (10, 10))
        screen.blit(time_text, (10, 40))

        if player["lives"] <= 0:
            running = False

        pygame.display.flip()

    show_game_over(timer)
    main()

if __name__ == "__main__":
    while True:
        main()
