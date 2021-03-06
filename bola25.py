import pygame as pg
import sys
import random
from enum import Enum

ALTO =  600
ANCHO = 800

TOP_BAR = 35

FPS = 60

class Back_rect(pg.sprite.Sprite):
    def __init__(self, h, w, x = 0,y = 0, color = (0,0,0)):
        super().__init__()
        self.image = pg.Surface((w,h))
        self.rect = self.image.get_rect()
        self.image.fill(color)


class Marcador(pg.sprite.Sprite):
    plantilla = "{}"

    def __init__(self, text, x, y, justificar = "topleft", fontsize = 20, color = (255,255,255)):
        super().__init__()
        self.fuente = pg.font.SysFont("Fox Cavalier", fontsize)
        self.color = color
        self.text = text
        self.justificar = {justificar : (x,y)}
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color)
        self.rect = self.image.get_rect(**self.justificar)

    def update(self, dt):
        self.image = self.fuente.render(str(self.text), True, self.color)

class Ladrillo(pg.sprite.Sprite):
    disfraces = [   "greenTile.png",
                    "redTile.png",
                    "redTileBreak.png"]

    def __init__(self, x, y, esDuro = False):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.esDuro = esDuro
        self.imagen_actual = 1 if self.esDuro else 0
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft= (x,y))
        self.numGolpes = 0

    def cargaImagenes(self):

        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("images/{}".format(fichero)))
        return imagenes

    def update(self, dt):
        if self.esDuro and self.numGolpes == 1:
            self.imagen_actual = 2
            self.image = self.imagenes[self.imagen_actual]

    def desaparece(self):
        self.numGolpes += 1

        """
        if (self.numGolpes > 0 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro):
            return True
        else:
            return False

        Este if es sustituible por un return con la condici??n que queremos que se cumple.
        """
        return (self.numGolpes > 0 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro)

class Level(pg.sprite.Sprite):
    level1 = [  [1,1,1,1,1,1,1,1],
                [1,0,0,1,1,0,0,1],
                [1,0,0,1,1,0,0,1],
                [1,1,1,1,1,1,1,1]]

    level2 = [  [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]]

    level3 = [  [2,2,1,1,0,0,0,0],
                [1,2,2,1,1,0,0,0],
                [1,1,2,2,1,1,0,0],
                [1,1,1,2,2,1,1,0]]

    level_list = [level1, level2, level3]
                
    def __init__(self, level):
        super().__init__()
        self.choosen_level = self.level_list[level]

    def Create_level(self):
        grupo_ladrillos = pg.sprite.Group()
        for fila in range(4):
            for columna in range(8):
                xb = 5 + 100*columna
                yb = 5 + 40*fila
                if self.level[fila][columna] == 1:
                    ladrillo = Ladrillo(xb, yb + TOP_BAR, False)
                    grupo_ladrillos.add(ladrillo)
                elif self.level[fila][columna] == 1:
                    ladrillo = Ladrillo(xb, yb + TOP_BAR, True )
                    grupo_ladrillos.add(ladrillo)
        return grupo_ladrillos

    

class Bola(pg.sprite.Sprite):

    class Estado(Enum):
        viva = 0
        agonizando = 1
        muerta = 2

    fotos = ["ball1.png",
            "ball2.png",
            "ball3.png",
            "ball4.png",
            "ball5.png"]

    def __init__(self, x, y):
        #Activamos los m??todos de la clase "madre" Sprite
        #pg.sprite.Sprite.__init__(self) <-- la manera cl??sica
        super().__init__() # <-- la super manera
        
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.milisegundos_cambio = 1000 // FPS * 10
        self.milisegundos_acumulado = 0
        self.image = self.imagenes[self.imagen_actual]
        
        #self.image = pg.image.load("images/ball1.png").convert_alpha()

        self.rect = self.image.get_rect(center=(x,y))
        self.x = x
        self.y = y
        #self.estoyViva = True
        self.estado_vital = Bola.Estado.viva

        self.vx = random.randint(5,10) * random.choice([-1,1])
        self.vy = random.randint(5,10) * random.choice([-1,1])

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1
        return candidatos

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.fotos:
            imagenes.append(pg.image.load("images/{}".format(fichero)))
        return imagenes

    def update(self, dt):

        # Comportamiento de la bola en modo normal.
        
        if self.estado_vital == Bola.Estado.viva:
            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1
            if self.rect.top <= 0 + TOP_BAR or self.rect.bottom >= ALTO:
                self.vy *= -1

            if self.rect.bottom >= ALTO:
                self.estado_vital = Bola.Estado.agonizando
                self.rect.bottom = ALTO

        #Comportamiento de la bola si "muere" 
        elif self.estado_vital == Bola.Estado.agonizando:
            self.milisegundos_acumulado +=dt
            if self.milisegundos_acumulado >= self.milisegundos_cambio:
                self.imagen_actual +=1
                if self.imagen_actual >= len(self.imagenes):
                    self.imagen_actual = 0
                    self.estado_vital = Bola.Estado.muerta
                self.milisegundos_acumulado = 0
            self.image = self.imagenes[self.imagen_actual]

        elif self.estado_vital == Bola.Estado.muerta:
            self.rect.center = (self.x, self.y)
            self.vx = random.randint(5,10) * random.choice([-1,1])
            self.vy = random.randint(5,10) * random.choice([-1,1])
            self.estado_vital = Bola.Estado.viva

