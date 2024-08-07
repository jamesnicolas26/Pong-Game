import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5
INITIAL_BALL_SPEED = 3  # Slower initial serve speed
SCORE_FONT_SIZE = 50
BANNER_FONT_SIZE = 80
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
BANNER_COLOR = (0, 0, 255)
SCORE_LIMIT = 5

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Fonts
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
banner_font = pygame.font.Font(None, BANNER_FONT_SIZE)
start_font = pygame.font.Font(None, 70)

# Classes
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, up, down):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if down and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, PADDLE_COLOR, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = random.choice([-1, 1]) * INITIAL_BALL_SPEED
        self.speed_y = random.choice([-1, 1]) * INITIAL_BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.ellipse(surface, BALL_COLOR, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = random.choice([-1, 1]) * INITIAL_BALL_SPEED
        self.speed_y = random.choice([-1, 1]) * INITIAL_BALL_SPEED

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main():
    clock = pygame.time.Clock()

    # Paddles
    paddle1 = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

    # Ball
    ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

    # Scores
    score1 = 0
    score2 = 0

    game_active = False
    paused = False
    game_over = False
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Restart the game
                        score1 = 0
                        score2 = 0
                        ball.reset()
                        game_over = False
                        game_active = True
                        winner = None
                    else:
                        game_active = not game_active
                        if not game_active:
                            ball.reset()
                elif event.key == pygame.K_p:
                    paused = not paused

        # Movement
        keys = pygame.key.get_pressed()
        paddle1.move(keys[pygame.K_w], keys[pygame.K_s])
        paddle2.move(keys[pygame.K_UP], keys[pygame.K_DOWN])

        if game_active and not paused:
            # Update ball
            ball.update()

            # Ball collision with paddles
            if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
                ball.speed_x *= -1.1  # Increase speed on paddle hit

            # Ball out of bounds
            if ball.rect.left <= 0:
                score2 += 1
                if score2 >= SCORE_LIMIT:
                    game_over = True
                    winner = "Player 2 Wins!"
                else:
                    ball.reset()
            if ball.rect.right >= SCREEN_WIDTH:
                score1 += 1
                if score1 >= SCORE_LIMIT:
                    game_over = True
                    winner = "Player 1 Wins!"
                else:
                    ball.reset()

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        paddle1.draw(screen)
        paddle2.draw(screen)
        ball.draw(screen)

        # Display scores
        draw_text(f"{score1}", score_font, TEXT_COLOR, screen, SCREEN_WIDTH // 4, 50)
        draw_text(f"{score2}", score_font, TEXT_COLOR, screen, SCREEN_WIDTH * 3 // 4, 50)

        # Display start screen
        if not game_active:
            if not game_over:
                draw_text("Press SPACE to Start", start_font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            else:
                # Victory Banner
                pygame.draw.rect(screen, BANNER_COLOR, (50, SCREEN_HEIGHT // 2 - 100, SCREEN_WIDTH - 100, 200))
                draw_text(winner, banner_font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                draw_text("Press SPACE to Restart", start_font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)

        # Display pause message
        if paused and game_active:
            draw_text("Paused", start_font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
