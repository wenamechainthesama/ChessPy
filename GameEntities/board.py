from GameEntities.piece import Piece
from GameEntities.square import Square
from GameEntities.enums import PieceType, PieceColor

ROWS_AMOUNT = 8
WHITE = (204, 166, 133)
BLACK = (145, 118, 89)

def get_square_index_by_coords(pos):
    return pos[1] // 100 * ROWS_AMOUNT + pos[0] // 100

class Board:
    def __init__(self):
        """
        FEN is a standard notation for describing a particular board position of a chess game
        More: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        """
        self.initial_position_fen = "RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr w KQkq - 0 1"
        self.squares = []
        self.piece_mark_accordance = {
            "r": PieceType.rook,
            "n": PieceType.knight,
            "b": PieceType.bishop,
            "q": PieceType.queen,
            "k": PieceType.king,
            "p": PieceType.pawn,
        }

        self.initialize_squares()

    def initialize_squares(self):
        for row in range(ROWS_AMOUNT):
            for column in range(ROWS_AMOUNT):
                square_color = WHITE if (row + column) % 2 == 0 else BLACK
                self.squares.append(Square((column * 100, row * 100), square_color))

    def setup_initial_position(self, screen):
        self.initial_position_fen = self.initial_position_fen.replace("/", "")
        square_index = 0
        for index, letter in enumerate(self.initial_position_fen):
            if self.initial_position_fen[index] == ' ':
                break
            if letter.isdigit():
                square_index += int(letter)
                continue
            current_square = self.squares[square_index]
            piece_type = self.piece_mark_accordance[letter.lower()]
            piece_color = PieceColor.black if letter.isupper() else PieceColor.white
            piece = Piece(piece_type, piece_color)
            piece.draw(screen, current_square.center)
            current_square.occupying_piece = piece
            square_index += 1

    def choose_piece(self, screen, mouse_pos, init_square_index):
        square_index = init_square_index
        square = self.squares[square_index]
        if square.occupying_piece is not None:
            print("piece selected")
            """ Hold piece by cursor until dropped """
            piece = square.occupying_piece
            piece.draw(screen, (mouse_pos[0] - 50, mouse_pos[1] - 50))

    def draw(self, screen):
        """ At first draw squares """
        for square in self.squares:
            square.draw(screen)

        """ And only then pieces """
        self.setup_initial_position(screen)