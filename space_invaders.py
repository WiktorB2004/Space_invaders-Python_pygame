import random
import pygame
import os

# Window Init
pygame.init()
pygame.font.init()
SCREEN_SIZE: tuple = 800, 700
FPS = 60
WIN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Space Invaders')

# Background and Style variables
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), SCREEN_SIZE)
bg_vel = 1

HEALTH_FONT = pygame.font.SysFont('comicsans', 24)
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 40)

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Player Variables
PLAYER_SIZE: tuple = 65, 55
PLAYER = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'spaceship.png')), PLAYER_SIZE), 180)
PLAYER_VEL = 5
player_lives = 3
# Bullet Variables
BULLET_VEL = 6
max_player_bullets = 10
# Enemy variables
ENEMY_SIZE: tuple = 60, 50
ENEMY_ADD_EVENT = pygame.USEREVENT + 1
ENEMY_SHOOT_EVENT = pygame.USEREVENT + 2
ENEMY_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'enemy.png')), ENEMY_SIZE)

pygame.time.set_timer(ENEMY_ADD_EVENT, 1500)
pygame.time.set_timer(ENEMY_SHOOT_EVENT, 1000)

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.lives = 3
    
    def draw_bullets(self, bullets, player):
        for bullet in bullets:
            if bullet.y < SCREEN_SIZE[1]:
                bullet.y += BULLET_VEL
            if bullet.colliderect(player):
                global player_lives
                player_lives -= 1
                bullets.remove(bullet)
            pygame.draw.rect(WIN, YELLOW, bullet)
    
    def handle_movement(self, enemies):
        global player_lives
        if self.y < SCREEN_SIZE[1]:
            self.y += 2
        else:
            player_lives -= 1
            enemies.remove(self)
            
def handle_enemy_action(player, enemies, player_bullets):
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE[0], ENEMY_SIZE[1])
        enemy.handle_movement(enemies)
        enemy.draw_bullets(enemy.bullets, player)
        for bullet in player_bullets:
            if enemy_rect.colliderect(bullet):
                player_bullets.remove(bullet)
                enemy.lives -= 1
        if enemy.lives == 0:
            enemies.remove(enemy)
        WIN.blit(ENEMY_IMG, (enemy.x, enemy.y))


# Drawing all elements
def draw_window(player, player_bullets, enemies):
    WIN.blit(PLAYER, (player.x, player.y))
    global player_lives
    lives_text = HEALTH_FONT.render(f'Lives: {str(player_lives)}', 1, WHITE)
    WIN.blit(lives_text, (10, 10))
    handle_enemy_action(player, enemies, player_bullets)
    for bullet in player_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


# Player movement
def handle_player_movement(player, pressed_keys):
    if pressed_keys[pygame.K_w] and player.y > 0:  # UP
        player.y -= PLAYER_VEL
    if pressed_keys[pygame.K_s] and player.y + PLAYER_SIZE[1] < SCREEN_SIZE[1]:  # DOWN
        player.y += PLAYER_VEL
    if pressed_keys[pygame.K_a] and player.x > 0:  # LEFT
        player.x -= PLAYER_VEL
    if pressed_keys[pygame.K_d] and player.x + PLAYER_SIZE[0] < SCREEN_SIZE[0]:  # RIGHT
        player.x += PLAYER_VEL

# Player bullets movement and deletion
def handle_player_bullets(player_bullets):
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            player_bullets.remove(bullet)
            
            
def draw_game_over():
    draw_text = GAME_OVER_FONT.render('Game Over', 1, WHITE)
    WIN.blit(draw_text, (SCREEN_SIZE[0] // 2 - draw_text.get_width() // 2, SCREEN_SIZE[1] // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    run = True
    clock = pygame.time.Clock()
    player = pygame.Rect(SCREEN_SIZE[0]//2 - PLAYER.get_width(), SCREEN_SIZE[1] - PLAYER_SIZE[0], PLAYER_SIZE[0], PLAYER_SIZE[1])
    player_bullets = []
    bg_move = 0
    enemies = []
    max_enemies = 5
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # Bullet handling
                if event.key == pygame.K_SPACE:
                    if len(player_bullets) < max_player_bullets:
                        bullet_rect = pygame.Rect(
                            player.x + 10, player.y, 3, 10)
                        player_bullets.append(bullet_rect)
            if event.type == ENEMY_ADD_EVENT:
                if len(enemies) < max_enemies:
                    enemy_rand_x = random.randint(0 + ENEMY_SIZE[0], SCREEN_SIZE[0] - ENEMY_SIZE[0])
                    enemy = Enemy(enemy_rand_x, -20)
                    enemies.append(enemy)   
            if event.type == ENEMY_SHOOT_EVENT:
                for enemy in enemies:
                    bullet = pygame.Rect(enemy.x + 10, enemy.y, 3, 10)
                    enemy.bullets.append(bullet)
            pressed_keys = pygame.key.get_pressed()   
        if player_lives == 0:
            draw_game_over()
            break
            
        # Background Loop
        WIN.fill(BLACK)
        WIN.blit(BACKGROUND, (0, bg_move))
        WIN.blit(BACKGROUND, (0, -(600 - bg_move)))
        if bg_move == 600:
            bg_move = 0
        bg_move += bg_vel
        # ----------------
        handle_player_movement(player, pressed_keys)
        handle_player_bullets(player_bullets)
        draw_window(player, player_bullets, enemies)


if __name__ == '__main__':
    main()