"""Snake game implementation using Pygame."""

import random
from typing import Tuple

import pygame

# Constants
WIDTH, HEIGHT = 800, 600
INITIAL_FRAMERATE = 5
MAX_FRAMERATE = 20
FONT_SIZE = 36

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Classes
class Snake:
    """Represents the snake in the game."""

    def __init__(self) -> None:
        """Initialize the snake at the center of the screen."""
        self.body: list[Tuple[int, int]] = [(WIDTH // 2, HEIGHT // 2)]
        self.direction: Tuple[int, int] = (0, -1)
        self.size = 20

    def head(self) -> Tuple[int, int]:
        """Return the position of the snake's head."""
        return self.body[0]

    def move(self) -> None:
        """Move the snake one step in the current direction."""
        head_x, head_y = self.head()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * self.size, head_y + dir_y * self.size)
        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """Change snake direction, preventing 180-degree turns."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def is_self_collision(self) -> bool:
        """Check if the snake's head collides with its body."""
        return self.head() in self.body[1:]

    def is_wall_collision(self) -> bool:
        """Check if the snake's head collides with a wall."""
        head_x, head_y = self.head()
        return head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT

    def grow(self) -> None:
        """Grow the snake by one segment."""
        self.body.append(self.body[-1])

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the snake on the given surface."""
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] + 1, segment[1] + 1, self.size - 2, self.size - 2
            )
            pygame.draw.rect(surface, GREEN, rect)


class Food:
    """Represents the food in the game."""

    def __init__(self) -> None:
        """Initialize food at a random position not occupied by the snake."""
        self.position: Tuple[int, int] = (0, 0)
        self.size = 20

    def reset_position(self, snake: Snake) -> None:
        """Place food at a random position not occupied by the snake."""
        while True:
            self.position = (
                random.randint(0, (WIDTH - self.size) // self.size) * self.size,
                random.randint(0, (HEIGHT - self.size) // self.size) * self.size,
            )
            if self.position not in snake.body:
                break

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the food on the given surface."""
        pygame.draw.rect(surface, RED, (*self.position, self.size, self.size))


# Functions
def main() -> None:
    """Main game loop."""
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)

    snake = Snake()
    food = Food()
    food.reset_position(snake)
    score = 0
    framerate = INITIAL_FRAMERATE
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
                elif event.key == pygame.K_r and game_over:
                    snake = Snake()
                    food = Food()
                    food.reset_position(snake)
                    score = 0
                    framerate = INITIAL_FRAMERATE
                    game_over = False

        if not game_over:
            snake.move()

            if snake.is_self_collision() or snake.is_wall_collision():
                game_over = True

            if snake.head() == food.position:
                snake.grow()
                food.reset_position(snake)
                score += 1
                framerate = min(framerate + 1, MAX_FRAMERATE)

        screen.fill(BLACK)

        snake.draw(screen)
        food.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, RED)
            screen.blit(
                game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2),
            )

        pygame.display.flip()

        clock.tick(framerate)

    pygame.quit()


if __name__ == "__main__":
    main()
