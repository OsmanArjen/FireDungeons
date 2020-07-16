import pygame as pg
import math as mth
from settings import *
from itertools import cycle
from random import randint

vec = pg.math.Vector2

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self,Walls)
        self.rect = pg.Rect(x, y, w, h)



class Player(pg.sprite.Sprite):
    def __init__(self, x, y):

        pg.sprite.Sprite.__init__(self)
        self.image = imageload("assets/heroes/knight/idle/knight_idle_anim_f0.png").convert_alpha()

        self.rect = self.image.get_rect(topleft=(x,y))

        self.hitbox = rect(x,y,64,24)

        self.vel = vec(0, 0)

        self.pos = vec(x, y)

        self.last_update = pg.time.get_ticks()

        self.direction = "right"
 
        self.Anims = {
            "runright":from_folder("assets/heroes/knight/run"),
            "runleft":flip_folder(from_folder("assets/heroes/knight/run"),True,False),
            "idleright":from_folder("assets/heroes/knight/idle"),
            "idleleft":flip_folder(from_folder("assets/heroes/knight/idle"),True,False),
        }

        self.anim = self.Anims["idleright"]

        self.animcount = 0

        self.Health = 100

        self.inventory = cycle([Sword("GreatSword"),Gun("1","pistol"),Gun("2","shotgun")])

        self.weapon = next(self.inventory)

    def get_key(self):

        key = pg.key.get_pressed()

        self.vel = vec(0,0)

        self.anim = self.Anims[f"idle{self.direction}"]



        if key[pg.K_w]:

            self.vel.y = -PLAYER_SPEED

            self.anim = self.Anims[f"run{self.direction}"]

        elif key[pg.K_s]:

            self.vel.y = PLAYER_SPEED

            self.anim = self.Anims[f"run{self.direction}"]

        if key[pg.K_d]:

            self.vel.x = PLAYER_SPEED

            self.direction = "right"

            self.anim = self.Anims["runright"]

        elif key[pg.K_a]:

            self.vel.x = -PLAYER_SPEED

            self.direction = "left"

            self.anim = self.Anims["runleft"]
        





    def collide_with_walls(self, dir):
        if dir == 'x':
           hits = pg.sprite.spritecollide(self, Walls, False,collide)
           if hits:
                if self.vel.x > 0:

                    self.pos.x = hits[0].rect.left - self.hitbox.width

                if self.vel.x < 0:

                    self.pos.x = hits[0].rect.right

                self.vel.x = 0

                self.rect.x = self.pos.x

                self.hitbox.x=self.pos.x

        if dir == 'y':

           hits = pg.sprite.spritecollide(self, Walls, False,collide)

           if hits:

                if self.vel.y > 0:

                    self.pos.y = hits[0].rect.top - self.hitbox.height - PLAYER_RECT_OFFSET

                if self.vel.y < 0:

                    self.pos.y = hits[0].rect.bottom-PLAYER_RECT_OFFSET

                self.vel.y = 0

                self.rect.y = self.pos.y

                self.hitbox.y = self.pos.y + PLAYER_RECT_OFFSET


    def update(self, dt, scroll):

        self.get_key()


        now = pg.time.get_ticks()

        if now - self.last_update > 50:

            self.last_update = now

            if self.animcount >= len(self.anim):

                self.animcount = 0

            else:

                self.image = self.anim[self.animcount]

            self.animcount += 1


        self.pos += self.vel * dt


        self.hitbox.x = self.pos.x

        self.rect.x = self.pos.x

        self.collide_with_walls("x")

        self.rect.y = self.pos.y

        self.hitbox.y = self.pos.y + PLAYER_RECT_OFFSET

        self.collide_with_walls("y")

        self.weapon.update(self,scroll)



