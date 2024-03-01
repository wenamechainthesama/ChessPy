from piece import Piece
from square import Square
from enums import PieceType, PieceColor
from game_manager import GameManager
from moves_generation import *
from constants import *


class Board:
    def __init__(self):
        self.squares = []
        self.piece_mark_accordance = {
            "r": PieceType.rook,
            "n": PieceType.knight,
            "b": PieceType.bishop,
            "q": PieceType.queen,
            "k": PieceType.king,
            "p": PieceType.pawn,
        }
        self.calculation_function_type_of_piece_based = {
            PieceType.queen: calculate_sliding_moves,
            PieceType.rook: calculate_sliding_moves,
            PieceType.bishop: calculate_sliding_moves,
            PieceType.knight: calculate_knight_moves,
            PieceType.pawn: calculate_pawn_moves,
            PieceType.king: calculate_king_moves,
        }

        self.white_king_position = 60
        self.black_king_position = 4

        self.initialize_squares()

    def initialize_squares(self):
        for row in range(ROWS_AMOUNT):
            for column in range(ROWS_AMOUNT):
                square_color = WHITE if (row + column) % 2 == 0 else BLACK
                self.squares.append(Square((column * 100, row * 100), square_color))

    def setup_position(self, screen, fen):
        square_index = 0
        for letter in fen:
            if letter.isdigit():
                square_index += int(letter)
                continue
            current_square = self.squares[square_index]
            piece_type = self.piece_mark_accordance[letter.lower()]
            piece_color = PieceColor.black if letter.isupper() else PieceColor.white
            piece = Piece(piece_type, piece_color)
            if current_square.occupying_piece is not None:
                piece.ever_moved = current_square.occupying_piece.ever_moved
            piece.draw(screen, current_square.center)
            current_square.occupying_piece = piece
            square_index += 1

    def choose_piece(self, screen, mouse_pos, init_square_index):
        square = self.squares[init_square_index]
        if square.occupying_piece is not None:
            """Hold piece by cursor until dropped"""
            piece = square.occupying_piece
            piece.chosen = True
            new_piece_coords = (mouse_pos[0] - 50, mouse_pos[1] - 50)
            piece.draw(screen, new_piece_coords)

    def make_move(self, init_square_index, target_square_index, is_validating=False):
        init_square = self.squares[init_square_index]
        target_square = self.squares[target_square_index]

        """ Save king position for check verification """
        if init_square.occupying_piece.type == PieceType.king:
            color = init_square.occupying_piece.color
            is_castling = False
            if (
                target_square.occupying_piece is not None
                and target_square.occupying_piece.color == color
            ):
                is_castling = True
                if not is_validating:
                    GameManager.is_castling = True
                king_jorney_distance = abs(target_square_index - init_square_index)
                king_square_index, rook_square_index = (
                    init_square_index,
                    target_square_index,
                )
                """ Long castle """
                if king_jorney_distance == 4:
                    king_square_index -= 2
                    rook_square_index += 3

                # """ Short castle """
                elif king_jorney_distance == 3:
                    king_square_index += 2
                    rook_square_index -= 2

                target_square_index = king_square_index

                king_square = self.squares[king_square_index]
                rook_square = self.squares[rook_square_index]

                """ Moving rook """
                rook_square.occupying_piece = target_square.occupying_piece
                rook_square.occupying_piece.ever_moved = True
                target_square.occupying_piece = None

                """ Moving king """
                init_square.occupying_piece.chosen = False
                king_square.occupying_piece = init_square.occupying_piece
                king_square.occupying_piece.ever_moved = True
                init_square.occupying_piece = None

            if not is_validating:
                if color == PieceColor.white:
                    self.white_king_position = target_square_index
                else:
                    self.black_king_position = target_square_index

            if is_castling:
                return

        init_square.occupying_piece.chosen = False
        init_square.occupying_piece.ever_moved = True
        target_square.occupying_piece = init_square.occupying_piece
        init_square.occupying_piece = None

    @staticmethod
    def get_square_index_by_coords(pos):
        return pos[1] // 100 * ROWS_AMOUNT + pos[0] // 100

    def validate_move_on_legality(self, screen, init_square_index, target_square_index):
        """
        Broad-force approach:
        Make move that we wanna validate on the copy of board
        and if king was captured this move is obviosly illegal
        """
        temp_board = Board()
        temp_board.white_king_position = self.white_king_position
        temp_board.black_king_position = self.black_king_position
        temp_board.setup_position(screen, self.generate_fen())
        temp_board.make_move(init_square_index, target_square_index, is_validating=True)
        responses = temp_board.get_all_possible_moves()
        piece_type = self.squares[init_square_index].occupying_piece.type
        if piece_type == PieceType.king:
            return target_square_index not in responses
        
        kings_color = (
            PieceColor.white if GameManager.is_white_move else PieceColor.black
        )
        kings_position = (
            temp_board.white_king_position
            if kings_color == PieceColor.white
            else temp_board.black_king_position
        )

        return kings_position not in responses

    def get_all_possible_moves(board):
        legal_square_indexes_global = []
        piece_color_needed = (
            PieceColor.white if not GameManager.is_white_move else PieceColor.black
        )
        for square_index, square in enumerate(board.squares):
            piece = square.occupying_piece
            if piece is not None and piece.color == piece_color_needed:
                calculation_function = board.calculation_function_type_of_piece_based[
                    piece.type
                ]
                legal_square_indexes_local = []
                if piece.type == PieceType.pawn:
                    legal_square_indexes_local, _ = calculate_pawn_moves(
                        square_index, board.squares
                    )
                else:
                    legal_square_indexes_local = calculation_function(
                        square_index, board.squares
                    )
                legal_square_indexes_global.extend(legal_square_indexes_local)
        return legal_square_indexes_global

    # def is_threatened_square(self, square_index):
    #     for current_square_index, square in enumerate(self.squares):
    #         piece_on_current_square = square.occupying_piece
    #         if piece_on_current_square is not None:
    #             calculation_function = self.calculation_function_type_of_piece_based[
    #                 piece_on_current_square.type
    #             ]
    #             """ Calculate 'legal' moves of current piece"""
    #             pseudo_legal_moves = []
    #             if piece_on_current_square.type == PieceType.pawn:
    #                 pseudo_legal_moves_to_check, _ = calculation_function(
    #                     current_square_index, self.squares
    #                 )
    #                 for pseudo_legal_move in pseudo_legal_moves_to_check:
    #                     if pseudo_legal_move % ROWS_AMOUNT != current_square_index % ROWS_AMOUNT:
    #                         pseudo_legal_moves.append(current_square_index)
    #             else:
    #                 pseudo_legal_moves = calculation_function(
    #                     current_square_index, self.squares
    #                 )

    #             """ If any piece can move to this square so it's threatened """
    #             if square_index in pseudo_legal_moves:
    #                 return True
    #     return False

    def highlight_legal_moves(self, screen, init_square_index):
        print("P", init_square_index)
        square = self.squares[init_square_index]
        pieceType = square.occupying_piece.type
        calculation_function = self.calculation_function_type_of_piece_based[pieceType]
        legal_square_indexes = []
        en_passant_square_index = None
        if pieceType == PieceType.pawn:
            legal_square_indexes, en_passant_square_index = calculate_pawn_moves(
                init_square_index, self.squares
            )
        else:
            legal_square_indexes = calculation_function(init_square_index, self.squares)

        for square_index in legal_square_indexes:
            if self.validate_move_on_legality(screen, init_square_index, square_index):
                self.squares[square_index].color = BLUE
        self.squares[init_square_index].color = (128, 52, 235)

        return (legal_square_indexes, en_passant_square_index)

    def drop_piece_back(self, init_square_index):
        self.squares[init_square_index].occupying_piece.chosen = False

    def generate_fen(self):
        """
        FEN is a standard notation for describing a particular board position of a chess game
        More: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        """
        fen = ""
        empty_square_counter = 0
        for square in self.squares:
            if empty_square_counter == ROWS_AMOUNT:
                empty_square_counter = 0
                fen += str(ROWS_AMOUNT)
            related_piece = square.occupying_piece
            if related_piece is not None and not related_piece.chosen:
                if empty_square_counter:
                    fen += str(empty_square_counter)
                    empty_square_counter = 0
                piece_type = related_piece.type
                piece_color = related_piece.color
                letter = list(self.piece_mark_accordance.keys())[
                    list(self.piece_mark_accordance.values()).index(piece_type)
                ]
                if piece_color:
                    letter = letter.upper()
                fen += letter
            else:
                empty_square_counter += 1

        return fen

    def get_square_by_index(self, square_index):
        return self.squares[square_index]

    def draw(self, screen, fen):
        """At first draw squares"""
        for square in self.squares:
            square.draw(screen)

        """ And only then pieces """
        self.setup_position(screen, fen)
