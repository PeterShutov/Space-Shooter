from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 1190:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet1.png', self.rect.centerx, self.rect.top, 10, 30, -60)
        bullets.add(bullet)

    def boss_fire(self):
        bullet_boss = Bullet('bullet_boss.png', self.rect.centerx, self.rect.top, 70, 90, -50)
        bullets_boss.add(bullet_boss)

lost = 0
score = 0

num_fire = 0
num_boss_fire = 0

life = 5

rel_time = False
rel_boss_time = False

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 800:
            self.rect.x = randint(50, 1100)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()
bullets_boss = sprite.Group()
monsters2 = sprite.Group()
boss_group = sprite.Group()
meteor_group = sprite.Group()

player1 = Player('player.png', 325, 700, 100, 100, 25)

for _ in range(2):
    enemy1 = Enemy('enemy2_2.png', randint(80, 1100), 50, 100, 100, randint(1, 5))
    monsters.add(enemy1)

for _ in range(2):
    enemy2 = Enemy('enemy1_1.png', randint(80, 1100), 50, 100, 100, randint(1, 5))
    monsters2.add(enemy2)

for _ in range(1):
    boss = Enemy('boss2.png', randint(80, 1100), 50, 100, 100, randint(1, 5))
    boss_group.add(boss)

for _ in range(2):
    meteor = Enemy('meteor_2.png', randint(80, 1100), 50, 100, 100, randint(1, 3))
    meteor_group.add(meteor)

window = display.set_mode((1200, 800))
display.set_caption('pygame window')
background = transform.scale(image.load('background2.png'), (1200, 800))
display.set_icon(image.load("rocket.bmp"))

clock = time.Clock()
mixer.init()
mixer.music.load('Galactic Rap.mp3')

fire_soun = mixer.Sound('blaster_1.ogg')
fire_soun_2 = mixer.Sound('blaster_2.ogg')
mixer.music.play()
game = True
font.init()
font1 = font.SysFont('candara', 40)
font_loos = font.SysFont('candara', 100)
font_victory = font.SysFont('candara', 100)

finish = False

while game:
    

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_w:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player1.fire()
                    fire_soun.play()

                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    lost_time = timer()

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_boss_fire < 5 and rel_boss_time == False:
                    num_boss_fire += 1
                    player1.boss_fire()
                    fire_soun_2.play()
                if num_boss_fire >= 5 and rel_boss_time == False:
                    rel_boss_time = True
                    lost_boss_time = timer()

    if finish != True:
        window.blit(background, (0, 0))
        text = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        text_score = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
        text_loos = font_loos.render('GAME OVER!', True, (255, 0, 0))
        text_victory = font_loos.render('YOU WIN!', True, (0, 255, 0))

        window.blit(text, (20, 20))
        window.blit(text_score, (20, 65))
        

    
        player1.reset()
        
        bullets.draw(window)
        bullets_boss.draw(window)
        monsters.draw(window)
        monsters2.draw(window)
        boss_group.draw(window)
        meteor_group.draw(window)

        bullets.update()
        player1.update()
        bullets_boss.update()
        monsters.update()
        monsters2.update()
        boss_group.update()
        meteor_group.update()

        if rel_time == True:
            new_time = timer()
            if new_time - lost_time < 3:
                text2 = font1.render('Идёт перезарядка!', True, (255, 255, 255))
                window.blit(text2, (300, 200))
            else:
                num_fire = 0
                rel_time = False

        if rel_boss_time == True:
            new_boss_time = timer()
            if new_boss_time - lost_boss_time < 3:
                text3 = font1.render('Идёт перезарядка!', True, (255, 255, 255))
                window.blit(text3, (300, 200))
            else:
                num_boss_fire = 0
                rel_boss_time = False

        sprite_collides1 = sprite.groupcollide(monsters, bullets, True, True) or sprite.groupcollide(monsters, bullets_boss, True, True)
        
        for _ in sprite_collides1:
            score += 1
            enemy1 = Enemy('enemy2_2.png', randint(80, 1100), 50, 100, 100, randint(1, 5))
            monsters.add(enemy1)

        sprite_collides2 = sprite.groupcollide(monsters2, bullets, True, True) or sprite.groupcollide(monsters2, bullets_boss, True, True)
        for _ in sprite_collides2:
            score += 1
            enemy2 = Enemy('enemy1_1.png', randint(80, 1100), 50, 100, 100, randint(1, 5))
            monsters.add(enemy2)

        sprite_collides3 = sprite.groupcollide(boss_group, bullets_boss, True, True)


        for _ in sprite_collides3:
            score += 1
            boss = Enemy('boss2.png', randint(80, 1100), 50, 100, 100, randint(1, 5))
            boss_group.add(boss)

        sprite_collides4 = sprite.groupcollide(meteor_group, bullets_boss, True, True)

        for _ in sprite_collides4:
            meteor = Enemy('meteor_2.png', randint(80, 1100), 50, 100, 100, randint(1, 3))
            meteor_group.add(meteor)


        if sprite.spritecollide(player1, monsters, False) or sprite.spritecollide(player1, monsters2, False) or sprite.spritecollide(player1, boss_group, False) or sprite.spritecollide(player1, meteor_group, False):
            sprite.spritecollide(player1, monsters, True)
            sprite.spritecollide(player1, monsters2, True)
            sprite.spritecollide(player1, boss_group, True)
            sprite.spritecollide(player1, meteor_group, True)
            life -= 1

        if life == 0 or lost > 3:
            finish = True
            window.blit(text_loos, (300, 200))


        if score >= 10:
            finish = True
            window.blit(text_victory, (120, 200))

        if life == 5:
            color = (14, 161, 39)
        elif life == 4:
            color = (88, 161, 14)
        elif life == 3:
            color = (154, 166, 20)
        elif life == 2:
            color = (166, 117, 20)
        elif life == 1:
            color = (166, 20, 20)

        text_HP = font1.render('Осталось HP: ' + str(life), True, color)
        window.blit(text_HP, (20, 110))
        display.update()

    else:
        finish = False
        life = 5
        num_fire = 0
        num_boss_fire = 0

        
        score = 0
        lost = 0
        for b in bullets:
            b.kill()

        for b in bullets_boss:
            b.kill()

        for b in monsters:
            b.kill()

        for b in monsters2:
            b.kill()

        for b in boss_group:
            b.kill()

        for b in meteor_group:
            b.kill()

        time.delay(3000)

        for _ in range(2):
            enemy1 = Enemy('enemy2_2.png', randint(80, 1100), 50, 100, 100, randint(1, 3))
            monsters.add(enemy1)

        for _ in range(2):
            enemy2 = Enemy('enemy1_1.png', randint(80, 1100), 50, 100, 100, randint(1, 3))
            monsters2.add(enemy2)

        for _ in range(1):
            boss = Enemy('boss2.png', randint(80, 1100), 50, 100, 100, randint(1, 3))
            boss_group.add(boss)

        for _ in range(2):
            meteor = Enemy('meteor_2.png', randint(80, 1100), 50, 100, 100, randint(1, 3))
            meteor_group.add(meteor)




    
    time.delay(50)
