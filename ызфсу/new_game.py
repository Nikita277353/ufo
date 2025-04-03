from pygame import *
from random import randint

score = 0 
goals = 10
lost = 0 
max_lost = 3

win_width = 800
win_hight = 600
FPS = 40
window = display.set_mode((win_width, win_hight))
display.set_caption('Shooter')

img_bullet = 'bullet.png'
img_hero = 'roket1.png'
img_enemy = 'roket2.png'

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

bullets = sprite.Group()
enemies = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_hight:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -50
            lost += 1

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)
        fire_sound.play()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

player = Player(img_hero, win_width // 2, win_hight - 100, 50, 50, 10)

for _ in range(5):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 5))
    enemies.add(enemy)

finish = False
running = True

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            player.fire()
    
    if not finish:
        window.fill((0, 0, 0)) 
        player.update()
        player.reset()

        bullets.update()
        bullets.draw(window)

        enemies.update()
        enemies.draw(window)

        collisions = sprite.groupcollide(enemies, bullets, True, True)
        for _ in collisions:
            score += 1
            enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 5))
            enemies.add(enemy)

        font.init()
        font1 = font.SysFont('Arial', 36)
        text_score = font1.render(f"Score: {score}", True, (255, 255, 255))
        text_lost = font1.render(f"Lost: {lost}", True, (255, 255, 255))
        window.blit(text_score, (10, 10))
        window.blit(text_lost, (10, 50))

        if lost >= max_lost or score >= goals:
            finish = True
            text_finish = font1.render(
                'Game Over' if lost >= max_lost else 'You Win!',
                True, (255, 0, 0)
            )
            window.blit(text_finish, (win_width // 2 - 100, win_hight // 2 - 50))

    display.update()
    time.delay(FPS)
