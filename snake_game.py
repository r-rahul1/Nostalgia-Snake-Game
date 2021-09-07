import pygame
from pygame.locals import *
import time
import random

size = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 23) * size
        self.y = random.randint(1, 21) * size


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/snake1.png").convert()
        self.length = 1
        self.x = [40] * self.length
        self.y = [40] * self.length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def build(self):

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'right':
            self.x[0] += size
        self.build()


class Game:
    def __init__(self):
        self.speed = 0.25
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake World")
        icon = pygame.image.load('resources/icon.ico')
        pygame.display.set_icon(icon)
        self.surface = pygame.display.set_mode((1000, 900))
        self.pause = False
        self.snake = Snake(self.surface)
        self.snake.build()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.background_music()
        self.walk_sound()

    def walk_sound(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("resources/walk.wav"))
        pygame.mixer.Channel(0).pause()

    def background_music(self):
        pygame.mixer.music.load("resources/background.mp3")
        pygame.mixer.music.play(loops=10)

    def effects(self, sound):
        effect = pygame.mixer.Sound(f"resources/{sound}.wav")
        pygame.mixer.Sound.play(effect)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        pygame.mixer.Channel(0).unpause()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= (x2 + size-1):
            if y1 >= y2 and y1 <= (y2 + size-1):
                return True
        return False

    def render_background(self):
        bgpic = pygame.image.load("resources/bgpic.jpg")
        self.surface.blit(bgpic, (0, 0))
        pygame.display.flip()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.effects("point")
            self.snake.increase_length()
            if self.speed >= 0.75:
                self.speed -= 0.0125
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.effects("over")
                raise "Collided itself"

        # Checking if snake hits boundary
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 900):
            self.effects("over")
            raise "hits the boundary"

    def display_score(self):
        font = pygame.font.SysFont('arial', 45)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 30))

    def show_game_over(self):
        pygame.mixer.music.pause()
        pygame.mixer.Channel(0).pause()
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Game is over! Your score is {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(score, (330, 250))
        replay = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(replay, (250, 450))
        pygame.display.flip()
        time.sleep(2)
        pygame.mixer.music.play()

    def run(self):
        running = True
        pygame.mixer.Channel(0).unpause()
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if not self.pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                    if event.key == K_RETURN:
                        self.pause = False
                elif event.type == QUIT:
                    running = False
            try:
                if not self.pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                self.pause = True
                self.reset()

            time.sleep(self.speed)

    def startup(self):
        self.render_background()
        head = pygame.font.SysFont('arial', 60, bold=True)
        welcome = head.render("Snake World", True, (255, 255, 255))
        self.surface.blit(welcome, (370, 400))
        font = pygame.font.SysFont('arial', 30)
        start = font.render("Press Enter to start the game!", True, (255, 255, 255))
        self.surface.blit(start, (350, 500))
        pygame.display.flip()
        running = True
        pygame.mixer.Channel(0).unpause()
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return True
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == QUIT:
                    running = False
        return False


if __name__ == '__main__':
    #rr
    game = Game()
    if game.startup():
        game.run()
