import pygame
import pygame.gfxdraw
import random

class TetrisGame(object):
    TICKEVENT = pygame.USEREVENT
    GAMEOVEREVENT = pygame.USEREVENT+1
    color_dict = [0xDBDBDB, 0x1D80A1, 0x57298F, 0xC437AF, 0xBD1717, 0x35A63E, 0xBCC416, 0x16C49C]

    def __init__(self, block_size):
        self.gameover = False
        self.BLOCK_SIZE = block_size
        self.width = 10
        self.height = 20
        self.board = [[0] * 10 for _ in range(20)]
        self.active_piece = Piece(4, 0, 3, self.BLOCK_SIZE, self)
        self.go_text = None
        self.go_font = None

    def draw(self, screen):
        screen.fill(TetrisGame.color_dict[0])
        if (self.active_piece):
            self.active_piece.draw_shadow(screen)
            self.active_piece.draw(screen)
        for i in range(self.height):
            for j in range(self.width):
                if (self.board[i][j]):
                    col = TetrisGame.color_dict[ self.board[i][j] ]
                    screen.fill(col, (j*self.BLOCK_SIZE, i*self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE ) )
        if self.gameover and self.go_text:
            pygame.gfxdraw.box(screen, (0, 0, self.BLOCK_SIZE*self.width, self.BLOCK_SIZE*self.height), (0, 0, 0, 128))
            screen.blit(self.go_text, (self.width*self.BLOCK_SIZE/2 - self.go_text.get_width()/2,
                                       self.height*self.BLOCK_SIZE/2 - self.go_text.get_height()/2))

    def get_active_piece(self):
        return self.active_piece

    def get_boardmatrix(self):
        return self.board

    def tick(self):
        self.move_active_down()

    def move_active_down(self):
        if not self.active_piece.move_down():
            self.active_piece.attach()
            self.active_piece = Piece(4, 0, random.randint(1, 7), self.BLOCK_SIZE, self)

    def clear_rows(self):
        for i, row in enumerate(self.board):
            if all(row):
                self.board.pop(i)
                self.board.insert(0, [0]*self.width)

    def game_over(self):
        self.gameover = True
        self.go_font = pygame.font.SysFont("Roboto,Arial", 52, bold=True)
        self.go_text = self.go_font.render("Game Over!", True, (255, 255, 255))
        pygame.time.set_timer(TetrisGame.TICKEVENT, 0)

class Piece(object):
    def __init__(self, x, y, _type, block_size, game_obj):
        self.x = x
        self.y = y
        self.type = _type
        self.BLOCK_SIZE = block_size
        self.game_obj = game_obj
        if (self.type == 1):
            self.m = [[1, 1, 1, 1]]
        elif (self.type == 2):
            self.m = [[1, 1, 1],
                       [0, 0, 1]]
        elif (self.type == 3):
            self.m = [[1, 1, 1],
                      [1, 0, 0]]
        elif (self.type == 4):
            self.m = [[1, 1],
                      [1, 1]]
        elif (self.type == 5):
            self.m = [[0, 1, 1],
                      [1, 1, 0]]
        elif (self.type == 6):
            self.m = [[1, 1, 1],
                      [0, 1, 0]]
        elif (self.type == 7):
            self.m = [[1, 1, 0],
                      [0, 1, 1]]
        else:
            raise RuntimeError("Incorrect Shape #")
        self.calc_dimensions()
        if self.collision():
            pygame.event.post(pygame.event.Event(TetrisGame.GAMEOVEREVENT))

    def calc_dimensions(self):
        self.width = len(self.m[0])
        self.height = len(self.m)

    def collision(self):
        for i in range(self.height):
            for j in range(self.width):
                if (self.m[i][j] and self.game_obj.get_boardmatrix()[self.y+i][self.x+j]):
                    return True
        return False

    def move_down(self):
        self.y += 1
        if ((self.y+self.height)>20):
            self.y -= 1
            return False
        if self.collision():
            self.y -= 1
            return False
        return True

    def move_right(self):
        self.x += 1
        if ((self.x+self.width) > 10) or self.collision():
            self.x -= 1
            return False
        return True

    def move_left(self):
        self.x -= 1
        if (self.x < 0) or self.collision():
            self.x += 1
            return False
        return True

    def rotate(self):
        _oldm = self.m
        self.m = list(zip(*reversed(self.m)))
        self.calc_dimensions()
        if (self.width+self.x > 10) or (self.height+self.y > 20) or self.collision():
            self.m = _oldm
            self.calc_dimensions()
            return False
        return True

    def attach(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.m[i][j]:
                    self.game_obj.get_boardmatrix()[self.y+i][self.x+j] = self.type
        self.game_obj.clear_rows()

    def draw_shadow(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.m[i][j]:
                    _rect = (self.BLOCK_SIZE*(self.x+j), self.BLOCK_SIZE*(self.y+i), self.BLOCK_SIZE+1, 20*self.BLOCK_SIZE)
                    screen.fill(0xBDBDBD, _rect)

    def draw(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.m[i][j]:
                    _rect = (self.BLOCK_SIZE*(self.x+j), self.BLOCK_SIZE*(self.y+i), self.BLOCK_SIZE+1, self.BLOCK_SIZE+1)
                    screen.fill(TetrisGame.color_dict[self.type], _rect)
                    pygame.gfxdraw.rectangle(screen, _rect, (0, 0, 0, 50))