from GameEntities.enums import PieceType

ROWS_AMOUNT = 8
num_squares_to_edge = [[]] * ROWS_AMOUNT ** 2

def calculate_sliding_moves(init_square_index, squares):
    """ 
    Generate moves for bishop, rook and queen
    at the same time as they are similar to each other
    """
    offsets = [-8, 8, 1, -1, -7, 7, -9, 9]

    start_square = squares[init_square_index]
    moving_piece_color = start_square.occupying_piece.color
    moving_piece_type = start_square.occupying_piece.type

    start_index = 4 if moving_piece_type == PieceType.bishop else 0
    end_index = 4 if moving_piece_type == PieceType.rook else 8

    avaible_squares = []
    for offset_index in range(start_index, end_index):
        for n in range(1, num_squares_to_edge[init_square_index][offset_index] + 1):
            target_square_index = init_square_index + offsets[offset_index] * n
            piece_on_target_square = squares[target_square_index].occupying_piece
            if piece_on_target_square is not None and piece_on_target_square.color == moving_piece_color:
                break

            avaible_squares.append(target_square_index)

            if piece_on_target_square is not None and piece_on_target_square.color != moving_piece_color:
                break

    return avaible_squares

def calculate_knight_moves(init_square_index, squares):
    offsets = [-17, -15, -10, -6, 6, 10, 15, +17]
    avaible_moves = []
    new_index = None
    for offset in offsets:
        new_index = init_square_index + offset
        if new_index < 64 and new_index > 0:
            other_piece = squares[new_index].occupying_piece
            if other_piece is not None and other_piece.color == squares[init_square_index].occupying_piece.color:
                    continue
            avaible_moves.append(new_index)
            
    return avaible_moves

def calculate_pawn_moves(init_square_index, squares):
    return []

def calculate_king_moves(init_square_index, squares):
    offsets = [-1, 7, -9, -8, 8, 1, -7, 9]
    if init_square_index % 8 == 0:
        offsets = offsets[3:]
    elif (init_square_index + 1) % 8 == 0:
        offsets = offsets[:(len(offsets) - 3)]
    avaible_moves = []
    new_index = None
    for offset in offsets:
        new_index = init_square_index + offset
        if new_index < 64 and new_index > 0:
            other_piece = squares[new_index].occupying_piece
            if other_piece is not None and other_piece.color == squares[init_square_index].occupying_piece.color:
                    continue
            avaible_moves.append(new_index)

    return avaible_moves


def save_precomputed_move_data():
    for row in range(ROWS_AMOUNT):
        for column in range(ROWS_AMOUNT):
            numUp = row
            numDown = ROWS_AMOUNT - 1 - row
            numLeft = ROWS_AMOUNT - 1 - column
            numRight = column

            square_index = row * ROWS_AMOUNT + column
            num_squares_to_edge[square_index] = [
                numUp,
                numDown,
                numLeft,
                numRight,
                min(numUp, numLeft),
                min(numDown, numRight),
                min(numUp, numRight),
                min(numDown, numLeft),
            ]