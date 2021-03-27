import pygame

class BoardConstants:
    '''
    Constants that dictate size and logistics of the game board.
    '''
    WIDTH = 1000
    HEIGHT = 1000
    ROWS = 8
    COLS = 8
    SQUARE_SIZE = WIDTH // COLS

class ColorConstants:
    '''
    RGB color constants.
    '''
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    GREY = (128, 128, 128)

class PygameConstants:
    '''
    Constants for Pygame data structures.
    '''
    FPS = 60

class PieceConstants:
    '''
    Constants for the Piece class.
    '''
    PADDING = 12
    OUTLINE = 2

class AssetConstants:
    '''
    Constants for assets used throughout the game.
    '''
    CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
