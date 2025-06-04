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

# Couleur
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Cube 
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

# Sons
# pygame.mixer.Sound("shoot.wav")

# Joueur
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 10))
        self.speed = 5
        self.lives = 3
        self.projectiles = []
        self.double_shot = False
        self.powered_up = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        if self.double_shot:
            self.projectiles.append(pygame.Rect(self.rect.left + 5, self.rect.top, 5, 10))
            self.projectiles.append(pygame.Rect(self.rect.right - 10, self.rect.top, 5, 10))
        else:
            self.projectiles.append(pygame.Rect(self.rect.centerx, self.rect.top, 5, 10))

    def draw(self):
        screen.blit(self.image, self.rect)
        for p in self.projectiles:
            pygame.draw.rect(screen, WHITE, p)

# Ennemi
class Enemy:
    def __init__(self, x, y, speed=2, hp=1):
        self.image = enemy_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.hp = hp

    def move(self, player):
        # IA basique
        if player.rect.centerx < self.rect.centerx:
            self.rect.x -= 1
        elif player.rect.centerx > self.rect.centerx:
            self.rect.x += 1
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Boss
class Boss:
    def __init__(self):
        self.image = boss_img
        self.rect = self.image.get_rect(midtop=(WIDTH//2, 0))
        self.speed = 3
        self.hp = 30
        self.direction = 1
        self.projectiles = []

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

    def shoot(self):
        if random.randint(0, 30) == 0:
            self.projectiles.append(pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 10))

    def draw(self):
        screen.blit(self.image, self.rect)
        for p in self.projectiles:
            pygame.draw.rect(screen, RED, p)

# Power-up
class PowerUp:
    def __init__(self):
        self.image = powerup_img
        self.rect = self.image.get_rect(topleft=(random.randint(0, WIDTH-30), 0))
        self.speed = 2

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Menu
def show_menu():
    screen.fill(BLACK)
    text = big_font.render("Appuyez sur une touche pour commencer", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
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

    screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
    screen.blit(time_text, time_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
    screen.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
    pygame.display.flip()
    wait_for_key()


# Boucle de jeu
def main():
    player = Player()
    enemies = []
    powerups = []
    boss = None
    boss_spawned = False
    score = 0
    timer = 0
    spawn_delay = 60

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
                player.shoot()

        player.move(keys)

        # Spawning enemies
        if timer % spawn_delay == 0 and not boss_spawned:
            enemies.append(Enemy(random.randint(0, WIDTH-50), -50, speed=2 + timer // 1500, hp=2))

        # Spawning power-ups
        if timer % 800 == 0:
            powerups.append(PowerUp())

        # Spawning boss
        if timer > 3000 and not boss_spawned:
            boss = Boss()
            boss_spawned = True

        # Update and draw
        player.draw()

        for p in player.projectiles[:]:
            p.y -= 10
            if p.bottom < 0:
                player.projectiles.remove(p)

        enemies_to_remove = []

        for e in enemies:
            e.move(player)
            e.draw()

            # Check collision with player (priority!)
            if e.rect.colliderect(player.rect):
                player.lives -= 1
                player.double_shot = False
                player.powered_up = False
                enemies_to_remove.append(e)
                continue  # Don't check projectiles if enemy touched player

            # Check if enemy went off screen
            if e.rect.top > HEIGHT:
                player.lives -= 1
                enemies_to_remove.append(e)
                continue

            # Check collision with player's projectiles
            for p in player.projectiles[:]:
                if e.rect.colliderect(p):
                    e.hp -= 1
                    player.projectiles.remove(p)

            if e.hp <= 0:
                enemies_to_remove.append(e)

        # Final cleanup after loop
        for e in enemies_to_remove:
            if e in enemies:
                enemies.remove(e)
                score += 10

  
        for pu in powerups[:]:
            pu.move()
            pu.draw()
            if pu.rect.colliderect(player.rect):
                player.double_shot = True
                player.powered_up = True
                powerups.remove(pu)
            elif pu.rect.top > HEIGHT:
                powerups.remove(pu)

        if boss:
            boss.move()
            boss.shoot()
            boss.draw()
            for p in boss.projectiles[:]:
                p.y += 5
                if p.colliderect(player.rect):
                    player.lives -= 1
                    player.double_shot = False
                    player.powered_up = False
                    boss.projectiles.remove(p)
                elif p.top > HEIGHT:
                    boss.projectiles.remove(p)
            for p in player.projectiles[:]:
                if boss.rect.colliderect(p):
                    boss.hp -= 1
                    player.projectiles.remove(p)
                    if boss.hp <= 0:
                        running = False

        # UI
        life_text = font.render(f"Vies : {player.lives}", True, WHITE)
        screen.blit(life_text, (10, 10))
        time_text = font.render(f"Temps : {timer // 60}", True, WHITE)
        screen.blit(time_text, (10, 40))
        if player.lives <= 0:
            running = False

        pygame.display.flip()

    show_game_over(timer)
    main()


if __name__ == "__main__":
    main()
