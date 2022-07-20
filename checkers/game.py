import pygame

from checkers.piece import Piece
from .constants import BLUE_GREEN, COLS, RED_RUBY, ROWS, SQUARE_SIZE, WHITE_MARBLE
from .board import Board


class Game:
    def __init__(self, win: pygame.Surface):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED_RUBY
        self.valid_moves = {}

    def reset(self):
        self._init()

    def winner(self):
        return self.board.winner()

    def select(self, row, col):
        '''
        Return if the selection of particular piece/square is valid or not. 
        '''
        if self.selected:  # after selection we are selecting another place.
            result = self._move(row, col)
            if not result:  # checking validity.
                self.selected = None
                self.select(row, col)

          # If no player is selected
        piece = self.board.get_piece(row, col)
        # current piece is current player piece.
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # free space and valid move
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED_RUBY:
            self.turn = WHITE_MARBLE
        else:
            self.turn = RED_RUBY

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE_GREEN, (col*SQUARE_SIZE +
                               SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), Piece.PADDING)

# AI IMPLEMENTATION

    def get_board(self):
        return self.board

    def ai_move(self, board):
        # ai will return the best moved board as the parameter.
        self.board = board
        self.change_turn()
