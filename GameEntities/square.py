from pygame import Surface

class Square:
    def __init__(self, pos, color):
        self.center = pos
        self.color = color
        self.image = Surface((100, 100))
        self.image.fill(self.color)
        self.occupying_piece = None

    def draw(self, screen):
        screen.blit(self.image, self.center)