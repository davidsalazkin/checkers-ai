import pygame
from constants import ColorConstants, BoardConstants
from game.piece import Piece

class Board:
    '''
    A class that wraps the checkerboard.
    '''

    def __init__(self):
        self.board = []
        self.turn = 0
        self.red_left = 12
        self.red_kings = 0
        self.white_left = 12
        self.white_kings = 0

        self.initialize_board()

    def draw_squares(self, win):
        '''
        A helper method that draws the red and black squares in a pygame window
        in a checkerboard pattern.
        '''
        win.fill(ColorConstants.BLACK)
        for row in range(BoardConstants.ROWS):
            for col in range(row % 2, BoardConstants.ROWS, 2):
                pygame.draw.rect(
                    win,
                    ColorConstants.RED,
                    (row * BoardConstants.SQUARE_SIZE, col * BoardConstants.SQUARE_SIZE, BoardConstants.SQUARE_SIZE, BoardConstants.SQUARE_SIZE))

    def initialize_board(self):
        '''
        Initializes the initial board state representation.
        '''
        for row in range(BoardConstants.ROWS):
            self.board.append([])
            for col in range(BoardConstants.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, ColorConstants.WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, ColorConstants.RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move_piece(self, piece, row, col):
        '''
        This method moves a piece on the board.
        '''
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if (piece.king == False) and (row == BoardConstants.ROWS - 1 or row == 0):
            piece.make_king()
            if piece.color == ColorConstants.WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        '''
        This method returns the piece in the given row and column.
        '''
        return self.board[row][col]

    def draw_board(self, win):
        '''
        A method that draws the board and all of the pieces.
        '''
        self.draw_squares(win)
        for row in range(BoardConstants.ROWS):
            for col in range(BoardConstants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_valid_moves(self, piece):
        '''
        Returns a dict of valid moves for the given piece.
        '''
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == ColorConstants.RED or piece.king:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        if piece.color == ColorConstants.WHITE or piece.king:
            moves.update(self._traverse_left(row+1, min(row+3, BoardConstants.ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row+1, min(row+3, BoardConstants.ROWS), 1, piece.color, right))

        return moves

    def remove(self, pieces):
        '''
        Removes a piece from the board.
        '''
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == ColorConstants.RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return ColorConstants.RED
        elif self.white_left <= 0:
            return ColorConstants.WHITE

        return None

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        '''
        Checks the left diagonal.
        '''
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, BoardConstants.ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        '''
        Checks the right diagonal.
        '''
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= BoardConstants.COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, BoardConstants.ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def evaluate(self):
        '''
        Will return a score for the current state of the board.
        '''
        return (self.white_left - self.red_left) + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        '''
        Returns all pieces for the RGB color passed in.
        '''
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
