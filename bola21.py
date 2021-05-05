import pygame as pg
import sys
import random

ALTO =  600
ANCHO = 800

class Marcador():
    def __init__(self, x, y, fontsize = 25, color = (255,255,255)):
        self.fuente = pg.font.SysFont("Fox Cavalier", fontsize)
        self.x = x
        self.y = y
        self.color = color

    def dibuja(self, text, lienzo):
        image = self.fuente.render(str(text), True, self.color)
        lienzo.blit(image, (self.x, self.y))


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
    def __init__(self):
        super().__init__()
        self.altura = 20
        self.anchura = 100
        self.color = (255,255,255)
        self.x = (ANCHO - self.anchura) // 2
        self.y = ALTO - (self.altura + 5)
        self.vx = 10
        self.vy = 0

    def dibujar(self,pantalla):
        rect = pg.Rect(self.x, self.y, self.anchura, self.altura)
        pg.draw.rect(pantalla, self.color, rect, border_radius = 2)

    def actualizar(self):
        tecla_pul = pg.key.get_pressed()
        if tecla_pul[pg.K_LEFT] and self.x > 0:
            self.x -= self.vx

        if tecla_pul[pg.K_RIGHT] and self.x < ANCHO - self.anchura:
            self.x += self.vx


class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.cuentaGolpes = Marcador(10,10)

        self.ballGroup = pg.sprite.Group()
        for i in range(random.randint(1, 20)):
            bola = Bola(random.randint(0, ANCHO), random.randint(0, ALTO))
            self.ballGroup.add(bola)

        self.bola = Bola(ANCHO//2, ALTO//2)
        self.raqueta = Raqueta()

    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()

        #Bucle principal
        while not game_over:
            reloj.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True
            
            self.ballGroup.update()
            
            self.raqueta.dibujar(self.pantalla)
            self.pantalla.fill((0,0,0))
            self.cuentaGolpes.dibuja("POINTS: ", self.pantalla)
            self.ballGroup.draw(self.pantalla)

            pg.display.flip()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.bucle_principal()
    bola = Bola()
