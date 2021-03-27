import pygame
from constants import ColorConstants, BoardConstants, PieceConstants, AssetConstants

class Piece:
    '''
    A class that wraps a single checkers piece.
    '''

    def __init__(self,
                row,
                col,
                color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        '''
        Calculates this piece's position based on which square it should be in.
        '''
        self.x = BoardConstants.SQUARE_SIZE * self.col + BoardConstants.SQUARE_SIZE // 2
        self.y = BoardConstants.SQUARE_SIZE * self.row + BoardConstants.SQUARE_SIZE // 2

    def make_king(self):
        '''
        This method will turn this piece into a king.
        '''
        print('making king')
        self.king = True

    def draw(self, win):
        '''
        This method will draw this piece.
        '''
        radius = BoardConstants.SQUARE_SIZE // 2 - PieceConstants.PADDING
        pygame.draw.circle(win, ColorConstants.GREY, (self.x, self.y), radius + PieceConstants.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(AssetConstants.CROWN, (self.x - AssetConstants.CROWN.get_width() // 2, self.y - AssetConstants.CROWN.get_height() // 2))

    def move(self, row, col):
        '''
        A method that moves the piece to another square on the board.
        '''
        self.row = row
        self.col = col
        self.calculate_position()

    def __repr__(self):
        '''
        Internal representation of this object.
        '''
        str(self.color)
