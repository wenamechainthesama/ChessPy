import pygame
from sys import exit
from os.path import abspath, dirname
from GameEntities.board import Board
from GameEntities.enums import PieceColor, PieceType
from GameEntities.movesGeneration import save_precomputed_move_data

"""
TODO:
1) make queen (and other pieces) from pawn
2) move order

LATER:
1) concept of check, mate, and stalemate
2) castling
3) sound effects
"""

# Define constants
FPS = 60
BOARD_SIZE = 800
ROWS_AMOUNT = 8
WHITE = (204, 166, 133)
BLACK = (145, 118, 89)
ASSETS_PATH = f"{abspath(dirname(__file__))}\\PiecesImages"

def get_square_index_by_coords(pos):
    return pos[1] // 100 * ROWS_AMOUNT + pos[0] // 100

def promote_pawn(screen, target_square, move_order_color):
    filenames = ["02", "05", "03", "04"] if move_order_color == PieceColor.black else ["14", "13", "15", "12"]
    box = pygame.Surface((100, 400))
    box.fill((219, 80, 15))
    box_y = target_square.center[1]
    if move_order_color == PieceColor.white:
        box_y -= 300
    screen.blit(box, (target_square.center[0], box_y))
    for filename, offset in zip(filenames, [0, 100, 200, 300]):
        screen.blit(pygame.transform.scale(pygame.image.load(f"{ASSETS_PATH}\\{filename}.png").convert_alpha(), (100, 100)), (target_square.center[0], box_y + offset))

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

    pawn_move = None
    en_passant_square_index = None
    is_piece_being_held = False
    is_pawn_promotion = False
    move_order_color = PieceColor.white
    init_square_index = None
    legal_square_indexes = None
    promotion_box_squares = []
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            """ To interrupt the game hit escape """
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

            clicked_square_index = get_square_index_by_coords(pygame.mouse.get_pos())
            clicked_square = board.get_square_by_index(clicked_square_index)
            if clicked_square.occupying_piece is not None:
                if event.type == pygame.MOUSEBUTTONDOWN and clicked_square.occupying_piece.color == move_order_color and not is_pawn_promotion:
                    is_piece_being_held = True
                    init_square_index = clicked_square_index
                    legal_square_indexes, en_passant_square_index = board.highlight_legal_moves(init_square_index, pawn_move)
            if event.type == pygame.MOUSEBUTTONUP:
                if is_pawn_promotion and clicked_square_index in promotion_box_squares:
                    piece_to_gain = [PieceType.queen, PieceType.rook, PieceType.bishop, PieceType.knight]
                    is_pawn_promotion = False
                    row = clicked_square_index // ROWS_AMOUNT
                    piece_to_gain_index = row if move_order_color == PieceColor.black else ROWS_AMOUNT - 1 - row
                    board.get_square_by_index(pawn_move[1]).occupying_piece.type = piece_to_gain[piece_to_gain_index]
                    board.draw(screen, board.generate_fen())
                elif is_piece_being_held:
                    is_piece_being_held = False
                    if board.squares[clicked_square_index].color == (73, 52, 227):
                        offset = 8 if move_order_color == PieceColor.white else -8
                        if en_passant_square_index is not None and (clicked_square_index + offset) == en_passant_square_index:
                            board.get_square_by_index(en_passant_square_index).occupying_piece = None
                        pawn_move, is_pawn_promotion = board.make_move(screen, init_square_index, clicked_square_index, is_pawn_promotion)
                        move_order_color = PieceColor.white if move_order_color == PieceColor.black else PieceColor.black
                    else:
                        board.drop_piece_back(init_square_index)
                        board.draw(screen, board.generate_fen())
                    legal_square_indexes.append(init_square_index)
                    for square_index in legal_square_indexes:
                        square = board.get_square_by_index(square_index)
                        square.color = WHITE if (square_index // ROWS_AMOUNT + square_index % ROWS_AMOUNT) % 2 == 0 else BLACK
                    legal_square_indexes = None
                    board.draw(screen, board.generate_fen())

        if is_piece_being_held:
            board.draw(screen, board.generate_fen())
            square = board.get_square_by_index(init_square_index)
            shadow_image = square.occupying_piece.image.copy()
            shadow_image.set_alpha(128)
            screen.blit(shadow_image, square.center)
            board.choose_piece(screen, pygame.mouse.get_pos(), init_square_index)

        elif is_pawn_promotion:
            offset = -8 if move_order_color == PieceColor.white else 8
            promotion_box_squares = [pawn_move[1], pawn_move[1] + offset, pawn_move[1] + offset * 2, pawn_move[1] + offset * 3]
            promote_pawn(screen, board.get_square_by_index(pawn_move[1]), move_order_color)

        """ Lock mouse inside the screen """
        pygame.event.set_grab(True)

        pygame.display.flip()

if __name__ == "__main__":
    main()