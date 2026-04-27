import pygame
import random
import sys

pygame.init() #initializing

#color pallete
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

CELL = 30

counter=0
level=1

font = pygame.font.SysFont("Verdana", 20)

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            global level
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # checks the right border
        if self.body[0].x > WIDTH // CELL - 1:
            pygame.quit()
        # checks the left border
        if self.body[0].x < 0:
            pygame.quit()
        # checks the bottom border
        if self.body[0].y > HEIGHT // CELL - 1:
            pygame.quit()
        # checks the top border
        if self.body[0].y < 0:
            pygame.quit()


    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            global counter
            global level
            global FPS
            counter+=food.weight
            print("Got food!")
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos()
            if counter%4 == 0:
                print("Level up!")
                level+=1
                FPS+=5

class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.randint(1, 3)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self):
        self.pos.x = random.randint(0, WIDTH // CELL - 1)
        self.pos.y = random.randint(0, HEIGHT // CELL - 1)


FPS = 5
clock = pygame.time.Clock()

snake = Snake()
food = Food()
food_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(food_spawn, 10000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == food_spawn:
            food = Food()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)

    draw_grid()

    snake.move()
    snake.check_collision(food)

    snake.draw()
    food.draw()

    score=font.render(str(counter), True, colorWHITE)
    leveldisplay=font.render(str(level), True, colorWHITE)
    screen.blit(score, (10, 10)) #displays score
    screen.blit(leveldisplay, (10, 30)) #displays level

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()