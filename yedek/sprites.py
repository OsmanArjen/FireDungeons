import pygame as pg 
from settings import *
import math
from itertools import cycle
from random import randint,choice,uniform

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self.groups = Walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):

        pg.sprite.Sprite.__init__(self)
        self.image = imageload("assets/heroes/knight/idle/knight_idle_anim_f0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.vx=self.vy=0
        self.x,self.y = x,y

        self.last_update=pg.time.get_ticks()
        self.hitbox= rect(self.rect.x,self.rect.y,0,0)
        self.direction="right"
        self.anims={
        "runright":from_folder("assets/heroes/knight/run"),
        "runleft":flip_folder(from_folder("assets/heroes/knight/run"),True,False),
        "idleright":from_folder("assets/heroes/knight/idle"),
        "idleleft":flip_folder(from_folder("assets/heroes/knight/idle"),True,False),
        }
        self.anim=self.anims["idleright"]
        self.animcount=0

        self.Health=100
        self.inventory=cycle([Gun("1","pistol"),Gun("2", "shotgun"),Sword("GreatSword")])
        self.weapon=next(self.inventory)
        self.last_shot=0
    def get_key(self):
        key=pg.key.get_pressed()
        self.vx,self.vy=0,0
        self.anim=self.anims["idle{}".format(self.direction)]



        if key[pg.K_w]:                                                                    
            self.vy=-PLAYER_SPEED
            self.anim=self.anims["run{}".format(self.direction)]
        elif key[pg.K_s]:
            self.vy=PLAYER_SPEED
            self.anim=self.anims["run{}".format(self.direction)]
        if key[pg.K_d]:
            self.vx=PLAYER_SPEED
            self.direction="right"
            self.anim=self.anims["runright"]
        elif key[pg.K_a]:
            self.vx=-PLAYER_SPEED
            
            self.direction="left"
            self.anim=self.anims["runleft"]
        if pg.mouse.get_pressed()[0]:
            if self.weapon.type=="pistol" or self.weapon.type=="shotgun":
                now=pg.time.get_ticks()
                if now-self.last_shot > 250:
                    self.last_shot=now
                    self.weapon.shoot(self)

        #if self.vx != 0 and self.vy != 0:
        #  self.vx *= 0.7071
        #  self.vy *= 0.7071



    def collide_with_walls(self, dir):
        if dir == 'x':
           hits = pg.sprite.spritecollide(self, Walls, False,collide)
           if hits:
             if self.vx > 0:
              self.x = hits[0].rect.left - self.hitbox.width
             if self.vx < 0:
              self.x = hits[0].rect.right
             self.vx = 0
             self.rect.x = self.x
             self.hitbox.x=self.x
        if dir == 'y':
           hits = pg.sprite.spritecollide(self, Walls, False,collide)
           if hits:
             if self.vy > 0:
              self.y = hits[0].rect.top - self.hitbox.height-40
             if self.vy < 0:
              self.y = hits[0].rect.bottom-40
             self.vy = 0
             self.rect.y = self.y
             self.hitbox.y=self.y+40
             

    def update(self,dt,scroll):
        self.get_key()
        self.hitbox= rect(self.hitbox.x,self.hitbox.y,64,24)
        
        now=pg.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update = now

            if self.animcount >= len(self.anim):
                self.animcount = 0

            else:
                self.image = self.anim[self.animcount]
            self.animcount += 1


        self.x += self.vx * dt
        self.y += self.vy * dt

        self.hitbox.x=self.x
        self.rect.x=self.x

        self.collide_with_walls("x")
        self.rect.y=self.y
        self.hitbox.y=self.y+40
        self.collide_with_walls("y")
        
        self.weapon.update(self,scroll)



#------------------------------------------------------------------------------------------
class Gun(pg.sprite.Sprite):
    def __init__(self,no,Type):
        self.type=Type
        pg.sprite.Sprite.__init__(self)
        self.image=Guns[no].convert_alpha()
        self.right=self.image
        self.left=flip(self.image,True,False)
        self.original_img=self.image
        self.dir="right"
        self.gun_flashes=from_folder("assets/muzzleflash")
        self.gun_flashes_group=pg.sprite.Group()
    def shoot(self,player):

        if self.type == "shotgun":


            pg.mixer.Sound("assets/sounds/shotgun.wav").play()
            if self.dir=="right":

                vel_x = math.cos(self.angle) * 900
                vel_y = math.sin(self.angle) * 900

                player.vx-=int(math.cos(self.angle)*600)
                player.vy-=int(math.sin(self.angle)*600)

            else:
                vel_x = -math.cos(self.angle) * 900
                vel_y = -math.sin(self.angle) * 900
                player.vx+=int(math.cos(self.angle)*600)
                player.vy+=int(math.sin(self.angle)*600)
            for i in range(1,6):
                Bullet(self.rect.centerx-9, self.rect.centery-9,vel_x*i,vel_y*randint(1,6))

        elif self.type == "pistol":
            pg.mixer.Sound("assets/sounds/pistol.wav").play()

            if self.dir=="right":

                vel_x = math.cos(self.angle) * 900
                vel_y = math.sin(self.angle) * 900

                player.vx-=int(math.cos(self.angle)*200)
                player.vy-=int(math.sin(self.angle)*200)

            else:
                vel_x = -math.cos(self.angle) * 900
                vel_y = -math.sin(self.angle) * 900
                player.vx+=int(math.cos(self.angle)*200)
                player.vy+=int(math.sin(self.angle)*200)


            Bullet(self.rect.centerx-9, self.rect.centery-9,vel_x,vel_y)

    def update(self,player,scroll):

        if player.direction=="right":

            self.rect=self.image.get_rect(center=(player.rect.center[0]+7,player.rect.center[1]+10))

        elif player.direction=="left":

            self.rect=self.image.get_rect(center=(player.rect.center[0]-7,player.rect.center[1]+10))

        self.rotate(player,scroll)

    def rotate(self,player,scroll):
        mouse_position = pg.mouse.get_pos()

        Mx,_=mouse_position

        if Mx > player.rect.centerx-scroll[0]:
            self.dir="right"
            self.original_img=self.right
            rise = mouse_position[1] - player.rect.centery+scroll[1]
            run = mouse_position[0] - player.rect.centerx+scroll[0]
        elif Mx < player.rect.centerx-scroll[0]:
            self.dir="left"
            self.original_img=self.left
            rise = -mouse_position[1] + player.rect.centery-scroll[1]
            run = -mouse_position[0] + player.rect.centerx-scroll[0]
        else:
            self.dir="right"
            self.original_img=self.right
            rise = mouse_position[1] - player.rect.centery+scroll[1]
            run = mouse_position[0] - player.rect.centerx+scroll[0]   

        self.angle = math.atan2(rise, run)
        self.image = pg.transform.rotate(self.original_img, -math.degrees(self.angle))
        self.rect=self.image.get_rect(center=self.rect.center)


class Sword(pg.sprite.Sprite):
    def __init__(self,Type):
        self.type="sword"
        pg.sprite.Sprite.__init__(self)
        #----------------------------------------------------------------------------
        self.anim=scale_from_folder("assets/melee/Sprites/{} Sprites".format(Type),(80,90))
        self.right=self.anim
        self.left=flip_folder(self.anim,True,False)
        self.image=self.anim[0]
        self.rect=self.image.get_rect()
        self.rect=rect(self.rect.topleft,self.rect.size)
        #----------------------------------------------------------------------------
        self.animCounter=0
        self.last_update=pg.time.get_ticks()
        self.attack=False
    def update(self,player,scroll):
        
        if player.direction=="right":
            self.rect.center=(player.rect.center[0]+45,player.rect.center[1]+10)
            self.anim=self.right
            self.hitbox=rect((self.rect.topleft[0]-20,self.rect.topleft[1]+10),(self.rect.size[0],self.rect.size[1]-20))
        else:
            self.rect.center=(player.rect.center[0]-45,player.rect.center[1]+10)
            self.anim=self.left  
            self.hitbox=rect((self.rect.topleft[0]+20,self.rect.topleft[1]+10),(self.rect.size[0],self.rect.size[1]-20))
        if pg.mouse.get_pressed()[0] and self.attack==False:
            pg.mixer.Sound("assets/sounds/slash.wav").play()
            self.attack=True
        if self.attack==True:
            now=pg.time.get_ticks()
            if now-self.last_update > 40:
                self.last_update=now
                if self.animCounter ==len(self.anim)-1:
                    self.animCounter=0
                    self.attack=False
                else:
                    self.image=self.anim[self.animCounter]

                self.animCounter+=1
        else:
            if player.direction=="right":
                self.image=self.right[0]

            else:
                self.image=self.left[0]

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,vel_x,vel_y):
        self.groups=Bullets
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image=imageload("assets/Guns/bullet.png").convert_alpha()
        self.rect=self.image.get_rect(center=(x,y))
        self.vx=vel_x
        self.vy=vel_y
        self.x,self.y=x,y
        self.spawn_time=pg.time.get_ticks()
    def update(self,player,dt):
        if pg.sprite.spritecollide(self,Walls,False):
            self.kill()
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.x=self.x
        self.rect.y=self.y


class Torch(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = Torchs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.anim=scale_from_folder("assets/torch",(32,32))
        self.image=self.anim[0]
        self.rect=self.image.get_rect(center=(x,y))
        self.animcount=0
        self.last_update=pg.time.get_ticks()
    def update(self):
        now=pg.time.get_ticks()
        if now- self.last_update > 60:
            self.last_update=now
            if self.animcount == len(self.anim)-1:
                self.animcount=0

            else:
                self.image=self.anim[self.animcount]
            self.animcount +=1
