from arkanoid import ANCHO, ALTO, FPS, TOP_BAR
import pygame as pg
from arkanoid.escenes import Game, Portada


pg.init()

class Arkanoid():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.escenas = [Portada(self.pantalla),
                        Game(self.pantalla)]
        self.escena_activa = 0

    def start(self):
        while True:
            la_escena = self.escenas[self.escena_activa]
            la_escena.reset()
            la_escena.bucle_principal()
            
            """
            self.escena_activa +=1
            if self.escena_activa >= len(self.escenas):
                self.escena_activa = 0
        
            El método de abajo sustituye a este bucle de ifs. vale sea cual sea la longitud de la lista.       
            """
            self.escena_activa = (self.escena_activa + 1) % len(self.escenas)