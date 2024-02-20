import pygame
from sys import exit
from GameEntities.board import Board

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

    board = Board()
    board.draw(screen)

    t = False
    init_square_index = None
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                t = True
                init_square_index = get_square_index_by_coords(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                t = False

        if t:
            board.choose_piece(screen, pygame.mouse.get_pos(), init_square_index)

        pygame.display.flip()

if __name__ == "__main__":
    main()