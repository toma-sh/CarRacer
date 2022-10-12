import pygame
import time
import math

from utils import scale_img

GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)

TRACK = scale_img(pygame.image.load("imgs/track.png"),0.9)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.9)

FINISH = pygame.image.load("imgs/finish.png")

RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"),0.55)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"),0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Racing Game!")

FPS = 60

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(FPS)

    WIN.blit(GRASS, (0,0))
    WIN.blit(TRACK, (0,0))
    WIN.blit(RED_CAR, (0,0))

    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            break

pygame.quit()