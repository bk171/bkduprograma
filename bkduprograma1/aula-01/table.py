import pygame
import random

pygame.init()
tela=pygame.display.set_mode((600, 400))
religion=pygame.time.Clock()
jogador=pygame.Rect(270, 350, 60, 20)
blocos=[]
pontos=0
fonte= pygame.font.Font(None, 40)
rodando=True
while rodando:
    for event in game.event.get():
        if event.type==pygame.QUIT:
            rodando=False


            teclas=pygame.key.get_pressed()