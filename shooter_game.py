from pygame import *
from random import randint
from time import time as timer
# фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
# шрифты и надписи
font.init()
font1 = font.Font(None, 80)
win = font1.render('ПОБЕДА! :-)',True,(0,255,0))
lose = font1.render('ПРОИГРЫШ :-(',True,(255,0,0))
font2 = font.Font(None, 36)
# герой
jedi_img = 'rocket.png'
# враг
C
asteroid_img = 'asteroid.png'
# пуля
bullet_img = 'bullet.png'
# сбито кораблей
score = 0
# пропущено кораблей
lost = 0
# количество жизней
lifes = 1
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_width,player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
# класс главного игрока
class Jedi(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-85:
            self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullets(bullet_img,self.rect.centerx-7,self.rect.top,-20,14,20)
        bullets.add(bullet)
# класс пуль
class Bullets(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
# класс спрайта-врага
class Sith(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(0,win_width-80)
            self.rect.y = -50
            self.speed = randint(1,5)
            lost += 1
# Создаем окошко
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Space Invaders')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
# создаем спрайты
jedi = Jedi(jedi_img,win_width/2-40,win_height-105,10,80,100)
siths = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    sith = Sith(sith_img,randint(0,win_width-80),-50,randint(1,5),80,50)
    siths.add(sith)
asteroids = sprite.Group()
for i in range(5):
    asteroid = Sith(asteroid_img,randint(0,win_width-80),-50,randint(3,7),50,50)
    asteroids.add(asteroid)
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
game = True
reload_time = False
# Основной цикл игры:
# флаг сбрасывается кнопкой закрытия окна
finish = False
num_fire = 0
 
while game:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if num_fire < 5 and reload_time == False:
                    fire_sound.play()
                    jedi.fire()
                    num_fire += 1

                if num_fire >= 5 and reload_time == False:
                    reload_time = True
                    last_time = timer()


 
    if finish == False:
        # обновляем фон
        window.blit(background, (0,0))
        # пишем текст на экране
        text_score = font2.render('Счёт: '+str(score),True,(200,255,200))
        window.blit(text_score,(10,20))
        text_lost = font2.render('Пропущено: '+str(lost),True,(200,255,200))
        window.blit(text_lost,(10,50))
        siths.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        # производим движения спрайтов
        jedi.update()
        siths.update()
        asteroids.update()
        bullets.update()
        # обновляем их в новом местоположении при каждой итерации цикла
        jedi.reset()

        if reload_time == True:
            cur_time = timer()
            if cur_time - last_time < 3:
                reload_text = font2.render('Перезарядка!...',1,(33,0,0))
                window.blit(reload_text,(200,350))
            else:
                reload_time = False
                num_fire = 0

        collides = sprite.groupcollide(siths,bullets,True,True)
        for c in collides:
            score += 1
            sith = Sith(sith_img,randint(0,win_width-80),-50,randint(1,5),80,50)
            siths.add(sith)
 
        if sprite.spritecollide(jedi,siths,False):
            lifes -= 1
        # проигрыш
        if lifes == 0 or lost >= 10:
            finish = True
            window.blit(lose,(150,200))
        # победа
        if score >= 20:
            finish = True
            window.blit(win,(150,200))
        display.update()
    else:
        time.delay(3000)
        finish = False
        score = 0
        lifes = 1
        lost = 0
        for b in bullets:
            b.kill()
        for s in siths:
            s.kill()
        for i in range(5):
            sith = Sith(sith_img,randint(0,win_width-80),-50,randint(1,5),80,50)
            siths.add(sith)
        # цикл срабатывает каждую 0.05 секунды
    time.delay(50)



        





