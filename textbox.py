from constants import *


class TextBox(pygame.sprite.Sprite):
    def __init__(self, group, text, pos, size):
        super().__init__(group)
        self.size = (size / 20) * 3
        self.font = pygame.font.Font('freesansbold.ttf', int(16 * (size / 200)))
        self.pos = pos

        self.rect = pygame.Rect(pos[0], pos[1], self.size * 1.3, self.size)
        self.rect.topleft = (pos[0] + self.size / 6, pos[1] + self.size / 6)

        # Stores the rendered text
        self.text = None
        self.selected = False
        self.updateText(text)
        # Default text that is shown when nothing is typed
        self.defaultText = text
        # The text that is typed by the user
        self.typedText = text

    def updateText(self, text):
        # Automatically resize the text box based on text size
        self.rect.width = self.size * (1.3 + 0.3 * (len(text) - 2))
        self.text = self.font.render(text, True, (240, 240, 240) if self.selected else LIGHT_BLUE)

    def update(self):
        pygame.draw.rect(display, (46, 80, 102) if self.selected else (23, 40, 52), self.rect, int(self.size/20))
        display.blit(self.text, (self.pos[0] + self.size / 2, self.pos[1] + self.size / 2.55))

        # color = (10, 10, 10)
        # if self.enabled:
        #     color = (10, 100, 80)
        #
        # pygame.draw.rect(self.display, color, pygame.Rect(self.pos[0] + self.size/6, self.pos[1] + self.size/6, self.size*2/3, self.size*2/3))

    def typing(self, numbersOnly=False):
        self.typedText = ""
        self.selected = True
        while self.selected:
            ev = pygame.event.get()
            for e in ev:
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if not self.checkCollision(e.pos):
                        self.selected = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                        self.selected = False
                    elif e.key == pygame.K_BACKSPACE:
                        self.typedText = self.typedText[:-1]
                    else:
                        if numbersOnly and e.unicode in [".", " ", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8",
                                                         "9"] and len(self.typedText) < 14:
                            self.typedText += e.unicode
                        elif not numbersOnly:
                            self.typedText += e.unicode

            # Right before loop exits check if we need to change text
            if not self.selected and self.typedText == "":
                self.typedText = self.defaultText
            display.fill(MENU_BACKGROUND_COLOR, self.rect)
            self.updateText(self.typedText)
            self.update()
            pygame.display.update()

    def checkCollision(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def setTypedValues(self, text):
        self.updateText(text)
        self.typedText = text

    def getTypedValues(self):
        return self.typedText
