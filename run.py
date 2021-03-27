import pygame
import time
from constants import BoardConstants, PygameConstants, ColorConstants
from game.game import Game
from minimax.algorithm import minimax

window = pygame.display.set_mode((BoardConstants.WIDTH, BoardConstants.HEIGHT))
pygame.display.set_caption('Minimax Checkers AI')

def get_position_from_mouse(pos):
    '''
    Returns the row and column of the position passed into this method.
    '''
    x, y = pos
    row = y // BoardConstants.SQUARE_SIZE
    col = x // BoardConstants.SQUARE_SIZE
    return row, col

def run_game():
    run = True
    clock = pygame.time.Clock()
    game = Game(window)

    while run:
        clock.tick(PygameConstants.FPS)

        if game.turn == ColorConstants.WHITE:
            value, new_board = minimax(game.get_board(), 3, ColorConstants.WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            while True: time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_position_from_mouse(pos)
                if game.turn == ColorConstants.RED or game.turn == ColorConstants.WHITE:
                    game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == '__main__':
    run_game()
