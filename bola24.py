import pygame as pg
import sys
import random

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
    def __init__(self, text, x, y, fontsize = 20, color = (255,255,255)):
        super().__init__()
        self.fuente = pg.font.SysFont("Fox Cavalier", fontsize)
        self.color = color
        self.text = text
        self.image = self.fuente.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, dt):
        self.image = self.fuente.render(str(self.text), True, self.color)

class Bola(pg.sprite.Sprite):

    ciclo_vital = ["vivo", "muerto", "limbo", "resucito"]
    
    fotos = ["ball1.png",
            "ball2.png",
            "ball3.png",
            "ball4.png",
            "ball5.png"]

    def __init__(self, x, y):
        #Activamos los métodos de la clase "madre" Sprite
        #pg.sprite.Sprite.__init__(self) <-- la manera clásica
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
        self.estado_vital = 0

        self.vx = random.randint(5,10) * random.choice([-1,1])
        self.vy = random.randint(5,10) * random.choice([-1,1])

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.fotos:
            imagenes.append(pg.image.load("images/{}".format(fichero)))
        return imagenes

    def update(self, dt):

        # Comportamiento de la bola en modo normal.
        
        if self.estado_vital == 0:
            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1
            if self.rect.top <= 0 + TOP_BAR or self.rect.bottom >= ALTO:
                self.vy *= -1

            if self.rect.bottom >= ALTO:
                self.estado_vital = 1

        #Comportamiento de la bola si "muere" 
        elif self.estado_vital == 1:
            self.milisegundos_acumulado +=dt
            if self.milisegundos_acumulado >= self.milisegundos_cambio:
                self.imagen_actual +=1
                if self.imagen_actual >= len(self.imagenes):
                    self.imagen_actual = 0
                    self.estado_vital = 2
                self.milisegundos_acumulado = 0
            self.image = self.imagenes[self.imagen_actual]

        elif self.estado_vital == 2:
            self.rect.center = (self.x, self.y)
            self.vx = random.randint(5,10) * random.choice([-1,1])
            self.vy = random.randint(5,10) * random.choice([-1,1])
            self.estado_vital = 0

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
        
        # Animación de raqueta.
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

        self.todoGroup = pg.sprite.Group()
        self.grupo_player = pg.sprite.Group()
        self.grupo_bricks = pg.sprite.Group()

        self.barra = Back_rect(35, ANCHO, color= (184,19,46))

        self.cuentaGolpes = Marcador("POINTS", 10, 10)
        self.cuentaVidas = Marcador("VIDAS: {}".format(self.vidas), 200, 10)
        self.cuentaVidas.rect.topright = (ANCHO -10,10)
        self.title = Marcador("Arkanoid V2.0", 10, 10)
        self.title.rect.midtop = (ANCHO //  2, 10)

        self.bola = Bola(ANCHO//2, ALTO//2)
        self.raqueta = Raqueta(ANCHO // 2, ALTO - 2)

        
        self.todoGroup.add( self.barra,
                            self.bola,
                            self.raqueta, 
                            self.cuentaGolpes,
                            self.cuentaVidas,
                            self.title)

        
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
            #Utilizo este código para convertir milisegundos en segundos
            if contador_milisegundos >= 1000:
                segundero +=1
                contador_milisegundos = 0

            #Gestiono eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True

            #Modifico estado
            self.bola.prueba_colision(self.grupo_player)
            self.cuentaGolpes.text = segundero
            self.todoGroup.update(dt)

            if self.bola.estado_vital == 2:
                self.vidas -= 1
                self.cuentaVidas.text = "VIDAS: {}".format(self.vidas)
            
            #Refresco pantalla
            self.pantalla.fill((10,10,20))
            self.todoGroup.draw(self.pantalla)

            pg.display.flip()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.bucle_principal()
