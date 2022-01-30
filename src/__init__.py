import os
import pygame
import src.locales as locales

pygame.init()
# center top window
desktop_sizes = pygame.display.get_desktop_sizes()
# >>> JUST FOR DEVELOPING
if len(desktop_sizes) == 2:
    desktop_w = desktop_sizes[1][0]
    desktop_h = desktop_sizes[1][1]
else:
    desktop_w = desktop_sizes[0][0]
    desktop_h = desktop_sizes[0][1]
# <<<
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((desktop_w - 1000) // 2, 0)
# init display
pygame.display.set_mode((1000, 800))
pygame.display.set_caption(f"{locales.get('info_welcome')}")