#------------------------------------------------------------------------------------------
class Gun(pg.sprite.Sprite):
    def __init__(self,no,Type):
        self.type = Type

        pg.sprite.Sprite.__init__(self)

        self.image = Guns[no].convert_alpha()

        self.right = self.image

        self.left = flip(self.image,True,False)

        self.original_img = self.right

        self.dir = "right"


    def shoot(self,player):

        if self.type == "shotgun":


            pg.mixer.Sound("assets/sounds/shotgun.wav").play()

            if self.dir == "right":

                vel_x = mth.cos(self.angle) * 450
                vel_y = mth.sin(self.angle) * 450



            else:

                vel_x = -mth.cos(self.angle) * 450
                vel_y = -mth.sin(self.angle) * 450


            Bullet(self.rect.centerx, self.rect.centery,vel_x,vel_y)

        elif self.type == "pistol":

            pg.mixer.Sound("assets/sounds/pistol.wav").play()

            if self.dir == "right":

                vel_x = mth.cos(self.angle) * 900
                vel_y = mth.sin(self.angle) * 900



            else:

                vel_x = -mth.cos(self.angle) * 900
                vel_y = -mth.sin(self.angle) * 900



            Bullet(self.rect.centerx, self.rect.centery,vel_x,vel_y)

    def update(self,player,scroll):
        #=================================================================================================================
        if player.direction == "right":

            self.rect = self.image.get_rect(center=(player.rect.center[0]+7,player.rect.center[1]+10))

        elif player.direction == "left":

            self.rect = self.image.get_rect(center=(player.rect.center[0]-7,player.rect.center[1]+10))

        self.rotate(player,scroll)
        #=================================================================================================================
    def rotate(self,player,scroll):
        mouse_position = pg.mouse.get_pos()

        Mx,_=mouse_position

        if Mx > player.rect.centerx-scroll[0]:

            self.dir = "right"

            self.original_img = self.right

            rise = mouse_position[1] - player.rect.centery+scroll[1]

            run = mouse_position[0] - player.rect.centerx+scroll[0]

        elif Mx < player.rect.centerx-scroll[0]:

            self.dir = "left"

            self.original_img = self.left

            rise = -mouse_position[1] + player.rect.centery-scroll[1]

            run = -mouse_position[0] + player.rect.centerx-scroll[0]

        else:

            self.dir = "right"

            self.original_img = self.right

            rise = mouse_position[1] - player.rect.centery+scroll[1]

            run = mouse_position[0] - player.rect.centerx+scroll[0]

        self.angle = mth.atan2(rise, run)

        self.image = pg.transform.rotate(self.original_img, -mth.degrees(self.angle))

        self.rect = self.image.get_rect(center=self.rect.center)


class Sword(pg.sprite.Sprite):
    def __init__(self,Type):
        self.type = Type

        pg.sprite.Sprite.__init__(self)

        #----------------------------------------------------------------------------
        self.anim = scale_from_folder(f"assets/melee/Sprites/{Type} Sprites",(80,90))

        self.right = self.anim

        self.left = flip_folder(self.anim,True,False)

        self.image = self.anim[0]

        self.rect = self.image.get_rect()

        self.rect = rect(self.rect.topleft,self.rect.size)
        #----------------------------------------------------------------------------
        self.Counter = 0

        self.last_update = pg.time.get_ticks()

        self.attack = False


    def update(self,player,scroll):
        #=================================================================================================================
        if player.direction == "right":

            self.rect.center = (player.rect.center[0]+45,player.rect.center[1]+10)

            self.hitbox = rect((self.rect.topleft[0]-25,self.rect.topleft[1]+10),(self.rect.size[0]-5,self.rect.size[1]-20))

            self.anim = self.right

        else:

            self.rect.center = (player.rect.center[0]-45,player.rect.center[1]+10)

            self.hitbox = rect((self.rect.topleft[0]+25,self.rect.topleft[1]+10),(self.rect.size[0]-5,self.rect.size[1]-20))

            self.anim = self.left

        #=================================================================================================================
        if self.attack == True:

            now = pg.time.get_ticks()

            if now-self.last_update > MELEE["sword"]["speed"]:

                self.last_update = now

                if self.Counter == len(self.anim)-1:

                    self.Counter = 0

                    self.attack = False

                else:

                    self.image = self.anim[self.Counter]

                self.Counter += 1
        else:

            self.image = self.anim[0]


        #=================================================================================================================
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,vel_x,vel_y):

        pg.sprite.Sprite.__init__(self,Bullets)

        self.image = imageload("assets/Guns/bullet.png").convert_alpha()

        self.rect = self.image.get_rect(center=(x,y))

        #=================================================================================================================
        self.vel = vec(vel_x, vel_y)

        self.pos = vec(x,y)
        #=================================================================================================================
        self.spawn_time = pg.time.get_ticks()

    def update(self,player,dt):

        if pg.sprite.spritecollide(self,Walls,False):

            self.kill()

        self.pos += self.vel * dt

        self.rect.center = self.pos



class Torch(pg.sprite.Sprite):
    def __init__(self, x, y):

        pg.sprite.Sprite.__init__(self,Torchs)

        self.anim = scale_from_folder("assets/torch",(32,32))

        self.image = self.anim[0]

        self.rect = self.image.get_rect(center=(x,y))

        self.animcount = 0

        self.last_update = pg.time.get_ticks()

    def update(self):

        now = pg.time.get_ticks()
        
        if now - self.last_update > 60:

            self.last_update = now

            if self.animcount == len(self.anim)-1:

                self.animcount = 0

            else:

                self.image = self.anim[self.animcount]

            self.animcount += 1
