class Move:
    def __init__(
        self,
        init_square_index,
        target_square_index,
        piece_moved,
        piece_captured,
        is_pawn_promotion=False,
        is_castling=False,
        is_en_passant=False,
    ):
        self.init_square_index = init_square_index
        self.target_square_index = target_square_index
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.is_pawn_promotion = is_pawn_promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
