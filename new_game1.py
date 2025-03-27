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

background = transform.scale(image.load('galaxy.jpg'))
img_bullet = 'bullet.png'
img_hero = 'roket1.png'
img_enemy = 'roket2.png'
img_back = 'galaxy.jpg'


mixer.init()
mixer.music.load('space.ogg')
mixer_music.music.play()
fire_sound = mixer.Sound()
fire_sound.play()


bullets = sprite.Group


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = -50
            lost +=1

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x -= self.speed


    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


player = Player(img_hero, win_width //                                                                                            2, win_hight - 100, 50, 50, 10)

enemies = sprite.Group()
for _ in range(5):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 50, randint(1, 5))
    enemies.add(enemy)

finish = False

running = True
while  running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    

        
    display.update() #!!!
    time.delay(FPS)




