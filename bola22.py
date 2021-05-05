import pygame as pg
import sys
import random

ALTO =  600
ANCHO = 800

FPS = 60

class Marcador(pg.sprite.Sprite):
    def __init__(self, text, x, y, fontsize = 25, color = (255,255,255)):
        super().__init__()
        self.fuente = pg.font.SysFont("Fox Cavalier", fontsize)
        self.color = color
        self.text = text
        self.image = self.fuente.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self):
        self.image = self.fuente.render(str(self.text), True, self.color)

class Bola(pg.sprite.Sprite):
    def __init__(self, x, y):
        #Activamos los métodos de la clase "madre" Sprite
        #pg.sprite.Sprite.__init__(self) <-- la manera clásica
        super().__init__() # <-- la super manera
        self.image = pg.image.load("images/ball1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))

        self.vx = random.randint(5,10) * random.choice([-1,1])
        self.vy = random.randint(5,10) * random.choice([-1,1])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.vy *= -1

class Raqueta(pg.sprite.Sprite):
    fotos = ["electric00.png",
            "electric01.png",
            "electric02.png"
            ]

    def __init__(self,x,y, w = 100,h = 30 ):
        super().__init__()
        self.image = pg.Surface((w,h), flags = pg.SRCALPHA , depth = 32)
        pg.draw.rect(self.image, (255,0,0), pg.Rect(0,0,w,h), border_radius=10)
        #self.image2 = pg.image.load("images/electric00.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x,y))
        self.vx = 10
        self.vy = 0

    def update(self):
        tecla_pul = pg.key.get_pressed()
        if tecla_pul[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.vx

        if tecla_pul[pg.K_RIGHT] and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += self.vx

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= ANCHO:
            self.rect.right = ANCHO


class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3

        self.cuentaGolpes = Marcador("POINTS", 10,10)
        self.bola = Bola(ANCHO//2, ALTO//2)
        self.raqueta = Raqueta(ANCHO // 2, ALTO - 2)

        self.todoGroup = pg.sprite.Group()
        self.todoGroup.add( self.bola,
                            self.raqueta, 
                            self.cuentaGolpes)

    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()
        contador_milisegundos = 0
        segundero = 0

        #Bucle principal
        while not game_over:
            dt = reloj.tick(FPS)
            contador_milisegundos += dt

            #Utilizo este código para convertir milisegundos en segundos
            if contador_milisegundos >= 1000:
                segundero +=1
                contador_milisegundos = 0

            #Gestiono eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True

            #Modifico estado
            self.cuentaGolpes.text = segundero
            self.todoGroup.update()

            #Refresco pantalla
            self.pantalla.fill((10,10,20))
            self.todoGroup.draw(self.pantalla)

            pg.display.flip()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.bucle_principal()
