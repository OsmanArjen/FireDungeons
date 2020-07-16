import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tiledmap import *
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT),0,32)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        pg.mouse.set_visible(False)
        self.cursor=imageload("assets/gui/crosshair_4.png").convert_alpha()
        self.HealthBar=imageload("assets/gui/health_ui.png").convert_alpha()
        self.true_scroll = [0,0]
    def DrawHealthbar(self, health):

        HealthBar = pg.Rect(58, 16, health*1.2, 18)
        HealthBar2 = pg.Rect(58, 16, health*1.2, 6)


        pg.draw.rect(self.screen, (200,50,50), HealthBar)
        pg.draw.rect(self.screen, (255,50,50), HealthBar2)


        self.screen.blit(self.HealthBar, (20, 10))
    def load_map(self):

        self.player=Player(64,64)
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'levels')
        self.map=TiledMap(path.join(map_folder, 'Base.tmx'))
        self.map_img=self.map.make_map()
        self.map_img=pg.transform.scale(self.map_img,(258*32,24*32)).convert_alpha()

        self.map_rect=self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(tile_object.x*2, tile_object.y*2)

            elif tile_object.name == 'wall':
                Obstacle( tile_object.x*2, tile_object.y*2,tile_object.width*2, tile_object.height*2)
            elif tile_object.name == "torch":
                Torch(tile_object.x*2,tile_object.y*2)




    def new(self):
        # initialize all variables and do all the setup for a new game
        ResetGroups()
        self.load_map()
        



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):

        #print(self.clock.get_fps())
        self.true_scroll[0] += (self.player.rect.x-self.true_scroll[0]-447)/20
        self.true_scroll[1] += (self.player.rect.y-self.true_scroll[1]-297)/20
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
        self.player.update(self.dt,self.scroll)
        Bullets.update(self.player,self.dt)
        Torchs.update()


    def draw(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map_img,(self.map_rect.x-self.scroll[0],self.map_rect.y-self.scroll[1]))
        # Get mouse position
        Mx,My = pg.mouse.get_pos()

        # Blit the crosshair
        for sprite in Torchs:
            self.screen.blit(sprite.image,(sprite.rect.x-self.scroll[0],sprite.rect.y-self.scroll[1]))
        for sprite in Bullets:
            self.screen.blit(sprite.image,(sprite.rect.x-self.scroll[0],sprite.rect.y-self.scroll[1]))

        self.screen.blit(self.player.image,(self.player.rect.x-self.scroll[0],self.player.rect.y-self.scroll[1]))
        self.screen.blit(self.player.weapon.image,(self.player.weapon.rect.x-self.scroll[0],self.player.weapon.rect.y-self.scroll[1]))

            
        self.DrawHealthbar(self.player.Health)
        self.screen.blit(self.cursor,(Mx,My))

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5: 
                    self.player.weapon=next(self.player.inventory)




    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()