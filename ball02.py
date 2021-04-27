import  pygame as pg
import sys

from random import randint

def rebotaX(x):
    if x <= 0 or x >=ANCHO:
        return -1
    return 1

def rebotaY(y):
    if y <= 0 or y >= ALTO:
        return -1
    return 1

ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
NEGRO = (0,0,0)

ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))

gameOver = False


# Bola 01
xB = ANCHO // 2
yB = ALTO // 2
xvB = -5
yvB = -5

# Bola 02

xB2 = randint(0, ANCHO)
yB2 = randint(0, ALTO)
xvB2 = randint(5, 15)
yvB2 = randint(5, 15)

reloj = pg.time.Clock()

class Bola():
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color


bolas = []
for _ in range(20):
    bola = Bola(randint(0, ANCHO),
                randint(0, ALTO),
                randint(5, 15),
                randint(5, 15),
                (randint(0, 255), randint(0, 255),randint(0, 255)))
    bolas.append(bola)

while not gameOver:

    reloj.tick(60)
    #Gestión de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameOver = True

    #Modificación de estado
    for bola in bolas:
        bola.x += bola.vx
        bola.y += bola.vy

        bola.vx *= rebotaX(bola.x)
        bola.vy *= rebotaY(bola.y)

    pantalla.fill(NEGRO)
    for bola in bolas:
        pg.draw.circle(pantalla, bola.color , (bola.x,bola.y), 10)

    """
        #Movimiento bola 1
    
    xB += xvB
    yB += yvB
    xB2 += xvB2
    yB2 += yvB2

    xvB *= rebotaX(xB)
    yvB *= rebotaY(yB)

    xvB2 *= rebotaX(xB2)
    yvB2 *= rebotaY(yB2)

    pg.draw.circle(pantalla,ROJO , (xB,yB),10)
    pg.draw.circle(pantalla,AZUL , (xB2,yB2),10)
    """

    #Refrescar pantalla

    pg.display.flip()

pg.quit()
sys.exit()