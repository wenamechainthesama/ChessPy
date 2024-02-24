from enums import PieceType, PieceColor
from game_manager import GameManager
from constants import *

num_squares_to_edge = [[]] * ROWS_AMOUNT**2


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

    avaible_moves = []
    for offset_index in range(start_index, end_index):
        for n in range(1, num_squares_to_edge[init_square_index][offset_index] + 1):
            target_square_index = init_square_index + offsets[offset_index] * n
            piece_on_target_square = squares[target_square_index].occupying_piece
            if (
                piece_on_target_square is not None
                and piece_on_target_square.color == moving_piece_color
            ):
                break

            avaible_moves.append(target_square_index)

            if (
                piece_on_target_square is not None
                and piece_on_target_square.color != moving_piece_color
            ):
                break

    return avaible_moves


def calculate_knight_moves(init_square_index, squares):
    offsets = [-17, -15, -10, -6, 6, 10, 15, +17]
    avaible_moves = []
    new_index = None
    current_row = init_square_index // ROWS_AMOUNT
    current_column = init_square_index % ROWS_AMOUNT
    for offset in offsets:
        new_index = init_square_index + offset
        new_index_row = new_index // ROWS_AMOUNT
        new_index_column = new_index % ROWS_AMOUNT
        if (
            new_index < 64
            and new_index >= 0
            and (
                abs(new_index_column - current_column)
                + abs(new_index_row - current_row)
            )
            == 3
        ):
            other_piece = squares[new_index].occupying_piece
            if (
                other_piece is not None
                and other_piece.color
                == squares[init_square_index].occupying_piece.color
            ):
                continue
            avaible_moves.append(new_index)

    return avaible_moves


def calculate_pawn_moves(init_square_index, squares):
    avaible_moves = []
    en_passant_square_index = None

    piece = squares[init_square_index].occupying_piece
    isPawnWhite = piece.color == PieceColor.white
    initial_row = 6 if isPawnWhite else 1
    current_row = init_square_index // ROWS_AMOUNT
    current_column = init_square_index % ROWS_AMOUNT

    move_offset = -8 if isPawnWhite else 8
    new_move_square_index = init_square_index + move_offset
    if (
        new_move_square_index >= 0
        and new_move_square_index < 64
        and squares[new_move_square_index].occupying_piece is None
    ):
        new_double_move_square_index = init_square_index + 2 * move_offset
        if (
            current_row == initial_row
            and squares[new_double_move_square_index].occupying_piece is None
        ):
            avaible_moves.append(new_double_move_square_index)
        avaible_moves.append(init_square_index + move_offset)

    kill_offsets = [-9, -7] if isPawnWhite else [7, 9]
    if current_column == 0:
        offset_to_remove = -9 if isPawnWhite else 7
        kill_offsets.remove(offset_to_remove)
    elif current_column == ROWS_AMOUNT - 1:
        offset_to_remove = -7 if isPawnWhite else 9
        kill_offsets.remove(offset_to_remove)

    for kill_offset in kill_offsets:
        new_kill_square_index = init_square_index + kill_offset
        other_piece = squares[new_kill_square_index].occupying_piece
        if other_piece is not None:
            if other_piece.color == piece.color:
                continue
            else:
                avaible_moves.append(new_kill_square_index)

    """ Implementation of en passant """
    pawn_move = None
    if GameManager.moves_history != []:
        pawn_move = GameManager.moves_history[-1]

    if pawn_move is not None:
        other_init_index = pawn_move[0]
        init_row = other_init_index // ROWS_AMOUNT

        other_target_index = pawn_move[1]
        target_row = other_target_index // ROWS_AMOUNT
        target_col = other_target_index % ROWS_AMOUNT

        other_piece_color = PieceColor.black if isPawnWhite else PieceColor.white
        other_piece_init_row = 6 if other_piece_color == PieceColor.white else 1
        if (
            init_row == other_piece_init_row
            and abs(target_row - init_row) == 2
            and target_row == current_row
        ):
            if current_column - target_col == 1:
                avaible_moves.append(init_square_index + kill_offsets[0])
                en_passant_square_index = other_target_index
            elif target_col - current_column == 1:
                avaible_moves.append(init_square_index + kill_offsets[1])
                en_passant_square_index = other_target_index

    return (avaible_moves, en_passant_square_index)


def calculate_king_moves(init_square_index, squares):
    color = squares[init_square_index].occupying_piece.color
    offsets = [-1, 7, -9, -8, 8, 1, -7, 9]
    if init_square_index % 8 == 0:
        offsets = offsets[3:]
    elif (init_square_index + 1) % 8 == 0:
        offsets = offsets[: (len(offsets) - 3)]
    avaible_moves = []
    new_index = None
    for offset in offsets:
        new_index = init_square_index + offset
        if new_index < 64 and new_index >= 0:
            other_piece = squares[new_index].occupying_piece
            if other_piece is not None and other_piece.color == color:
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
