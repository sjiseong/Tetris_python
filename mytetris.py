import pygame as pg
import sys, random, os

# 게임 실행을 위해 pygame 필요
# cmd, 터미널에 pip install pygame 입력

# 게임 조작
# 방향키 좌, 우 : 현재 블럭을 좌우로 이동
# 방향키 하   : 현재 블럭을 아래로 이동
# 방향키 상   : 현재 블럭을 90도 회전
# 스페이스    : 현재 블럭을 낙하시켜 밑바닥으로 이동
# ESC        : 현재 게임을 종료 (game over 화면으로 이동)

# shapes 는 한 종류의 테트리미노를 90씩 회전시켜 얻을 수있는 모든 모양을 배열로 담는다
# shapes 에 담긴 요소는 인덱스 i 로 접근한다
# rotate() 는 i 를 증가 시켜 테트리미노가 90도 회전한 모양에 접근한다
class Tetrimino:
    def __init__(self, shapes, color):
        self.shapes = shapes
        self.color = color
        self.num = len(shapes)
        self.i = 0

    def get_shape(self):
        return self.shapes[self.i]
    
    def get_rotate(self):
        return self.shapes[(self.i + 1) % self.num]

    def rotate(self):
        self.i = (self.i + 1) % self.num


#color
BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
GRAY = (99, 110, 114)
DARKGRAY = (45, 52, 54)
#   Flat UI Pallete v1 by Flat UI Colors
CONCRETE = (149, 165, 166)
LIGHTGRAY = (127, 140, 141)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
PURPLE = (155, 89, 182)
CARROT = (230, 126, 34)
TURQUOISE = (26, 188, 156)
YELLOW = (241, 196, 15)

colors = [0, BLUE, GREEN, RED, PURPLE, CARROT, TURQUOISE, YELLOW]
board_colors = [DARKGRAY, DARKGRAY]

# 각각의 조각은 네 개의 블럭으로 이루어져 있다.
# 좌측 상단을 기준으로 각 블럭의 좌표를 (y, x) 형태로 저장한다.
# 90도 회전했을 때의 모양도 함께 저장.
tetlist = [
    Tetrimino([
        ((0, 0), (0, 1), (0, 2), (0, 3)),  # ****
        ((0, 0), (1, 0), (2, 0), (3, 0))
    ], 0),
    Tetrimino([
        ((0, 0), (0, 1), (1, 0), (1, 1)),  # **
    ], 1),                                 # **
    Tetrimino([
        ((0, 1), (1, 0), (1, 1), (1, 2)),  # *..
        ((0, 0), (1, 0), (1, 1), (2, 0)),  # ***
        ((0, 0), (0, 1), (0, 2), (1, 1)),
        ((0, 1), (1, 0), (1, 1), (2, 1))
    ], 2),
    Tetrimino([
        ((0, 2), (1, 0), (1, 1), (1, 2)),  # ..*
        ((0, 0), (1, 0), (2, 0), (2, 1)),  # ***
        ((0, 0), (0, 1), (0, 2), (1, 0)),
        ((0, 0), (0, 1), (1, 1), (2, 1))
    ], 3),
    Tetrimino([
        ((0, 0), (1, 0), (1, 1), (1, 2)),  # *..
        ((0, 0), (0, 1), (1, 0), (2, 0)),  # ***
        ((0, 0), (0, 1), (0, 2), (1, 2)),
        ((0, 1), (1, 1), (2, 0), (2, 1))
    ], 4),
    Tetrimino([
        ((0, 1), (0, 2), (1, 0), (1, 1)),  # .**
        ((0, 0), (1, 0), (1, 1), (2, 1)),  # **.
    ], 5),
    Tetrimino([
        ((0, 0), (0, 1), (1, 1), (1, 2)),  # **.
        ((0, 1), (1, 0), (1, 1), (2, 0)),  # .**
    ], 6)
]

# tetlist의 테트리미노들을 CUI 에 프린트하는 함수. 테스트용
def print_tetrimino():
    for tet in tetlist:
        for shape in tet.shapes:
            i = 0
            j = -1
            for y, x in shape:
                if y > i:
                    print('')
                    i = y
                    j = -1
                j += 1
                if x > j:
                    for k in range(x - j):
                        print(' ', end='')
                    j = x
                print('*', end='')
            print('\n')


