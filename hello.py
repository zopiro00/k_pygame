import pygame as pg
import sys
import random


class Ball():

    def __init__(self,surface,pos = (0,0),size = 10):
        self.center = pos
        self.size = size
        self.color = (0,0,0)
        self.surface = surface

    def display(self): 
        pg.draw.circle(self.surface, self.color, self.center, self.size)

class Game():

    __width = 600
    __height = 400

    def __init__(self):
        self.__pantalla = pg.display.set_mode((self.__width,self.__height))
        pg.display.set_caption("Hola")
        self.__pantalla.fill((0,255,0))
        self.b = Ball(self.__pantalla)
        self.b.center = [self.__width/2,self.__height/2]

    def start(self):
        gameOver = False
        mx = -10
        my = -10
        reloj = pg.time.Clock()

        while not gameOver:
            #Gestión de eventos
            reloj.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameOver = True
            #Gestión del estado0
            self.b.center[0] += mx
            self.b.center[1] += my

            if self.b.center[0] >= self.__width or self.b.center[0] <= 0:
                mx = -mx
            if self.b.center[1] >= self.__height or self.b.center[1] <= 0:
                my = -my

            #Refrescar / Renderizar
            self.__pantalla.fill((255,255,255))
            self.b.display()
        

            pg.display.flip()

        pg.quit()
        sys.exit()


# Iniciar juego
pg.init()
game = Game()
game.start()