# Helper enums for self-explanatory code
class PieceType:
    king = 1
    queen = 2
    bishop = 3
    knight = 4
    rook = 5
    pawn = 6


class PieceColor:
    white = 0
    black = 1


class GameState:
    playing = 0
    white_won = 1
    black_won = 2
    draw = 3
