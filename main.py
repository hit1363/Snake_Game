import pygame
import random
import sys

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.paused = False

        self.snake = [(200, 200), (190, 200), (180, 200)]  # Center the snake on the screen
        self.snake_direction = "RIGHT"
        self.food = self.create_food()
        self.bonus_food = None
        self.food_counter = 0

        self.game_speed = 10  # Speed of the game (in frames per second)
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 24)

    def create_food(self):
        while True:
            food = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)
            if food not in self.snake:
                break
        return food

    def create_bonus_food(self):
        while True:
            bonus_food = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)
            if bonus_food not in self.snake and bonus_food != self.food:
                break
        return bonus_food

    def change_direction(self, event):
        if event.key == pygame.K_SPACE:
            self.paused = not self.paused
            return

        all_directions = {
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT"
        }
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if event.key in all_directions and opposite_directions[all_directions[event.key]] != self.snake_direction:
            self.snake_direction = all_directions[event.key]

    def update_snake(self):
        if self.game_running and not self.paused:
            head_x, head_y = self.snake[0]

            if self.snake_direction == "UP":
                new_head = (head_x, head_y - 10)
            elif self.snake_direction == "DOWN":
                new_head = (head_x, head_y + 10)
            elif self.snake_direction == "LEFT":
                new_head = (head_x - 10, head_y)
            else:
                new_head = (head_x + 10, head_y)

            self.snake = [new_head] + self.snake[:-1]

            # Check if snake hits wall or itself
            if (new_head[0] < 0 or new_head[0] >= 400 or
                new_head[1] < 0 or new_head[1] >= 400 or
                new_head in self.snake[1:]):
                self.game_running = False
                self.show_game_over()
                return

            # Check if snake eats the food
            if new_head == self.food:
                self.snake.append(self.snake[-1])  # Grow the snake
                self.food = self.create_food()
                self.score += 10
                self.food_counter += 1

                # Check if it's time to create bonus food
                if self.food_counter == 5:
                    self.bonus_food = self.create_bonus_food()
                    self.food_counter = 0

            # Check if snake eats the bonus food
            if self.bonus_food and new_head == self.bonus_food:
                self.snake.append(self.snake[-1])  # Grow the snake
                self.bonus_food = None
                self.score += 100

            self.redraw()

    def redraw(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (segment[0], segment[1], 10, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.food[0], self.food[1], 10, 10))
        if self.bonus_food:
            pygame.draw.rect(self.screen, (0, 0, 255), (self.bonus_food[0], self.bonus_food[1], 10, 10))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def draw_button(self, text, position):
        button_font = pygame.font.SysFont("Arial", 24)
        button_text = button_font.render(text, True, (255, 255, 255))
        button_rect = button_text.get_rect(center=position)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect.inflate(20, 10))
        self.screen.blit(button_text, button_rect)
        return button_rect

    def show_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(game_over_text, (100, 180))

        restart_button = self.draw_button("Restart", (200, 240))
        exit_button = self.draw_button("Exit", (200, 300))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.__init__()  # Restart the game
                        self.run()
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.clock.tick(10)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.change_direction(event)

            self.update_snake()
            self.clock.tick(self.game_speed)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()