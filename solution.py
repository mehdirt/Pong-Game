from decouple import config
import pygame

WIDTH = config('WIDTH')
HEIGHT = config('HEIGHT')

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
