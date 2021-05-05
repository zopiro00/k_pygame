import  pygame as pg
import sys

from random import randint, choice

ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
NEGRO = (0,0,0)

ANCHO = 800
ALTO = 600

BAR_SIZE = 25

pg.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))



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
        self.puntos = 0
    
    def muevete(self, ancho, alto):        
        self.x += self.vx
        self.y += self.vy

        if (self.y - self.radio) <= 0 + BAR_SIZE:
            self.vy *= -1
            self.puntos +=1

        if (self.x - self.radio) <= 0 or (self.x + self.radio) >= ancho:
            self.vx *= -1
            self.puntos += 1

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

class Triangulo():
    def __init__(self, origen):
            self.origen = origen
            self.vertices = [self.origen,[self.origen[0] -12, self.origen[1] +8],[self.origen[0] -12, self.origen[1] -8]]
            self.color = (255,255,255)
            print(self.origen)
    
    def dibujar(self,pantalla):
        pg.draw.polygon(pantalla, self.color, self.vertices)

    def actualizar(self):
        #tecla_pul = pg.key.get_pressed()
        if pg.K_DOWN:
            self.origen[1] += 40
            self.vertices = [self.origen,[self.origen[0] -12, self.origen[1] +8],[self.origen[0] -12, self.origen[1] -8]]

        if pg.K_UP:
            self.origen[1] -= 40
            self.vertices = [self.origen,[self.origen[0] -12, self.origen[1] +8],[self.origen[0] -12, self.origen[1] -8]]

class Barra():

    def __init__(self):
        self.__font = pg.font.SysFont("Fox Cavalier", 20)
        self.size = pg.Rect(0, 0, ANCHO, BAR_SIZE)
        self.title = self.__font.render("ARKANOID V 1.0", True, (0,0,0))
        self.rectTitle = self.title.get_rect()
        

    def render(self, value, puntos):
            #Definición texto vidas
        self.strValue = "VIDAS: {}".format(value)
        self.textBlock = self.__font.render(self.strValue, True, (0,0,0))
            #Definición marcador puntos
        self.strPuntos = "PUNTOS: {}".format(puntos)
        self.textPuntos = self.__font.render(self.strPuntos, True, (0,0,0))
        self.rectPuntos = self.textPuntos.get_rect()
            #Renderizado marcador
        pg.draw.rect(pantalla, (255,255,255), self.size)
        pantalla.blit(self.textBlock, (2,2))
        pantalla.blit(self.textPuntos, (ANCHO-(self.rectPuntos[2] + 2),2))
        pantalla.blit(self.title, (ANCHO // 2 -(self.rectTitle[2] // 2),2))

class Text():
    def __init__(self, text, size):
        self.font = pg.font.SysFont("Fox Cavalier", size)
        self.text = self.font.render(text, True, (255,255,255))
        self.rect = self.text.get_rect()
        self.centroX = self.rect[2] // 2
        self.centroY = self.rect[3] // 2

class Game_menu():
    def __init__(self):
        self.title = Text("GAME OVER", 30)
        self.retry = Text("RETRY?", 20)
        self.end = Text("END", 20)
        self.centroGY = ALTO // 2 - self.retry.centroY // 2
        self.sel = Triangulo([ANCHO // 2 - 60, self.centroGY + 10])

    def finjuego(self):
        pantalla.blit(self.title.text, (ANCHO // 2 - self.title.centroX, self.centroGY - 40))
        pantalla.blit(self.retry.text , (ANCHO // 2 - self.retry.centroX, self.centroGY))
        pantalla.blit(self.end.text , (ANCHO // 2 - self.end.centroX, self.centroGY + 25))
        self.sel.dibujar(pantalla)
        #print (self.centroGY)
        #print(self.centroGY + 10)
    
    def act_sel(self):
        self.sel.actualizar()

#Programa principal
vidas = 3
game_time = 0
pierdebola = False
gameOver = False

bola = Bola(randint(40, ANCHO),
            randint(0, ALTO),
            randint(7, 7) * choice([-1,1]),
            randint(7, 7) * choice([-1,1]),
            (randint(0, 255), randint(0, 255),randint(0, 255)),
            10)


raqueta = Raqueta()
barra = Barra()
gameM = Game_menu()


while not gameOver:

    reloj.tick(60)
    if pierdebola:
        pg.time.delay(500)
    #Gestión de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameOver = True
        
    #Modificación de estado
    gameM.act_sel()
    raqueta.actualizar()
    pierdebola = bola.muevete(ANCHO,ALTO)
    
    if pierdebola:
        vidas -= 1
        if vidas == 0:
            gameM.finjuego()
            game_time += 1
        else:
            bola.x = ANCHO // 2
            bola.y = ALTO // 2
            bola.dibujar(pantalla)
            raqueta.dibujar(pantalla)
    else:
        bola.comprueba_colision(raqueta)
    
    #Refrescar pantalla

    if game_time == 0:
        pantalla.fill(NEGRO)
        barra.render(vidas,bola.puntos)
        bola.dibujar(pantalla)
        raqueta.dibujar(pantalla)
 
        
    pg.display.flip()

pg.time.delay(1000)

pg.quit()
sys.exit()