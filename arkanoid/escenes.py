from arkanoid import ANCHO, ALTO, FPS, TOP_BAR
import pygame as pg
import sys
from arkanoid.entities import Marcador, Bola, Ladrillo, Raqueta, Back_rect, Level


class Escene():
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.todoGroup = pg.sprite.Group()
        self.reloj = pg.time.Clock()

    def maneja_eventos(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                self.grupo_bricks.empty()
                self.todoGroup.remove(self.grupo_bricks)
    def reset(self):
        pass
    def bucle_principal(self):
        pass
        """
        while True:
            self.maneja_eventos()
            self.todoGroup.update(dt)
            pg.display.flip()
        """
class Game(Escene):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.vidas = 3
        self.puntuacion = 0

        #Elementos
        self.bola = Bola(ANCHO//2, ALTO//2)
        self.raqueta = Raqueta(ANCHO // 2, ALTO - 2)

        self.level = Level()

        #Textos marcador
        self.barra = Back_rect(35, ANCHO, color= (184,19,46))
        self.cuentaGolpes = Marcador("POINTS: {}".format(self.puntuacion), 10, 10)
        self.cuentaVidas = Marcador("VIDAS: {}".format(self.vidas), ANCHO-10, 10, justificar = "topright")
        self.actual_level = Marcador("LEVEL: {}".format(self.level.level), 40 + self.cuentaVidas.rect.width, 10)
        self.title = Marcador("Arkanoid V2.0", ANCHO //  2, 10, justificar= "midtop")

        #grupos
        self.grupo_player = pg.sprite.Group()
        
        self.level.level = 0
        self.grupo_bricks = self.level.create_level(self.level.level)
        
        self.todoGroup.add( self.barra,
                            self.bola,
                            self.raqueta, 
                            self.cuentaGolpes,
                            self.cuentaVidas,
                            self.actual_level,
                            self.title)

        self.grupo_player.add(self.raqueta)

    
    def reset(self):
        self.vidas = 3
        self.puntuacion = 0
        self.level.level = 0
        self.todoGroup.remove(self.grupo_bricks)
        self.grupo_bricks.empty()
        self.grupo_bricks = self.level.create_level(self.level.level)
        self.todoGroup.add(self.grupo_bricks)

    def new_level(self):
        self.level.level += 1
        self.grupo_bricks = self.level.create_level(self.level.level)
        self.todoGroup.add(self.grupo_bricks)
        self.bola.x = ANCHO // 2
        self.bola.y = ALTO -60


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
            self.maneja_eventos()

            #Modifico estado
            self.cuentaVidas.text = "VIDAS: {}".format(self.vidas)
            self.bola.prueba_colision(self.grupo_player)
            tocados = self.bola.prueba_colision(self.grupo_bricks)
            for ladrillo in tocados:
                self.puntuacion += 5
                if ladrillo.desaparece():
                    self.grupo_bricks.remove(ladrillo)
                    self.todoGroup.remove(ladrillo)
                    if len(self.grupo_bricks) == 0:
                        self.new_level()

            self.todoGroup.update(dt)

            if self.bola.estado_vital == self.bola.Estado.muerta:
                self.vidas -= 1
            
            #Refresco pantalla
            self.pantalla.fill((10,10,20))
            self.todoGroup.draw(self.pantalla)

            pg.display.flip()
        if not game_over:
            #hare algo para saber que me he salido por el QUIT
            pass

class Portada(Escene):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.instrucciones = Marcador("INSTRUCCIONES", 100, 100)
        self.todoGroup = pg.sprite.Group()
        self.todoGroup.add(self.instrucciones)
        
    def reset(self):
        pass

    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            self.maneja_eventos()

            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_SPACE]:
                game_over = True

            self.todoGroup.update(dt)
            self.pantalla.fill((0,0,0))
            self.todoGroup.draw(self.pantalla)

            pg.display.flip()