import pygame
import src.locales as locales


pygame.init()
pygame.display.set_mode((100, 100))
pygame.display.set_caption(f"{locales.get('info_welcome')}")
