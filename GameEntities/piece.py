from pygame import image, transform, sprite
from os.path import abspath, dirname

ASSETS_PATH = f"{abspath(dirname(dirname(__file__)))}\\PiecesImages"

class Piece(sprite.Sprite):
    def __init__(self, piece_type, color):
        sprite.Sprite.__init__(self)
        self.type = piece_type
        self.color = color
        self.image = image.load(f"{ASSETS_PATH}\\{self.color}{self.type}.png").convert_alpha()
        self.image = transform.scale(self.image, (100, 100))
        # self.location = None

    def draw(self, screen, pos):
        screen.blit(self.image, pos)
        # self.location = square