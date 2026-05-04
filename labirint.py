from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        

    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and  packman.x_speed < 0:
            self.rect.x += self.x_speed
        
            platforms_touched = sprite.spritecollide(self, barriers, False)
            if self.x_speed > 0:
                for p in platforms_touched :
                    self.rect.right = min(self.rect.right, p.rect.left)
            elif self.x_speed < 0:
                for p in platforms_touched:
                    self.rect.left = max(self.rect.left, p.rect.right)
            
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and  packman.y_speed < 0:
            self.rect.y += self.y_speed
            platforms_touched = sprite.spritecollide(self, barriers, False)
            if self.y_speed > 0:
                for p in platforms_touched :
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.y_speed < 0:
                for p in platforms_touched:
                    self.rect.top = max(self.rect.top, p.rect.bottom)
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, playe_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = playe_speed
    
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, playe_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = playe_speed

    def update(self):
        if self.rect.x <= 30:
            self.side = "right"
        if self.rect.x >= win_width - 420:
            self.side = "left"
        
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, playe_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = playe_speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Maze Game Dhafia")
window = display.set_mode((win_width, win_height))
back = (114, 76, 142)
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 80, 50, 400)

barriers = sprite.Group()
bullets = sprite.Group()

barriers.add(w1)
barriers.add(w2)

packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
monster = Enemy('monster.png', win_width - 180, 140, 80, 80, 5 )
monster2 = Enemy('monster2.png', win_width - 180, 260, 80, 80, 5 )
monster3 = Enemy2('monster3.png', 50, 180, 80, 80, 5 )
treasure = GameSprite('final.png', win_width - 100, win_height - 100, 80, 80)

monsters = sprite.Group()
monsters2 = sprite.Group()
monsters.add(monster)
monsters.add(monster2)
monsters2.add(monster3)

run = True
finish = False

while run:
    time.delay(50)
  
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                packman.x_speed = -10
            elif e.key == K_d:
                packman.x_speed = 10
            elif e.key == K_w:
                packman.y_speed = -10
            elif e.key == K_s:
                packman.y_speed = 10
            elif e.key == K_SPACE:
                packman.fire()

        elif e.type == KEYUP:
            if e.key == K_a:
                packman.x_speed = 0
            elif e.key == K_d:
                packman.x_speed = 0
            elif e.key == K_w:
                packman.y_speed = 0
            elif e.key == K_s:
                packman.y_speed = 0
    
    if not finish:
        window.fill(back)

        barriers.draw(window)
        packman.reset()
        treasure.reset()

        packman.update()
        bullets.update()

        bullets.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)

        sprite.groupcollide(bullets, barriers, True, False)

        sprite.groupcollide(monsters2, bullets, True, True)
        monsters2.update()
        monsters2.draw(window)

        if sprite.spritecollide(packman, monsters, False):
            finish = True

            img = image.load('lose.png')
            d = img.get_width() // img.get_height()
            window.fill((208, 211, 245))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
        
        if sprite.spritecollide(packman, monsters2, False):
            finish = True

            img = image.load('lose.png')
            d = img.get_width() // img.get_height()
            window.fill((208, 211, 245))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


        if sprite.collide_rect(packman, treasure):
            finish = True

            img = image.load('win.jpg')
            window.fill((208, 211, 245))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    
    display.update()




