import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GATAGA")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

player_img = pygame.Surface((50, 50))
player_img.fill(BLUE)
enemy_img = pygame.Surface((50, 50))
enemy_img.fill(RED)
boss_img = pygame.Surface((100, 100))
boss_img.fill((128, 0, 128))
powerup_img = pygame.Surface((30, 30))
powerup_img.fill(GREEN)
bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill(BLACK)
stars = [pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 2, 2) for _ in range(100)]

def create_player():
    return {
        "image": player_img,
        "rect": player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10)),
        "speed": 5,
        "lives": 3,
        "projectiles": [],
        "double_shot": False,
        "powered_up": False
    }

def move_player(player, keys):
    if keys[pygame.K_LEFT]:
        player["rect"].x -= player["speed"]
    if keys[pygame.K_RIGHT]:
        player["rect"].x += player["speed"]
    if keys[pygame.K_UP]:
        player["rect"].y -= player["speed"]
    if keys[pygame.K_DOWN]:
        player["rect"].y += player["speed"]
    player["rect"].clamp_ip(screen.get_rect())

def shoot_player(player):
    if player["double_shot"]:
        player["projectiles"].append(pygame.Rect(player["rect"].left + 5, player["rect"].top, 5, 10))
        player["projectiles"].append(pygame.Rect(player["rect"].right - 10, player["rect"].top, 5, 10))
    else:
        player["projectiles"].append(pygame.Rect(player["rect"].centerx, player["rect"].top, 5, 10))

def draw_player(player):
    screen.blit(player["image"], player["rect"])
    for p in player["projectiles"]:
        pygame.draw.rect(screen, WHITE, p)

def create_enemy(x, y, speed=2, hp=1):
    return {"rect": enemy_img.get_rect(topleft=(x, y)), "speed": speed, "hp": hp}

def move_enemy(enemy, player):
    if player["rect"].centerx < enemy["rect"].centerx:
        enemy["rect"].x -= 1
    elif player["rect"].centerx > enemy["rect"].centerx:
        enemy["rect"].x += 1
    enemy["rect"].y += enemy["speed"]

def draw_enemy(enemy):
    screen.blit(enemy_img, enemy["rect"])

def create_boss():
    return {
        "rect": boss_img.get_rect(midtop=(WIDTH // 2, 0)),
        "speed": 3,
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

def create_powerup():
    return {"rect": powerup_img.get_rect(topleft=(random.randint(0, WIDTH - 30), 0)), "speed": 2}

def move_powerup(pu):
    pu["rect"].y += pu["speed"]

def draw_powerup(pu):
    screen.blit(powerup_img, pu["rect"])

def create_explosion(center):
    return {"center": center, "radius": 1, "max_radius": 30, "finished": False}

def update_explosion(ex):
    ex["radius"] += 2
    if ex["radius"] >= ex["max_radius"]:
        ex["finished"] = True

def draw_explosion(ex):
    if not ex["finished"]:
        pygame.draw.circle(screen, RED, ex["center"], ex["radius"], 2)

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
    powerups = []
    boss = None
    boss_spawned = False
    score = 0
    timer = 0
    spawn_delay = 60
    explosions = []
    show_menu()

    running = True
    while running:
        clock.tick(60)
        timer += 1
        bg.fill(BLACK)
        for star in stars:
            star.y += 1
            if star.y > HEIGHT:
                star.y = 0
                star.x = random.randint(0, WIDTH)
            pygame.draw.rect(bg, WHITE, star)
        screen.blit(bg, (0, 0))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot_player(player)

        move_player(player, keys)
        draw_player(player)

        for p in player["projectiles"][:]:
            p.y -= 10
            if p.bottom < 0:
                player["projectiles"].remove(p)

        if timer % spawn_delay == 0 and not boss_spawned:
            enemies.append(create_enemy(random.randint(0, WIDTH - 50), -50, speed=2 + timer // 1500, hp=2))

        #13sec
        if timer % 800 == 0:
            powerups.append(create_powerup())

        if timer > 3000 and not boss_spawned:
            boss = create_boss()
            boss_spawned = True

        for e in enemies[:]:
            move_enemy(e, player)
            draw_enemy(e)

            if e["rect"].colliderect(player["rect"]):
                explosions.append(create_explosion(player["rect"].center))
                player["lives"] -= 1
                player["double_shot"] = False
                player["powered_up"] = False
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
                score += 10

        for pu in powerups[:]:
            move_powerup(pu)
            draw_powerup(pu)
            if pu["rect"].colliderect(player["rect"]):
                player["double_shot"] = True
                player["powered_up"] = True
                powerups.remove(pu)
            elif pu["rect"].top > HEIGHT:
                powerups.remove(pu)

        if boss:
            move_boss(boss)
            shoot_boss(boss)
            draw_boss(boss)
            for p in boss["projectiles"][:]:
                p.y += 5
                if p.colliderect(player["rect"]):
                    explosions.append(create_explosion(player["rect"].center))
                    player["lives"] -= 1
                    player["double_shot"] = False
                    player["powered_up"] = False
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

        for ex in explosions[:]:
            update_explosion(ex)
            draw_explosion(ex)
            if ex["finished"]:
                explosions.remove(ex)

        pygame.display.flip()

    show_game_over(timer)
    main()

if __name__ == "__main__":
    main()
