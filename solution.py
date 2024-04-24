from decouple import config
import pygame

#
pygame.init()
#
WIDTH = int(config('WIDTH'))
HEIGHT = int(config('HEIGHT'))
FPS = int(config('FPS')) #
WHITE = tuple(map(int, config('WHITE').split(', ')))
BLACK = tuple(map(int, config('BLACK').split(', ')))
#
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


def draw(win: pygame.Surface):
    """"""
    win.fill(WHITE)
    pygame.display.update()


def main() -> None:
    run = True
    clock = pygame.time.Clock()

    while run:
        #
        clock.tick(FPS)
        draw(WIN)
        #    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()

if __name__ == '__main__':
    main()
