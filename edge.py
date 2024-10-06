from constants import *
from textbox import TextBox


class Edge(pygame.sprite.Sprite):
    def __init__(self, group, p1, p2, textbox_group):
        super().__init__(group)
        self.p1 = p1
        self.p2 = p2
        self.weight = random.randint(10, 100)
        mid_point = pointOnLine(self.p1.getCoords(), self.p2.getCoords(), 0.5)
        self.textbox = TextBox(textbox_group, str(self.weight), mid_point, HEIGHT / 8)

    def update(self):
        # Draw line
        drawThickLine(GREY, self.p1.getCoords(), self.p2.getCoords())

        # Move the textbox
        mid_point = pointOnLine(self.p1.getCoords(), self.p2.getCoords(), 0.5)
        self.textbox.setCenter(mid_point)
        self.textbox.update()

        self.weight = float(self.textbox.getTypedValues())

    def getTextBox(self):
        return self.textbox
