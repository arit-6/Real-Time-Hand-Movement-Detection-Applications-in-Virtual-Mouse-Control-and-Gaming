import pygame
from pygame.locals import *
import random

pygame.init()
width = 850
height = 650
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Hand Gesture Car")

clock = pygame.time.Clock()
fps = 120

font = pygame.font.Font(None, 36)  

background_image = pygame.image.load('images/back.jpg')
background_image = pygame.transform.scale(background_image, screen_size)  

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed=0):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 45 / image.get_rect().width
        vehicle_width = image.get_rect().width * image_scale
        vehicle_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(vehicle_width), int(vehicle_height)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

class Player(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/player (2).png')
        super().__init__(image, x, y)

    def position(self, cursor_x, cursor_y):
        self.rect.center = (cursor_x, cursor_y)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, height)

    def update(self, enemies):
        collisions = pygame.sprite.spritecollide(self, enemies, False)
        if collisions:
            crash_image = pygame.image.load('images/crash.png')
            screen.blit(crash_image, (self.rect.centerx - crash_image.get_width() / 2, self.rect.centery - crash_image.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)  
            pygame.quit()
            quit()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png') 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self, enemies):
        global score 
        self.rect.y -= self.speed
        collisions = pygame.sprite.spritecollide(self, enemies, True)
        if collisions:
            pygame.display.update()
            self.kill()
            score += 1
        if self.rect.top < 0:
            self.kill()

player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

player = Player(250, 400)
player_group.add(player)

RELOAD_COOLDOWN = 0.5
bullet_count = 0
reload_timer = 0

enemy_list = ['images/enemy4.png', 'images/enemy2.png', 'images/enemy1.png', 'images/enemy3.png']
def spawn_enemy_ship():
    if len(vehicle_group) < 6:
        if random.random() < 0.05:
            x = random.randint(0, width)
            y = random.randint(-100, -50)
            enemy = Vehicle(pygame.image.load(random.choice(enemy_list)), x, y, speed=1.8)
            vehicle_group.add(enemy)
score = 0

game_started = False

running = True
while running:
    clock.tick(fps)
    
    screen.blit(background_image, (0, 0))  

    if reload_timer > 0:
        reload_timer -= clock.get_time() / 500
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_x:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:  
            if reload_timer <= 0:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullet_group.add(bullet)
                bullet_count += 1
                reload_timer = RELOAD_COOLDOWN
        elif event.type == KEYDOWN and event.key == K_s and not game_started:
            game_started = True

    if game_started:
        cursor_x, cursor_y = pygame.mouse.get_pos()
        player.position(cursor_x, cursor_y)

        spawn_enemy_ship()

        bullet_group.update(vehicle_group)
        vehicle_group.update()

        player.update(vehicle_group)

        bullet_group.draw(screen)
        player_group.draw(screen)
        vehicle_group.draw(screen)
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        if reload_timer <= 0:
            screen.blit(font.render("Fire", True, (255, 255, 255)), (cursor_x - 20, cursor_y - 40))

        pygame.display.update()

pygame.quit()
