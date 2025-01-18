from pygame import *
from random import randint
 
 
#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
 
#fonts and captions
font.init()
font2 = font.Font(None, 36)
 
 
#we need the following images:
img_back = "galaxy.jpg" # game background
img_hero = "rocket.png" # hero
img_enemy = "ufo.png" # enemy
img_bullet = "bullet.png"
img_asterode = "asteroid.png"
 
 
score = 0 #ships destroyed
lost = 0 #ships missed
 
 
#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
 
 
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
 
        #every sprite must have the rect property that represents the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
  #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet ,self.rect.centerx,ship.rect.centery, 15, 20, 15,)
        bullets.add(bullet)

   
class Enemy(GameSprite):
   #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
 
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
 
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

asteriods = sprite.Group()
for i in range(1, 3):
    asteriod = Enemy(img_asterode, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteriods.add(asteriod)

bullets = sprite.Group()
goal = 15
max_lost = 15

#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
while run:
   #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    

    if not finish:
        #update the background
        window.blit(background,(0,0))
 
 
       #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        lose = font2.render("You Lose", 1, (168, 50, 50))
        win = font2.render("You win", 1, (50, 168, 50))
 
 
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
 
       #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteriods.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        

        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monster.add(monsters)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteriods, False):
            finish = True
            window.blit(lose,(300,200))


        if score >= goal:  
            finish = True
            window.blit(win, (300,200))

        

 
        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteriods.draw(window)
        display.update()

    
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
            monsters.add(monster)

    #the loop is executed each 0.05 sec
    time.delay(50)

