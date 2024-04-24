from decouple import config
import pygame

#
pygame.init()
#
WIDTH, HEIGHT = int(config('WIDTH')), int(config('HEIGHT'))
PADDLE_WIDTH, PADDLE_HEIGHT = int(config('PADDLE_WIDTH')), int(config('PADDLE_HEIGHT'))
FPS = int(config('FPS')) #
WHITE = tuple(map(int, config('WHITE').split(', ')))
BLACK = tuple(map(int, config('BLACK').split(', ')))
#
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win: pygame.Surface) -> None:
        """"""
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

def draw(win: pygame.Surface, paddles: Paddle):
    """"""
    #
    win.fill(BLACK)
    #
    for paddle in paddles:
        paddle.draw(win)
    #
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    pygame.display.update()

def check_paddle_boundry(paddle, direction):
    """"""
    if direction == 'up':
        return paddle.y - paddle.VEL >= 2
    elif direction == 'down':
        return paddle.y + paddle.height + paddle.VEL <= HEIGHT - 2
    else:
        raise Exception("Wron direction! Only 'up' or 'down'")

def handle_paddle_movement(keys, left_paddle, right_paddle):
    """"""
    if keys[pygame.K_w] and check_paddle_boundry(left_paddle, 'up'):
        left_paddle.move(up=True)
    if keys[pygame.K_s] and check_paddle_boundry(left_paddle, 'down'):
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and check_paddle_boundry(right_paddle, 'up'):
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and check_paddle_boundry(right_paddle, 'down'):
        right_paddle.move(up=False)

def main() -> None:
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        #
        clock.tick(FPS)
        draw(WIN, (left_paddle, right_paddle))
        #    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

    pygame.quit()

if __name__ == '__main__':
    main()
