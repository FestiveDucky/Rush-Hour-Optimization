from random import randint as ri
import pygame
import ctypes
from math import *
import pygame.gfxdraw


fullscreen = True

pygame.init()

PATH_FOR_FILE_EXPORT = fr"C:\Users\alexr\Documents\GitHub\ScienceResearchProject"

# Automatically resizes everything for you
ctypes.windll.user32.SetProcessDPIAware()



if fullscreen:
    WIDTH, HEIGHT = pygame.display.list_modes()[0]
    display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    WIDTH, HEIGHT = pygame.display.list_modes()[0]
    WIDTH //= 2
    HEIGHT //= 2
    display = pygame.display.set_mode((WIDTH, HEIGHT))

# Ticks per second
TPS = 100

colors = [(217, 15, 73), (182, 158, 60), (13, 192, 128)]

LINE_COLOR = (42, 150, 204)
REVERSED_LINE_COLOR = (255, 86, 92)
MENU_BACKGROUND_COLOR = (34, 45, 56)
LINE_THICKNESS = HEIGHT/720
ORANGE = (243, 170, 78)
DARK_BLUE = (17, 24, 32)
SEMI_DARK_BLUE = (47, 54, 62)
BLUE = (77, 84, 92)
WHITE = (255, 255, 255)

def events(nested=False):
    while True:
        ev = pygame.event.get()
        for e in ev:
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if not nested:
                        return events(True)
                    else:
                        return False
                elif e.key == pygame.K_c:
                    return True
        if not nested:
            return False


def pointOnLine(p1, p2, t):
    return (p2[0] - p1[0]) * t + p1[0], (p2[1] - p1[1]) * t + p1[1]



def drawThickLine(color, p1, p2):
    # Not my code, found on the internet to draw thicker lines
    center_L1 = pointOnLine(p1, p2, 0.5)
    length = dist(p1, p2)
    thickness = LINE_THICKNESS
    angle = atan2(p1[1] - p2[1], p1[0] - p2[0])
    UL = (center_L1[0] + (length / 2.) * cos(angle) - (thickness / 2.) * sin(angle),
          center_L1[1] + (thickness / 2.) * cos(angle) + (length / 2.) * sin(angle))
    UR = (center_L1[0] - (length / 2.) * cos(angle) - (thickness / 2.) * sin(angle),
          center_L1[1] + (thickness / 2.) * cos(angle) - (length / 2.) * sin(angle))
    BL = (center_L1[0] + (length / 2.) * cos(angle) + (thickness / 2.) * sin(angle),
          center_L1[1] - (thickness / 2.) * cos(angle) + (length / 2.) * sin(angle))
    BR = (center_L1[0] - (length / 2.) * cos(angle) + (thickness / 2.) * sin(angle),
          center_L1[1] - (thickness / 2.) * cos(angle) - (length / 2.) * sin(angle))

    pygame.gfxdraw.aapolygon(display, (UL, UR, BR, BL), color)
    pygame.gfxdraw.filled_polygon(display, (UL, UR, BR, BL), color)

