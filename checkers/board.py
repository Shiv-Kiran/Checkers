'''
Moving Specific pieces erasing
'''
from matplotlib.pyplot import pie
import pygame

from checkers.piece import Piece
from .constants import COLS, GREEN_LIGHT, RED_RUBY, ROWS, SQUARE_SIZE, WHITE_MARBLE, WOODEN_YELLOW


class Board:
    def __init__(self):
        '''
        Here we will initialize board and its pieces.
        '''
        self.board = []  # for storing pieces and free spaces.
        self.selected_piece = None
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win: pygame.Surface):
        '''
        This function just draws the basic outline of the checkers board.
        '''
        win.fill(GREEN_LIGHT)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(
                    win, WOODEN_YELLOW, (row*SQUARE_SIZE,
                                         col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece: Piece, row, col):
        '''
        Function for moving the pieces and checking other positions
        '''
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS-1 or row == 0:
            piece.make_king()
        if piece.color == WHITE_MARBLE:
            self.white_kings += 1
        else:
            self.red_kings += 1

    def create_board(self):
        '''
        This function adds the pieces to the board. 
        '''
        for row in range(ROWS):
            self.board.append([])
            # we need to select board[0][1], board[1][0]
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:  # draw white
                        self.board[row].append(Piece(row, col, WHITE_MARBLE))
                    elif row > 4:  # draw red
                        self.board[row].append(Piece(row, col, RED_RUBY))
                    else:  # store 0 in remaining so that we can track movement.
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def get_piece(self, row, col) -> Piece:
        return self.board[row][col]

    def draw(self, win: pygame.Surface):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece: Piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(win)

    def get_valid_moves(self, piece):
        '''
        We will go recursively to left and right diagnols till we reach edges of the board. 

        '''
        moves = {}
        left, right = piece.col - 1, piece.col+1
        row = piece.row
        # king has more valid moves.
        if piece.color == RED_RUBY or piece.king:
            # when it is red we can move upward 2 diagnols
            moves.update(self._traverse_left(
                row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(
                row-1, max(row-3, -1), -1, piece.color, right))

        if piece.color == WHITE_MARBLE or piece.king:
            # white can move downward 2 diagnols
            moves.update(self._traverse_left(
                row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(
                row+1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        '''
        start, stop, step to specify the row 
        skipped to mention if we jumped. 
        color to know the present player 
        '''
        moves = {}  # dictionary to store the possible moves with pieces jumped.
        found_piece = []
        for r in range(start, stop, step):
            if left < 0:  # outside the board
                break
            current = self.board[r][left]
            if current == 0:  # empty space just add not need to think more
                if skipped and not found_piece:
                    break
                elif skipped:  # if there is jumped
                    moves[(r, left)] = found_piece + skipped
                else:
                    moves[(r, left)] = found_piece

                if found_piece:  # deciding for next jump
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, left-1, skipped=found_piece))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, left+1, skipped=found_piece))

                break
            elif current.color == color:  # same color as present
                break
            else:  # different color
                found_piece = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        found_piece = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not found_piece:
                    break
                elif skipped:
                    moves[(r, right)] = found_piece + skipped
                else:
                    moves[(r, right)] = found_piece

                if found_piece:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, right-1, skipped=found_piece))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, right+1, skipped=found_piece))
                break
            elif current.color == color:
                break
            else:
                found_piece = [current]

            right += 1

        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED_RUBY:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0 or self.check_moves(WHITE_MARBLE):
            return WHITE_MARBLE
        elif self.white_left <= 0 or self.check_moves(RED_RUBY):
            return RED_RUBY

        return None

    def check_moves(self, color):
        pieces = self.get_all_pieces(color)
        for piece in pieces:
            if len(self.get_valid_moves(piece)) != 0:
                return False
            # print(color, "Hello there")
        # print("Out of Loop")
        return True
# AI IMPLEMENTATION

    def evaluate(self):
        return self.white_left - self.red_left + self.white_kings*0.5 - self.red_kings*0.5

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
