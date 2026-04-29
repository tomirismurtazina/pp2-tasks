import pygame
import random
import json
import os

SIZE = 800
CELL_SIZE = 40
GRID_WIDTH = SIZE // CELL_SIZE 
GRID_HEIGHT = SIZE // CELL_SIZE
FPS = 60

COLOR_BG = (0, 0, 0)
COLOR_SNAKE_DEFAULT = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_FOOD_1 = (255, 0, 0) 
COLOR_FOOD_2 = (0, 255, 0)
COLOR_FOOD_3 = (255, 255, 0)
COLOR_POISON = (139, 0, 0)
COLOR_WALL = (70, 70, 70)
COLOR_UI_BG = (50, 50, 50)

INITIAL_SPEED = 200
SPEED_INCREMENT = 10
MIN_SPEED = 60
LEVEL_UP_THRESHOLD = 4

FOOD_TIMER = 5000 
POWERUP_TIMER = 8000
POWERUP_EFFECT_DURATION = 5000

FOOD_WEIGHTS = [70, 20, 10]

SETTINGS_FILE = "settings.json"

PWR_SPEED = "SPEED"
PWR_SLOW = "SLOW"
PWR_SHIELD = "SHIELD"

def get_grid_range():
    return (CELL_SIZE // 2, SIZE - CELL_SIZE // 2, CELL_SIZE)

class Game:
    def __init__(self, username, pb):
        self.username = username 
        self.pb = pb
        self.settings = self.load_settings()

        self.score = 0
        self.level = 1
        self.game_over = False 
   
        self.snake_dir = (0, 0)
        self.snake_head = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        self.snake_head.center = (SIZE // 2 + 20, SIZE // 2 + 20)
        self.segments = [self.snake_head.copy()]
        self.length = 1
 
        self.food = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        self.poison = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        self.powerup = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        
        self.obstacles = []
        self.food_weight = 1
        self.powerup_type = None

        self.time_prev = 0
        self.current_step = INITIAL_SPEED
        self.food_spawn_time = pygame.time.get_ticks()
        self.pwr_spawn_time = pygame.time.get_ticks()
        self.pwr_active_until = 0

        self.shield_active = False
        self.pwr_on_field = False
        
        self.spawn_food()
        self.spawn_poison()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {"snake_color": COLOR_SNAKE_DEFAULT, "grid_overlay": True, "sound": True}

    def get_valid_pos(self):
        range_data = get_grid_range()
        while True:
            pos = [random.randrange(*range_data), random.randrange(*range_data)]
            temp_rect = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
            temp_rect.center = pos
            if any(obs.colliderect(temp_rect) for obs in self.obstacles):
                continue
            if any(seg.colliderect(temp_rect) for seg in self.segments):
                continue
            return pos

    def spawn_food(self):
        self.food.center = self.get_valid_pos()
        self.food_weight = random.choices([1, 2, 3], weights=FOOD_WEIGHTS)[0]
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison.center = self.get_valid_pos()

    def spawn_powerup(self):
        if not self.pwr_on_field:
            self.powerup.center = self.get_valid_pos()
            self.powerup_type = random.choice([PWR_SPEED, PWR_SLOW, PWR_SHIELD])
            self.pwr_spawn_time = pygame.time.get_ticks()
            self.pwr_on_field = True

    def handle_level_up(self):
        self.level += 1
        self.current_step = max(MIN_SPEED, INITIAL_SPEED - (self.level * SPEED_INCREMENT))
        
        if self.level >= 3:
            self.obstacles = []
            for _ in range(self.level + 2):
                new_obs = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
                new_obs.center = self.get_valid_pos()
                if not new_obs.colliderect(self.snake_head.inflate(CELL_SIZE*4, CELL_SIZE*4)):
                    self.obstacles.append(new_obs)

    def update(self):
        now = pygame.time.get_ticks()

        if self.pwr_on_field and now - self.pwr_spawn_time > POWERUP_TIMER:
            self.pwr_on_field = False

        if self.pwr_active_until > 0 and now > self.pwr_active_until:
            self.pwr_active_until = 0
            self.current_step = max(MIN_SPEED, INITIAL_SPEED - (self.level * SPEED_INCREMENT))

        if now - self.food_spawn_time > FOOD_TIMER:
            self.spawn_food()

        if now - self.time_prev > self.current_step:
            self.time_prev = now
            if self.snake_dir != (0, 0):
                self.snake_head.move_ip(self.snake_dir)
                self.segments.append(self.snake_head.copy())
                self.segments = self.segments[-self.length:]

        hit_wall = (self.snake_head.left < 0 or self.snake_head.right > SIZE or self.snake_head.top < 0 or self.snake_head.bottom > SIZE)
        hit_obs = any(self.snake_head.colliderect(obs) for obs in self.obstacles)
        hit_self = any(self.snake_head.colliderect(seg) for seg in self.segments[:-1])

        if hit_wall or hit_obs or hit_self:
            if self.shield_active:
                self.shield_active = False 
                if hit_wall:
                    self.snake_head.move_ip([-d for d in self.snake_dir])
            else:
                self.game_over = True

        if self.snake_head.colliderect(self.food):
            self.score += self.food_weight
            self.length += self.food_weight
            if self.score // LEVEL_UP_THRESHOLD >= self.level:
                self.handle_level_up()
            self.spawn_food()
            if random.random() < 0.3: self.spawn_powerup()

        if self.snake_head.colliderect(self.poison):
            self.length -= 2
            if self.length <= 1:
                self.game_over = True
            else:
                self.segments = self.segments[-self.length:]
                self.spawn_poison()

        if self.pwr_on_field and self.snake_head.colliderect(self.powerup):
            self.apply_powerup(self.powerup_type)
            self.pwr_on_field = False

    def apply_powerup(self, ptype):
        now = pygame.time.get_ticks()
        if ptype == PWR_SPEED:
            self.current_step = 60
            self.pwr_active_until = now + POWERUP_EFFECT_DURATION
        elif ptype == PWR_SLOW:
            self.current_step = 350
            self.pwr_active_until = now + POWERUP_EFFECT_DURATION
        elif ptype == PWR_SHIELD:
            self.shield_active = True

    def draw(self, screen, snake_color):
        f_colors = {1: COLOR_FOOD_1, 2: COLOR_FOOD_2, 3: COLOR_FOOD_3}
        pygame.draw.rect(screen, f_colors.get(self.food_weight), self.food)
        pygame.draw.rect(screen, COLOR_POISON, self.poison)
        if self.pwr_on_field:
            p_color = (255, 255, 255)
            if self.powerup_type == PWR_SLOW: p_color = (255, 0, 255) 
            if self.powerup_type == PWR_SHIELD: p_color = (0, 255, 255)
            pygame.draw.ellipse(screen, p_color, self.powerup)

        for obs in self.obstacles:
            pygame.draw.rect(screen, COLOR_WALL, obs)
            
        for i, seg in enumerate(self.segments):
            color = snake_color
            if self.shield_active and i == len(self.segments) - 1:
                color = (0, 255, 255)
            pygame.draw.rect(screen, color, seg)