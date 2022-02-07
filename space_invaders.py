import pygame
import os 

# Window Init
pygame.init()
SCREEN_SIZE: tuple = 800, 600
FPS = 60
WIN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Space Invaders')

# Background and Style variables
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), SCREEN_SIZE)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
# Player Variables
PLAYER_SIZE: tuple = 65, 55
PLAYER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship.png')), PLAYER_SIZE), 180)
PLAYER_VEL = 5
# Bullet Variables
BULLET_VEL = 7
max_player_bullets = 10
  
    
# Drawing all elements
def draw_window(player, player_bullets):
    WIN.fill(BLACK)

    WIN.blit(BACKGROUND,(0, 0))
    WIN.blit(PLAYER, (player.x, player.y))

    for bullet in player_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()


# Player movement
def handle_player_movement(player, pressed_keys):
    if pressed_keys[pygame.K_w] and player.y > 0: # UP
        player.y -= PLAYER_VEL
    if pressed_keys[pygame.K_s] and player.y + PLAYER_SIZE[1] < SCREEN_SIZE[1]: # DOWN
        player.y += PLAYER_VEL 
    if pressed_keys[pygame.K_a] and player.x > 0: # LEFT
        player.x -= PLAYER_VEL 
    if pressed_keys[pygame.K_d] and player.x + PLAYER_SIZE[0] < SCREEN_SIZE[0]: # RIGHT
        player.x += PLAYER_VEL  

# Player bullets movement and deletion
def handle_player_bullets(player, player_bullets):
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            player_bullets.remove(bullet)

def main():
    run = True
    clock = pygame.time.Clock()
    player = pygame.Rect(SCREEN_SIZE[0]//2 - PLAYER.get_width(), SCREEN_SIZE[1] - PLAYER_SIZE[0], PLAYER_SIZE[0], PLAYER_SIZE[1])
    player_bullets = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Bullet handling
                if event.key == pygame.K_SPACE:
                    if len(player_bullets) < max_player_bullets:
                        bullet_rect = pygame.Rect(player.x + 10, player.y, 3, 10)
                        player_bullets.append(bullet_rect)
        
            pressed_keys = pygame.key.get_pressed()
        
        handle_player_movement(player, pressed_keys)
        handle_player_bullets(player, player_bullets)
        draw_window(player, player_bullets)

if __name__ == '__main__': main()