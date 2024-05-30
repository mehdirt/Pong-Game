from decouple import config
import pygame

# Initialize Pygame
pygame.init()
# Set the game's variables
WIDTH, HEIGHT = int(config('WIDTH')), int(config('HEIGHT'))
PADDLE_WIDTH, PADDLE_HEIGHT = int(config('PADDLE_WIDTH')), int(config('PADDLE_HEIGHT'))
BALL_RADIUS = int(config('BALL_RADIUS'))
FPS = int(config('FPS')) #
WHITE = tuple(map(int, config('WHITE').split(', ')))
BLACK = tuple(map(int, config('BLACK').split(', ')))
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = int(config("WINNING_SCORE"))

# Set up the game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win: pygame.Surface) -> None:
        """Draw the a rectangle (paddle) on the given pygame window."""
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        """Move the paddle on the y-axis. Paddle goes up if up equals True and down if False."""
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        """Resets the paddle's properties after each score."""
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 7
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win) :
        """Draw the a circle (ball) on the given pygame window."""
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        """Movement of the ball affected by 'x_vel' and 'y-vel' instance attributes."""
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        """Resets the ball's properties after each score."""
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win: pygame.Surface, paddles: Paddle, ball, left_score: int, right_score: int) -> None:
    """Draw and update the components of the game."""
    
    # Set the background color
    win.fill(BLACK)
    
    # Draw the scores
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)

    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    # Draw the paddles
    for paddle in paddles:
        paddle.draw(win)
    
    # Draw dashed line
    j = 0
    for i in range(10, HEIGHT, HEIGHT//20):
        if j % 2 == 1:
            j+=1
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        j+=1
    
    # Draw the ball
    ball.draw(win)

    # Update display screen
    pygame.display.update()

def check_paddle_boundry(paddle: Paddle, direction: str) -> None:
    """Cheack if the paddels reached the boundries"""

    if direction == 'up':
        return paddle.y - paddle.VEL >= 2
    elif direction == 'down':
        return paddle.y + paddle.height + paddle.VEL <= HEIGHT - 2
    else:
        raise Exception("Wrong direction! Only 'up' or 'down'")

def handle_paddle_movement(keys, left_paddle: Paddle, right_paddle: Paddle) -> None:
    """Move the paddles according to the entered keys."""
    
    if keys[pygame.K_w] and check_paddle_boundry(left_paddle, 'up'):
        left_paddle.move(up=True)
    elif keys[pygame.K_s] and check_paddle_boundry(left_paddle, 'down'):
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and check_paddle_boundry(right_paddle, 'up'):
        right_paddle.move(up=True)
    elif keys[pygame.K_DOWN] and check_paddle_boundry(right_paddle, 'down'):
        right_paddle.move(up=False)

def handle_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> None:
    """Handle collisions between the ball and other components."""

    # Handling ceiling collision
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Handeling paddle collision
    if ball.x_vel < 0:
        # Left paddle
        # Check if the ball is in the paddle vertical range
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: 
            # Change horizental direction if the ball crashed to the paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:  
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = ball.y - middle_y
                # Reduction factor
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel

    else:
        # Right paddle
        # Check if the ball is in the paddle vertical range
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height: # Check if the ball is in the paddle vertical range
            if ball.x + ball.radius >= right_paddle.x: 
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = ball.y - middle_y
                # Reduction factor
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel

def handle_scores(ball: Ball, left_paddle: Paddle, right_paddle: Paddle, left_score: int, right_score: int) -> tuple[int]:
    """Handles Score mechanism for both paddles."""
    if ball.x < 0:
        right_score += 1
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
    
    elif ball.x > WIDTH:
        left_score += 1
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
    
    won = False
    if left_score >= WINNING_SCORE:
        won = True
        win_text = "Left Player Won!"
    elif right_score >= WINNING_SCORE:
        won = True
        win_text = "Right Player Won!"
    
    if won:
        # Show a winning text
        text = SCORE_FONT.render(win_text, 1, WHITE)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(5000)
        
        # Reset the components 
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
        left_score, right_score = 0, 0
   

    return left_score, right_score


def main() -> None:
    
    run = True
    # Create a clock to track time
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT //
                          2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                           2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # Initializing scores
    left_score, right_score = 0, 0
    
    while run:
        
        clock.tick(FPS)
        draw(WIN, (left_paddle, right_paddle), ball, left_score, right_score)
        
        # Check for quitting from the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
       
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        
        left_score, right_score = handle_scores(ball, left_paddle, right_paddle, left_score, right_score)


    pygame.quit()

if __name__ == '__main__':
    main()
