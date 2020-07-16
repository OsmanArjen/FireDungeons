import pygame as pg
import os
import random
vec = pg.math.Vector2
BARREL_OFFSET = vec(30, 10)
__author__ = "efeosmanaslanoglu"

TITLE = "Fire Dungeons"
WIDTH = 894
HEIGHT = 594
PLAYER_SPEED=250
#-------short cuts----
rect=pg.Rect

imageload=pg.image.load

flip=pg.transform.flip
#--------------------
Torchs=pg.sprite.Group()
Walls=pg.sprite.Group()
Bullets=pg.sprite.Group()

#--------------------
particles=[]
smokes=[]
all_particles = []


Groups = [Walls,Bullets,Torchs]
#-------------------
FPS = 60
def ResetGroups():
  for group in Groups:
      group.empty()
  for particle in all_particles:
      particle.clear()
  

def from_folder(folder : str):
    """Dosyadaki resimlerden liste oluşturur."""
    dosyalar = sorted(os.listdir(folder))
    images = []
    for i in dosyalar:
        images.append(pg.image.load(os.path.join(folder,i)).convert_alpha())
    return images
def scale2x_from_folder(folder: str):
    dosyalar = sorted(os.listdir(folder))
    images = []
    for i in dosyalar:
        images.append(pg.transform.scale2x(pg.image.load(os.path.join(folder,i))).convert_alpha())
    return images
def scale_from_folder(folder: str,scale):
    dosyalar = sorted(os.listdir(folder))
    images = []
    for i in dosyalar:
        images.append(pg.transform.scale(pg.image.load(os.path.join(folder,i)),scale).convert_alpha())
    return images
def flip_folder(Images,xbool=False,ybool=False):
    return [flip(image,xbool,ybool) for image in Images]

def blit_text(surface, text, pos, font, color=pg.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()

    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def collide(sprite,other):
    return other.rect.colliderect(sprite.hitbox)

Guns={
"1":pg.image.load("assets/Guns/Gun_1.png"),
"2":pg.image.load("assets/Guns/Gun_2.png"),
"bullet":pg.image.load("assets/Guns/bullet.png")
 }
