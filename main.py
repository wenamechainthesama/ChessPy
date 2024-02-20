import pygame
from sys import exit
from GameEntities.enums import PieceType
from GameEntities.board import Board
from GameEntities.pseudoLegalMoveGenerator import PseudoLegalMoveGenerator

# Define constants
FPS = 60
BOARD_SIZE = 800
ROWS_AMOUNT = 8

def get_square_index_by_coords(pos):
    return pos[1] // 100 * ROWS_AMOUNT + pos[0] // 100

# Setup & Run Game
def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    initial_position_fen = "RNBKQBNRPPPPPPPP8888pppppppprnbkqbnr"
    board = Board()
    board.draw(screen, initial_position_fen)

    is_piece_being_held = False
    init_square_index = None
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            clicked_square_index = get_square_index_by_coords(pygame.mouse.get_pos())
            clicked_square = board.get_square_by_index(clicked_square_index)
            if clicked_square.occupying_piece is not None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_piece_being_held = True
                    init_square_index = clicked_square_index
            if event.type == pygame.MOUSEBUTTONUP and is_piece_being_held:
                # calculation_function_type_of_piece_based = {
                #     PieceType.queen or PieceType.rook or PieceType.bishop: PseudoLegalMoveGenerator.calculate_sliding_moves,
                #     PieceType.knight: PseudoLegalMoveGenerator.calculate_knight_moves,
                #     PieceType.pawn: PseudoLegalMoveGenerator.calculate_pawn_moves,
                #     PieceType.king: PseudoLegalMoveGenerator.calculate_king_moves,
                # }
                # is_piece_being_held = False
                current_square_index = clicked_square_index
                # calculation_function = calculation_function_type_of_piece_based[pieceType]
                # is_move_legal = calculation_function(init_square_index)
                is_move_legal = True
                if is_move_legal:
                    board.make_move(init_square_index, current_square_index)
                    fen = board.generate_fen()
                    board.draw(screen, fen)
                else:
                    board.drop_piece_back(init_square_index)
                    board.draw(screen, board.generate_fen())

        if is_piece_being_held:
            board.draw(screen, board.generate_fen())
            board.choose_piece(screen, pygame.mouse.get_pos(), init_square_index)

        pygame.display.flip()

if __name__ == "__main__":
    main()