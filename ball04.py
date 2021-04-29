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
        self.anchura = radio*2
        self.altura = radio*2
    
    def muevete(self, ancho, alto):        
        self.x += self.vx
        self.y += self.vy

        if (self.y - self.radio) <= 0:
            self.vy *= -1

        if (self.x - self.radio) <= 0 or (self.x + self.radio) >= ancho:
            self.vx *= -1

        if (self.y + self.radio) >= alto:
            self.y = ALTO  // 2
            self.x = ANCHO // 2
            self.vx = randint(5, 15) * choice([-1,1])
            self.vy = randint(5, 15) * choice([-1,1])
            return True
        return False

    def dibujar(self,pantalla):
        pg.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)

    def comprueba_colision(self,objeto):

        choqueX = self.x >= objeto.x and self.x <= objeto.x + objeto.anchura or \
            self.x + self.anchura >= objeto.x and self.x + self.anchura <= objeto.x + objeto.anchura
        choqueY = self.y >= objeto.y and self.y <= objeto.y + objeto.altura or \
            self.y + self.altura >= objeto.y and self.y + self.altura <= objeto.y + objeto.altura

        if choqueX and choqueY:
            self.vy *= -1

class Raqueta():
    def __init__(self):
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

vidas = 3
bola = Bola(randint(0, ANCHO),
            randint(0, ALTO),
            randint(5, 15) * choice([-1,1]),
            randint(5, 15) * choice([-1,1]),
            (randint(0, 255), randint(0, 255),randint(0, 255)),
            10)

raqueta = Raqueta()
    

while not gameOver and vidas > 0:

    reloj.tick(60)
    #Gestión de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameOver = True
        
    #Modificación de estado
    raqueta.actualizar()
    pierdebola = bola.muevete(ANCHO,ALTO)
    if pierdebola:
        vidas -= 1
        print(vidas)
    bola.comprueba_colision(raqueta)

    #Refrescar pantalla
    pantalla.fill(NEGRO)
    bola.dibujar(pantalla)
    raqueta.dibujar(pantalla)

    pg.display.flip()
    if pierdebola:
        pg.time.delay(500)

pg.quit()
sys.exit()