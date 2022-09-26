from asyncore import read
from turtle import Screen, distance, window_width
import pygame

import random
import square
import math

import button


pygame.init()


screen_width = 850
screen_height = 600
surface = pygame.display.set_mode((screen_width,screen_height))


black = 0,0,0
background=pygame.image.load('background.jpg')

playerImg=pygame.image.load('space-invaders.png')

alienImg=pygame.image.load('alien.png')

GREEN_SPACE_SHIP = pygame.image.load('pixel_ship_green_small.png')


bulletImg=pygame.image.load('pixel_laser_blue.png')


enemy_bulletImg=pygame.image.load('pixel_laser_red.png')
GREEN_LASER = pygame.image.load('pixel_laser_green.png')
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)



class character:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(screen_height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = playerImg
        self.laser_img = bulletImg
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(screen_height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(character):
    COLOR_MAP = {
                "red": (alienImg, enemy_bulletImg),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None




def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    score = 0
    main_font = pygame.font.Font("digital-7.ttf", 50)
    lost_font = pygame.font.Font("digital-7.ttf", 60)


    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5


    player =Player(370,480)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        surface.fill((0,0,0))
        surface.blit(background,(0,0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label =main_font.render(f"score: {score}", 1, (255,255,255))

        surface.blit(lives_label, (10, 10))
        surface.blit(level_label, (screen_width - level_label.get_width() - 10, 10))
       # surface.blit(score_label,(screen_width/2,10))


        for enemy in enemies:
            enemy.draw(surface)
        
        player.draw(surface)

        if lost:
            lost_label = lost_font.render("GAME OVER !", 1, (255,255,255))
            surface.blit(lost_label, (screen_width/2 - lost_label.get_width()/2, 350))

        pygame.display.update()



    
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width-100), random.randrange(-1500, -100), random.choice(["red","green"]))
                enemies.append(enemy)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < screen_width: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < screen_height: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1
                enemies.remove(enemy)
               

        player.move_lasers(-laser_vel, enemies)
        


def main_menu():


   title_font = pygame.font.Font("digital-7.ttf", 70)

   screen_width = 850
   screen_height = 600
   Screen= pygame.display.set_mode((screen_width,screen_height)) 
   pygame.display.set_caption('Play Game!')
   start_img=pygame.image.load('start_btn.png').convert_alpha()
   Start_button=button.Button(300, 200, start_img,0.6)
   run=True
   while run:
    Screen.fill((0,0,0))
    Screen.blit(background,(0,0))
    title_label = title_font.render("Press Start To Play", 1, (255,255,255))
    surface.blit(title_label, (screen_width/2- title_label.get_width()/2, 350))

    if Start_button.draw(Screen):
        print('action')
        main()

        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
    pygame.display.flip()
    

    
 

main_menu()