class Raqueta(pg.sprite.Sprite):
    fotos = ["electric00.png",
            "electric01.png",
            "electric02.png"]

    def __init__(self,x,y, w = 100,h = 30 ):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.milisegundos_cambio = 1000 // FPS * 5
        self.milisegundos_acumulado = 0
        self.image = self.imagenes[self.imagen_actual]

        self.rect = self.image.get_rect(midbottom=(x,y))
        self.vx = 10

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.fotos:
            imagenes.append(pg.image.load("images/{}".format(fichero)))
        return imagenes

    #Movimiento de la raqueta
    def update(self, dt):
        #Control de la raqueta por botones.
        tecla_pul = pg.key.get_pressed()
        if tecla_pul[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.vx

        if tecla_pul[pg.K_RIGHT] and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += self.vx

        #Evitar que la raqueta haga cosas raras en el borde.
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= ANCHO:
            self.rect.right = ANCHO
        
        # Animaci??n de raqueta.
        self.milisegundos_acumulado +=dt
        if self.milisegundos_acumulado >= self.milisegundos_cambio:
            self.imagen_actual +=1
            if self.imagen_actual >= len(self.imagenes):
                self.imagen_actual = 0
            self.milisegundos_acumulado = 0

        self.image = self.imagenes[self.imagen_actual]


class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.puntuacion = 0

        self.todoGroup = pg.sprite.Group()
        self.grupo_player = pg.sprite.Group()
        self.grupo_bricks = pg.sprite.Group()

        for fila in range(4):
            for columna in range(8):
                xb = 5 + 100*columna
                yb = 5 + 40*fila
                esDuro = random.randint(1, 10) == 1
                ladrillo = Ladrillo(xb, yb + TOP_BAR, esDuro )
                self.grupo_bricks.add(ladrillo)

        self.barra = Back_rect(35, ANCHO, color= (184,19,46))

        self.cuentaGolpes = Marcador("POINTS: {}".format(self.puntuacion), 10, 10)
        self.cuentaVidas = Marcador("VIDAS: {}".format(self.vidas), ANCHO-10, 10, justificar = "topright")
        self.title = Marcador("Arkanoid V2.0", ANCHO //  2, 10, justificar= "midtop")

        self.bola = Bola(ANCHO//2, ALTO//2)
        self.raqueta = Raqueta(ANCHO // 2, ALTO - 2)

        
        self.todoGroup.add( self.barra,
                            self.bola,
                            self.raqueta, 
                            self.cuentaGolpes,
                            self.cuentaVidas,
                            self.title)

        self.todoGroup.add(self.grupo_bricks)

        self.grupo_player.add(self.raqueta)


    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()
        contador_milisegundos = 0
        segundero = 0

        #Bucle principal
        while not game_over:
            dt = reloj.tick(FPS)
            contador_milisegundos += dt
            '''
            if not self.bola.estoyViva:
                pg.time.delay(500)
            '''
            #Utilizo este c??digo para convertir milisegundos en segundos
            if contador_milisegundos >= 1000:
                segundero +=1
                contador_milisegundos = 0

            #Gestiono eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True

            #Modifico estado
            
            self.cuentaVidas.text = "VIDAS: {}".format(self.vidas)
            self.bola.prueba_colision(self.grupo_player)
            tocados = self.bola.prueba_colision(self.grupo_bricks)
            for ladrillo in tocados:
                self.puntuacion += 5
                if ladrillo.desaparece():
                    self.grupo_bricks.remove(ladrillo)
                    self.todoGroup.remove(ladrillo)

            self.todoGroup.update(dt)

            if self.bola.estado_vital == self.bola.Estado.muerta:
                self.vidas -= 1
            
            #Refresco pantalla
            self.pantalla.fill((10,10,20))
            self.todoGroup.draw(self.pantalla)

            pg.display.flip()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.bucle_principal()
