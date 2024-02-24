from GameEntities.enums import PieceColor


class GameManager:
    moves_history = []
    is_white_move = True
    is_piece_being_held = False
    is_pawn_promoting = False
    # is_castle_for_white_king_side_avaible = True
    # is_castle_for_white_queen_side_avaible = True
    # is_castle_for_black_king_side_avaible = True
    # is_castle_for_black_queen_side_avaible = True

    @classmethod
    def is_right_color(cls, piece_color):
        return (piece_color == PieceColor.white and cls.is_white_move) or (
            piece_color == PieceColor.black and not cls.is_white_move
        )

    @classmethod
    def move_made(cls, init_square_index, target_square_index):
        cls.is_white_move = not cls.is_white_move
        cls.moves_history.append([init_square_index, target_square_index])