class TetrisApp():
    
    def __init__(self, block_size, board_width, board_height):
        #pygame
        pg.init()

        #pygame screen size
        self.block_size = block_size
        self.width = board_width
        self.height = board_height
        self.size = [block_size * self.width, block_size * self.height]
        self.screen = pg.display.set_mode(self.size)

        #pygame displayed title
        pg.display.set_caption("My Tetris")

        #text
        font_lg = pg.font.Font(os.path.join(os.path.dirname(sys.argv[0]), 'myfont.ttf'), 32)
        font_md = pg.font.Font(os.path.join(os.path.dirname(sys.argv[0]), 'myfont.ttf'), 14)
        self.text_start = font_lg.render('Game Start', True, WHITE)
        self.text_gameover = font_lg.render('Game Over', True, WHITE)
        self.text_start_info = font_md.render('Press Enter to start', True, LIGHTGRAY)
        self.text_gameover_info = font_md.render('Press Enter to restart', True, LIGHTGRAY)
        self.text_control_info = font_md.render('control : arrows, space', True, WHITE)
        
        #Loop until the user clicks the close button.
        self.quit_game = False
        self.done = False
        self.clock = pg.time.Clock()

        #game init
        self.board = [[0] * self.width for row in range(self.height)]
        self.block_pos = [0, 0] #[y, x]
        self.block_type = 0     #1 ~ 7
        self.pressing = 0
        self.lastpressed = 0

        self.set_new_block()

    #draw on pygame
    def draw_board(self, board):
        for y in range(self.height):
            for x in range(self.width):
                if board[y][x] == 0:
                    pg.draw.rect(self.screen, board_colors[(y + x) % 2], [x * self.block_size, y * self.block_size, self.block_size, self.block_size])
                else:
                    pg.draw.rect(self.screen, colors[board[y][x]], [x * self.block_size, y * self.block_size, self.block_size, self.block_size])
                pg.draw.rect(self.screen, board_colors[1], [x * self.block_size, y * self.block_size, self.block_size, self.block_size], 1)
    
    def draw_block(self, pos):
        for y, x in tetlist[self.block_type - 1].get_shape():
            pg.draw.rect(self.screen, colors[self.block_type], [
                    (pos[1] + x) * self.block_size, (pos[0] + y) * self.block_size, self.block_size, self.block_size])
            pg.draw.rect(self.screen, board_colors[1], [(pos[1] + x) * self.block_size, (pos[0] + y) * self.block_size, self.block_size, self.block_size], 1)
   
    #game algorithm
    def set_new_block(self):
        tetlist[self.block_type - 1].i = 0
        self.block_type = random.randint(1, 7)
        x = int(self.width / 2 - 2)
        if self.block_type == 1:
            self.block_pos = [0, x]
        elif self.block_type == 2:
            self.block_pos = [0, x + 1]
        else:
            self.block_pos = [0, x + self.width % 2]

    def check_collision(self, block_y, block_x, shape):
        if block_x < 0:
            return True
        for y, x in shape:
            if block_y + y >= self.height or block_x + x >= self.width or self.board[block_y + y][block_x + x] != 0:
                return True
        return False
 
    def check_stack(self):
        for y, x in tetlist[self.block_type - 1].get_shape():
            if self.block_pos[0] + y == self.height - 1 or self.board[self.block_pos[0] + y + 1][self.block_pos[1] + x] != 0:
                break
        else:
            return False
        #stack block
        for y, x in tetlist[self.block_type - 1].get_shape():
            self.board[self.block_pos[0] + y][self.block_pos[1] + x] = self.block_type
        #boom
        for y in range(self.block_pos[0], self.block_pos[0] + 4):
            if y >= self.height:
                break
            for x in range(self.width):
                if self.board[y][x] == 0:
                    break
            else:
                del(self.board[y])
                self.board.insert(0, [0] * self.width)
        self.set_new_block()
        if self.check_collision(self.block_pos[0], self.block_pos[1], tetlist[self.block_type - 1].get_shape()):
            self.gameover()
        return True

    def move(self, distance):
        if not self.check_collision(self.block_pos[0], self.block_pos[1] + distance, tetlist[self.block_type - 1].get_shape()):
            self.block_pos[1] += distance

    def down(self):
        if not self.check_collision(self.block_pos[0] + 1, self.block_pos[1], tetlist[self.block_type - 1].get_shape()):
            self.block_pos[0] += 1
    
    def rotate(self):
        if not self.check_collision(self.block_pos[0], self.block_pos[1], tetlist[self.block_type - 1].get_rotate()):
            tetlist[self.block_type - 1].rotate()

    def dropdown(self):
        while not self.check_stack():
            self.block_pos[0] += 1

    def gameover(self):
        self.done = True
        pg.time.set_timer(pg.USEREVENT + 1, 0)

    def run(self):
        self.screen.blit(self.text_start, ((self.width * self.block_size - self.text_start.get_width()) / 2,
            (self.height * self.block_size - self.text_start.get_height()) / 2 * 9 / 10))
        self.screen.blit(self.text_start_info, ((self.width * self.block_size - self.text_start_info.get_width()) / 2,
            (self.height * self.block_size - self.text_start_info.get_height()) / 2 * 9 / 10 + 50))
        self.screen.blit(self.text_control_info, ((self.width * self.block_size - self.text_control_info.get_width()) / 2,
            (self.height * self.block_size - self.text_control_info.get_height()) / 2 * 9 / 10 + 150))
        pg.display.update()
        while not self.quit_game:
            self.clock.tick(20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.done = False
                        self.run_game()
                        self.screen.fill(BLACK)
                        self.screen.blit(self.text_gameover, ((self.width * self.block_size - self.text_gameover.get_width()) / 2,
                            (self.height * self.block_size - self.text_gameover.get_height()) / 2 * 9 / 10))
                        self.screen.blit(self.text_gameover_info, ((self.width * self.block_size - self.text_gameover_info.get_width()) / 2,
                            (self.height * self.block_size - self.text_gameover_info.get_height()) / 2 * 9 / 10 + 50))
                        pg.display.update()
                        # 게임 초기화
                        self.board = [[0] * self.width for row in range(self.height)]
                        self.set_new_block()

    def run_game(self):
        #set timer
        # 1초에 한번씩 유저이벤트를 발생시킨다.
        pg.time.set_timer(pg.USEREVENT + 1, 1000)
        while not self.done:
            #set delay
            self.clock.tick(20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                    self.quit_game = True
                # 유저 이벤트 발생시 현재 낙하중인 블럭을 한 칸 낙하시키고 밑바닥에 도달했는지 확인. 
                elif event.type == pg.USEREVENT + 1:
                    self.down()
                    self.check_stack()
                elif event.type == pg.KEYDOWN:
                    self.pressing = 0
                    self.lastpressed = event.key
                    if event.key == pg.K_ESCAPE:
                        self.done = True
                    elif event.key == pg.K_LEFT:
                        self.move(-1)
                    elif event.key == pg.K_RIGHT:
                        self.move(1)
                    elif event.key == pg.K_DOWN:
                        self.down()
                    elif event.key == pg.K_UP:
                        self.rotate()
                    elif event.key == pg.K_SPACE:
                        self.dropdown()
            # 키보드의 특정 버튼을 계속 누르고 있을 때 수행
            keys = pg.key.get_pressed()
            if self.pressing < 6:
                    self.pressing += 1
            elif keys[self.lastpressed]:
                if self.lastpressed == pg.K_LEFT:
                      self.move(-1)
                elif self.lastpressed == pg.K_RIGHT:
                    self.move(1)
                elif self.lastpressed == pg.K_DOWN:
                    self.down()
                elif self.lastpressed == pg.K_UP:
                    self.rotate()
            # 화면 업데이트
            self.draw_board(self.board)
            self.draw_block(self.block_pos)
            pg.display.update()
        # 현재 진행중인 게임이 종료되면 유저이벤트를 발생시키지 않는다
        pg.time.set_timer(pg.USEREVENT + 1, 0)

if __name__ == '__main__':
    # 게임판 크기 설정 가능 (한 칸의 크기, 가로 칸 수, 세로 칸 수)
    app = TetrisApp(30, 10, 20)
    app.run()