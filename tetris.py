import pygame
from tetrisgame import TetrisGame


def main():
    pygame.init()
    global running
    running = True
    width = 10
    height = 20
    BLOCK_SIZE = 32

    screen = pygame.display.set_mode((width * BLOCK_SIZE, height * BLOCK_SIZE))
    pygame.display.set_caption('Tetris')
    game = TetrisGame(width, height, BLOCK_SIZE)
    game.begin()

    clock = pygame.time.Clock()

    while running:
        try:
            clock.tick(60)
            game.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == TetrisGame.GAMEOVEREVENT:
                    game.game_over()
                elif event.type == TetrisGame.TICKEVENT:
                    game.tick()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        game.get_active_piece().move_right()
                    elif event.key == pygame.K_LEFT:
                        game.get_active_piece().move_left()
                    elif event.key == pygame.K_DOWN:
                        game.move_active_down()
                        game.set_tick_time(TetrisGame.TICK_TIME_FAST)
                    elif event.key == pygame.K_UP:
                        game.get_active_piece().rotate()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        game.set_tick_time(TetrisGame.TICK_TIME)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game.is_game_over():
                        game.restart()
            pygame.display.flip()
        except Exception:
            running = False
            pygame.quit()
            raise


if __name__ == '__main__':
    main()
