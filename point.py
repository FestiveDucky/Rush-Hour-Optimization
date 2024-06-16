from constants import *


class Point(pygame.sprite.Sprite):
    def __init__(self, coords, group):
        super().__init__(group)
        self.coords = coords
        self.selected = False
        self.size = (HEIGHT / 36)
        self.color = WHITE
        self.rect = pygame.Rect(self.coords[0] - self.size / 2, self.coords[1] - self.size / 2, self.size, self.size)

    def update(self):
        # Draws a circle at the points location
        pygame.draw.circle(display, self.color, self.coords, LINE_THICKNESS * 2)

    def setCoords(self, coords):
        self.coords = coords
        self.rect = pygame.Rect(self.coords[0] - 10, self.coords[1] - 10, 20, 20)

    def setColor(self, color):
        self.color = color

    def getCoords(self):
        return self.coords