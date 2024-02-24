from GameEntities.piece import Piece
from GameEntities.square import Square
from GameEntities.enums import PieceType, PieceColor
from GameEntities.game_manager import GameManager
from GameEntities.moves_generation import *
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

    def make_move(self, screen, init_square_index, target_square_index):
        # board_corners = [56, 63, 0, 7]

        GameManager.move_made(init_square_index, target_square_index)
        init_square = self.squares[init_square_index]
        # color = init_square.occupying_piece.color
        target_square = self.squares[target_square_index]

        """ Phorbiding castling """
        # if init_square.occupying_piece.type == PieceType.king:
        #     if target_square.occupying_piece.type == PieceType.rook:
        #         print("Hi")
        #     elif color == PieceColor.white:
        #         GameManager.is_castle_for_white_king_side_avaible = False
        #         GameManager.is_castle_for_white_queen_side_avaible = False
        #     else:
        #         GameManager.is_castle_for_black_king_side_avaible = False
        #         GameManager.is_castle_for_black_queen_side_avaible = False
        # elif init_square.occupying_piece.type == PieceType.rook:
        #     if init_square_index == board_corners[0]:
        #         GameManager.is_castle_for_white_queen_side_avaible = False
        #     elif init_square_index == board_corners[1]:
        #         GameManager.is_castle_for_white_king_side_avaible = False
        #     elif init_square_index == board_corners[2]:
        #         GameManager.is_castle_for_black_queen_side_avaible = False
        #     elif init_square_index == board_corners[3]:
        #         GameManager.is_castle_for_black_king_side_avaible = False
        # elif (
        #     target_square.occupying_piece is not None
        #     and target_square.occupying_piece.type == PieceType.rook
        # ):
        #     if target_square_index == board_corners[0]:
        #         GameManager.is_castle_for_white_queen_side_avaible = False
        #     elif target_square_index == board_corners[1]:
        #         GameManager.is_castle_for_white_king_side_avaible = False
        #     elif target_square_index == board_corners[2]:
        #         GameManager.is_castle_for_black_queen_side_avaible = False
        #     elif target_square_index == board_corners[3]:
        #         GameManager.is_castle_for_black_king_side_avaible = False

        init_square.occupying_piece.chosen = False
        target_square.occupying_piece = init_square.occupying_piece
        init_square.occupying_piece = None
        fen = self.generate_fen()
        self.draw(screen, fen)

        row = target_square_index // ROWS_AMOUNT
        if target_square.occupying_piece.type == PieceType.pawn and row in [0, 7]:
            GameManager.is_pawn_promoting = True

    @staticmethod
    def get_square_index_by_coords(pos):
        return pos[1] // 100 * ROWS_AMOUNT + pos[0] // 100

    def highlight_legal_moves(self, init_square_index):
        calculation_function_type_of_piece_based = {
            PieceType.queen: calculate_sliding_moves,
            PieceType.rook: calculate_sliding_moves,
            PieceType.bishop: calculate_sliding_moves,
            PieceType.knight: calculate_knight_moves,
            PieceType.pawn: calculate_pawn_moves,
            PieceType.king: calculate_king_moves,
        }
        square = self.get_square_by_index(init_square_index)
        pieceType = square.occupying_piece.type
        calculation_function = calculation_function_type_of_piece_based[pieceType]
        legal_square_indexes = []
        en_passant_square_index = None
        if pieceType == PieceType.pawn:
            legal_square_indexes, en_passant_square_index = calculate_pawn_moves(
                init_square_index, self.squares
            )
        else:
            legal_square_indexes = calculation_function(init_square_index, self.squares)

        for square_index in legal_square_indexes:
            self.get_square_by_index(square_index).color = BLUE
        self.get_square_by_index(init_square_index).color = (128, 52, 235)

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
