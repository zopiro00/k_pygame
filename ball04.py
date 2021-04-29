import  pygame as pg
import sys

from random import randint, choice

ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
NEGRO = (0,0,0)

ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))

gameOver = False

reloj = pg.time.Clock()

class Bola():
    def __init__(self, x, y, vx, vy, color, radio):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radio = radio
    
    def muevete(self, ancho, alto):        
        self.x += self.vx
        self.y += self.vy

        if (self.y - self.radio) <= 0 or (self.y + self.radio) >= alto:
            self.vy *= -1
            """
            if self.color != NEGRO:
                self.color = NEGRO
            else:
                self.color = (randint(0, 255), randint(0, 255),randint(0, 255))
            """
        if (self.x - self.radio) <= 0 or (self.x + self.radio) >= ancho:
            self.vx *= -1

    def dibujar(self,pantalla):
        pg.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)

bolas = []
for _ in range(10):
    bola = Bola(randint(0, ANCHO),
                randint(0, ALTO),
                randint(5, 15) * choice([-1,1]),
                randint(5, 15) * choice([-1,1]),
                (randint(0, 255), randint(0, 255),randint(0, 255)),
                randint(5, 15))
    bolas.append(bola)

while not gameOver:

    reloj.tick(60)
    #Gestión de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameOver = True

    #Modificación de estado
    for bola in bolas:
        bola.muevete(ANCHO,ALTO)

    pantalla.fill(NEGRO)
    for bola in bolas:
        bola.dibujar(pantalla)

    #Refrescar pantalla

    pg.display.flip()

pg.quit()
sys.exit()