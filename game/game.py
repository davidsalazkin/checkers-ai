import pygame
from game.board import Board
from constants import ColorConstants, BoardConstants

class Game:
    '''
    A class that facilitates the rules and possible movements of the game.
    '''

    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        '''
        A helper method that sets the game to its initial state.
        '''
        self.selected = None
        self.board = Board()
        self.turn = ColorConstants.RED
        self.valid_moves = {}

    def _move(self, row, col):
        '''
        This method facilitates the movement of the pieces.
        '''
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move_piece(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        '''
        This method toggles the players turns.
        '''
        self.valid_moves = []
        if self.turn == ColorConstants.RED:
            self.turn = ColorConstants.WHITE
        else:
            self.turn = ColorConstants.RED

    def update(self):
        '''
        This method updates the board's visual state.
        '''
        self.board.draw_board(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        '''
        This method resets the game to its initial state.
        '''
        self._init()

    def select(self, row, col):
        '''
        This method facilitates the selection of pieces.
        '''
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def draw_valid_moves(self, moves):
        '''
        Draws the valid moves upon selection of a piece.
        '''
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, ColorConstants.YELLOW, (col * BoardConstants.SQUARE_SIZE + BoardConstants.SQUARE_SIZE // 2, row * BoardConstants.SQUARE_SIZE + BoardConstants.SQUARE_SIZE // 2), 15)

    def winner(self):
        return self.board.winner()
