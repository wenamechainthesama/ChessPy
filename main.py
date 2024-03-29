import pygame
from sys import exit
from os.path import abspath, dirname
from board import Board
from enums import PieceType, GameState
from piece import Piece
from moves_generation import save_precomputed_move_data
from constants import *
from game_manager import GameManager
from audio_player import Sound

"""
TODO:
clean-up & bug fix
sound effects
"""

ASSETS_PATH = f"{abspath(dirname(__file__))}\\PiecesImages"


# Setup & Run Game
def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    save_precomputed_move_data()

    initial_position_fen = "RNBQKBNRPPPPPPPP8888pppppppprnbqkbnr"
    board = Board()
    board.draw(screen, initial_position_fen)

    while True:
        clock.tick(FPS)
        """ Lock mouse inside the screen """
        # pygame.event.set_grab(True)
        for event in pygame.event.get():
            """To interrupt the game hit escape"""
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                exit()

            if GameManager.game_state == GameState.playing:
                clicked_square_index = board.get_square_index_by_coords(
                    pygame.mouse.get_pos()
                )
                clicked_square = board.get_square_by_index(clicked_square_index)
                if clicked_square.occupying_piece is not None:
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and not GameManager.is_pawn_promoting
                        and GameManager.is_right_color(
                            clicked_square.occupying_piece.color
                        )
                    ):
                        GameManager.is_piece_being_held = True
                        init_square_index = clicked_square_index
                        legal_square_indexes, en_passant_square_index = (
                            board.highlight_legal_moves(screen, init_square_index)
                        )
                if event.type == pygame.MOUSEBUTTONUP:
                    promotion_box_squares = []
                    if GameManager.moves_history != []:
                        offset = -8 if GameManager.is_white_move else 8
                        promotion_box_squares = [
                            GameManager.moves_history[-1][1],
                            GameManager.moves_history[-1][1] + offset,
                            GameManager.moves_history[-1][1] + offset * 2,
                            GameManager.moves_history[-1][1] + offset * 3,
                        ]
                    if (
                        GameManager.is_pawn_promoting
                        and clicked_square_index in promotion_box_squares
                    ):
                        piece_to_gain = [
                            PieceType.queen,
                            PieceType.rook,
                            PieceType.bishop,
                            PieceType.knight,
                        ]
                        GameManager.is_pawn_promoting = False
                        row = clicked_square_index // ROWS_AMOUNT
                        piece_to_gain_index = (
                            row
                            if not GameManager.is_white_move
                            else ROWS_AMOUNT - 1 - row
                        )
                        board.get_square_by_index(
                            GameManager.moves_history[-1][1]
                        ).occupying_piece.type = piece_to_gain[piece_to_gain_index]
                        board.draw(screen, board.generate_fen())
                        board.audioplayer.play(Sound.check)
                    elif GameManager.is_piece_being_held:
                        GameManager.is_piece_being_held = False
                        if (
                            board.get_square_by_index(clicked_square_index).color
                            == BLUE
                        ):
                            offset = -8 if not GameManager.is_white_move else 8
                            if (
                                en_passant_square_index is not None
                                and (clicked_square_index + offset)
                                == en_passant_square_index
                            ):
                                board.get_square_by_index(
                                    en_passant_square_index
                                ).occupying_piece = None
                            board.make_move(
                                init_square_index,
                                clicked_square_index,
                            )
                            row = clicked_square_index // ROWS_AMOUNT
                            """ Switch turn and remember move """
                            if GameManager.is_castling:
                                GameManager.move_made(
                                    init_square_index,
                                    (
                                        board.white_king_position
                                        if GameManager.is_white_move
                                        else board.black_king_position
                                    ),
                                )
                            else:
                                GameManager.move_made(
                                    init_square_index, clicked_square_index
                                )
                            if (
                                not GameManager.is_castling
                                and clicked_square.occupying_piece.type
                                == PieceType.pawn
                                and row in [0, 7]
                            ):

                                GameManager.is_pawn_promoting = True
                            GameManager.is_castling = False
                            fen = board.generate_fen()
                            board.draw(screen, fen)
                        else:
                            board.drop_piece_back(init_square_index)
                            board.draw(screen, board.generate_fen())

                        legal_square_indexes.append(init_square_index)
                        for square_index in legal_square_indexes:
                            square = board.get_square_by_index(square_index)
                            row = square_index // ROWS_AMOUNT
                            column = square_index % ROWS_AMOUNT
                            square.color = WHITE if (row + column) % 2 == 0 else BLACK
                        legal_square_indexes = None
                        board.draw(screen, board.generate_fen())
                    pygame.display.flip()
                    board.detect_checkmate(screen)
                    board.detect_stalemate()

        if GameManager.game_state == GameState.playing:
            if GameManager.is_piece_being_held:
                board.draw(screen, board.generate_fen())
                square = board.get_square_by_index(init_square_index)
                shadow_image = square.occupying_piece.image.copy()
                shadow_image.set_alpha(128)
                screen.blit(shadow_image, square.center)
                board.choose_piece(screen, pygame.mouse.get_pos(), init_square_index)

            elif GameManager.is_pawn_promoting:
                Piece.promote_pawn(
                    screen, board.get_square_by_index(GameManager.moves_history[-1][1])
                )
        else:
            if GameManager.game_state == GameState.white_won:
                text = "White won"
                pos = (150, 300)
            elif GameManager.game_state == GameState.black_won:
                text = "Black won"
                pos = (175, 300)
            elif GameManager.game_state == GameState.draw:
                pos = (275, 300)
                text = "Draw"

            my_font = pygame.font.SysFont("Comic Sans MS", 100)
            text_surface = my_font.render(text, False, (252, 3, 3))
            screen.blit(text_surface, pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()
