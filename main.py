import pygame
from sys import exit
from GameEntities.board import Board
from GameEntities.movesGeneration import save_precomputed_move_data

"""
TODO:
1) en passant
2) make queen (and other pieces) from pawn
3) follow move order

LATER:
concept of check, mate, and stalemate
castling
sound effects
"""

# Define constants
FPS = 60
BOARD_SIZE = 800
ROWS_AMOUNT = 8
WHITE = (204, 166, 133)
BLACK = (145, 118, 89)

def get_square_index_by_coords(pos):
    return pos[1] // 100 * ROWS_AMOUNT + pos[0] // 100

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
    init_square_index = None
    legal_square_indexes = None
    while True:
        clock.tick(FPS)
        """ Lock mouse inside the screen """
        pygame.event.set_grab(True)
        for event in pygame.event.get():
            """ To interrupt the game hit escape """
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

            clicked_square_index = get_square_index_by_coords(pygame.mouse.get_pos())
            clicked_square = board.get_square_by_index(clicked_square_index)
            if clicked_square.occupying_piece is not None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_piece_being_held = True
                    init_square_index = clicked_square_index
                    legal_square_indexes, en_passant_square_index = board.highlight_legal_moves(init_square_index, pawn_move)
            if event.type == pygame.MOUSEBUTTONUP and is_piece_being_held:
                is_piece_being_held = False
                if en_passant_square_index is not None:
                    board.get_square_by_index(en_passant_square_index).occupying_piece = None
                if board.squares[clicked_square_index].color == (73, 52, 227):
                    pawn_move = board.make_move(screen, init_square_index, clicked_square_index)
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

        pygame.display.flip()

if __name__ == "__main__":
    main()