from pygame import Surface


class Square:
    def __init__(self, pos, color):
        self.center = pos
        self.color = color
        self.image = Surface((100, 100))
        self.occupying_piece = None

    def get_piece_color(self):
        return self.occupying_piece.color

    def get_piece_type(self):
        return self.occupying_piece.type

    def draw(self, screen):
        self.image.fill(self.color)
        screen.blit(self.image, self.center)
