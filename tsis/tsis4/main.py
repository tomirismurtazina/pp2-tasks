import pygame
import sys
import json
import os
from db import *
from game import *

SETTINGS_FILE = "settings.json"

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("Snake game")
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont("comicsansms", 40)
        self.font_small = pygame.font.SysFont("comicsansms", 20)
        self.settings = self.load_settings()

        self.state = "MENU" 
        self.username = ""
        self.personal_best = 0
        self.game = None
    
        create_table()

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def load_settings(self):
        defaults = {
            "snake_color": [0, 255, 0], 
            "grid_overlay": True,
            "sound": True
        }
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return defaults
    
    def text(self, text, pos, font=None, color=COLOR_TEXT, center=False):
        if font is None: font = self.font_main
        img = font.render(text, True, color)
        rect = img.get_rect(topleft=pos)
        if center: rect.center = pos
        self.screen.blit(img, rect)

    def menu_screen(self):
        self.screen.fill(COLOR_BG)
        self.text("Snake", (SIZE//2, 150), center=True)
        self.text(f"Player: {self.username}", (SIZE//2, 250), self.font_small, center=True)
        self.text("Press ENTER to Play", (SIZE//2, 400), self.font_small, center=True)
        self.text("L: Leaderboard | S: Settings | Q: Quit", (SIZE//2, 450), self.font_small, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username:
                    self.personal_best = pb(self.username)
                    self.game = Game(self.username, self.personal_best)
                    self.state = "GAME"
                if event.key == pygame.K_l: self.state = "LEADERBOARD"
                if event.key == pygame.K_s: self.state = "SETTINGS"
                if event.key == pygame.K_q: pygame.quit(); sys.exit()
                if event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                elif len(self.username) < 10 and event.unicode.isalnum():
                    self.username += event.unicode

    def settings_screen(self):
        self.screen.fill(COLOR_BG)
        self.text("SETTINGS", (SIZE//2, 100), center=True)

        grid_txt = "ON" if self.settings["grid_overlay"] else "OFF"
        sound_txt = "ON" if self.settings["sound"] else "OFF"
        color_rgb = self.settings["snake_color"]

        self.text(f"[1] Grid Overlay: {grid_txt}", (SIZE//2, 250), self.font_small, center=True)
        self.text(f"[2] Sound: {sound_txt}", (SIZE//2, 300), self.font_small, center=True)
        self.text(f"[3] Snake Color: {color_rgb}", (SIZE//2, 350), self.font_small, center=True)
        
        self.text("Press ESC to Save and Return", (SIZE//2, 600), self.font_small, center=True, color=(150, 150, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                
                if event.key == pygame.K_2:
                    self.settings["sound"] = not self.settings["sound"]
                
                if event.key == pygame.K_3:
                    color_palette = [[0, 255, 0], [0, 0, 255], [255, 0, 0]]
                    current_idx = color_palette.index(color_rgb) if color_rgb in color_palette else 0
                    self.settings["snake_color"] = color_palette[(current_idx + 1) % len(color_palette)]
                
                if event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    self.state = "MENU"

    def leaderboard_screen(self):
        self.screen.fill(COLOR_BG)
        self.text("TOP 10 SCORES", (SIZE//2, 80), center=True)
        
        data = leaderboard()
        y_offset = 180
        header = f"{'User':<12} {'Score':<8} {'Lvl':<5} {'Date'}"
        self.text(header, (100, 150), self.font_small, (200, 200, 0))

        for row in data:
            date_str = row[3].strftime("%Y-%m-%d")
            entry = f"{row[0]:<12} {row[1]:<8} {row[2]:<5} {date_str}"
            self.text(entry, (100, y_offset), self.font_small)
            y_offset += 35

        self.text("Press ESC for Menu", (SIZE//2, 700), self.font_small, center=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "MENU"

    def game_over_screen(self):
        self.screen.fill((255, 0, 0))
        self.text("GAME OVER", (SIZE//2, 200), center=True)
        self.text(f"Score: {self.game.score}", (SIZE//2, 300), self.font_small, center=True)
        
        self.text("Press ENTER to Save to Leaderboard", (SIZE//2, 500), self.font_small, center=True)
        self.text("Press ESC to Discard", (SIZE//2, 550), self.font_small, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(f"Attempting to save: {self.username}, {self.game.score}")
                    result(self.username, self.game.score, self.game.level)
                    self.state = "LEADERBOARD"
                    
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

    def run(self):
        while True:
            if self.state == "MENU":
                self.menu_screen()
            elif self.state == "LEADERBOARD":
                self.leaderboard_screen()
            elif self.state == "SETTINGS":
                self.settings_screen()
            elif self.state == "GAME":
                self.play_game()
            elif self.state == "GAME_OVER":
                self.game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def play_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.game.snake_dir != (0, CELL_SIZE):
                    self.game.snake_dir = (0, -CELL_SIZE)
                if event.key == pygame.K_DOWN and self.game.snake_dir != (0, -CELL_SIZE):
                    self.game.snake_dir = (0, CELL_SIZE)
                if event.key == pygame.K_LEFT and self.game.snake_dir != (CELL_SIZE, 0):
                    self.game.snake_dir = (-CELL_SIZE, 0)
                if event.key == pygame.K_RIGHT and self.game.snake_dir != (-CELL_SIZE, 0):
                    self.game.snake_dir = (CELL_SIZE, 0)

        self.game.update()
        if self.game.game_over:
            self.state = "GAME_OVER"

        self.screen.fill(COLOR_BG)
        
        if self.settings["grid_overlay"]:
            for x in range(0, SIZE, CELL_SIZE):
                pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, SIZE))
            for y in range(0, SIZE, CELL_SIZE):
                pygame.draw.line(self.screen, (0, 0, 0), (0, y), (SIZE, y))

        self.game.draw(self.screen, self.settings['snake_color'])
        
        self.text(f"Score: {self.game.score} | Lvl: {self.game.level}", (10, 10), self.font_small)
        self.text(f"PB: {self.personal_best}", (SIZE - 100, 10), self.font_small)

if __name__ == "__main__":
    app = App()
    app.run()