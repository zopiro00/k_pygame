import pygame as pg

pg.init()
pantalla = pg.display.set_mode((600,400))
pg.display.set_caption("Hola")

gameOver = False

while not gameOver:
    #Gestión de eventos
    for evento in pg.event.get():
        pass

    #Gestión del estado
    print("Hola Mundo")
    #Refrescar / Renderizar

    pantalla.fill((0,255,0))

    pg.display.flip()