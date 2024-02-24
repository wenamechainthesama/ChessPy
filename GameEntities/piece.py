from pygame import image, transform, sprite, Surface
from os.path import abspath, dirname
from GameEntities.game_manager import GameManager

ASSETS_PATH = f"{abspath(dirname(dirname(__file__)))}\\PiecesImages"


class Piece(sprite.Sprite):
    def __init__(self, piece_type, color):
        sprite.Sprite.__init__(self)
        self.type = piece_type
        self.color = color
        self.image = image.load(
            f"{ASSETS_PATH}\\{self.color}{self.type}.png"
        ).convert_alpha()
        self.image = transform.scale(self.image, (100, 100))
        self.chosen = False

    @staticmethod
    def promote_pawn(screen, target_square):
        filenames = (
            ["02", "05", "03", "04"]
            if not GameManager.is_white_move
            else ["14", "13", "15", "12"]
        )
        box = Surface((100, 400))
        box.fill((219, 80, 15))
        box_y = target_square.center[1]
        if GameManager.is_white_move:
            box_y -= 300
        screen.blit(box, (target_square.center[0], box_y))
        for filename, offset in zip(filenames, [0, 100, 200, 300]):
            screen.blit(
                transform.scale(
                    image.load(f"{ASSETS_PATH}\\{filename}.png").convert_alpha(),
                    (100, 100),
                ),
                (target_square.center[0], box_y + offset),
            )

    def draw(self, screen, pos):
        screen.blit(self.image, pos)
