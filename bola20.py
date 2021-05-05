import pygame as pg
import sys
import random

ALTO =  600
ANCHO = 800


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

class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.botes = 0

        self.ballGroup = pg.sprite.Group()
        for i in range(random.randint(1, 20)):
            bola = Bola(random.randint(0, ANCHO), random.randint(0, ALTO))
            self.ballGroup.add(bola)

        self.bola = Bola(ANCHO//2, ALTO//2)

    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()

        #Bucle principal
        while not game_over:
            reloj.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True
            
            self.bola.update()

            self.pantalla.fill((0,0,0))
            self.pantalla.blit(self.bola.image, self.bola.rect.topleft)

            pg.display.flip()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.bucle_principal()
    bola = Bola()
