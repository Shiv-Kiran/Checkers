import pygame
from checkers.constants import RED_RUBY, SQUARE_SIZE, WHITE_MARBLE, WIDTH, HEIGHT
from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60
DEPTH = 4
pygame.init()
WIN = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row, col = y//SQUARE_SIZE, x//SQUARE_SIZE
    return row, col


def main():
    clock = pygame.time.Clock()
    running: bool = True
    game = Game(WIN)
    while running:
        clock.tick(FPS)
        if game.turn == WHITE_MARBLE:
            value, new_board = minimax(
                game.get_board(), DEPTH, WHITE_MARBLE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            # running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # print(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    pygame.quit()


main()
