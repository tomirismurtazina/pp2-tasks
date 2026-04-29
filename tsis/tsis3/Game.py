#Imports
import pygame, sys
from pygame.locals import *
import random, time
import persistence as p
import ui

#Initialzing 
pygame.init()

running = True

#Setting up FPS 
FPS = 60
clock = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
screen = pygame.display.set_mode((400,600))
screen.fill(WHITE)
pygame.display.set_caption("Game")



class Enemy(pygame.sprite.Sprite):
      def __init__(self, speed):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)
        self.speed = speed

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.color = color
        self.speed = 5
        self.shielded = False
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.weight = random.randint(1, 3)

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
   
class Powerup(pygame.sprite.Sprite):
    def __init__(self, type):
                super().__init__()
                self.type = type 
                self.image = pygame.Surface((30, 30))
                colors = {"Nitro": (0, 0, 255), "Shield": (0, 255, 255), "Repair": (255, 255, 0)}
                self.image.fill(colors.get(type, (255, 255, 255)))
                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)

    def update(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (139, 69, 19), (0, 0, 50, 20))
        pygame.draw.ellipse(self.image, (100, 50, 15), (5, 5, 40, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def update(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
    

class Game:
    def __init__(self):
        self.settings = p.get_settings()
        self.state = "MENU"
        self.username = "Player"
        self.reset_game()

    def reset_game(self):
        self.coins_count = 0
        self.distance = 0
        base_speed = {"Easy": 3, "Medium": 5, "Hard": 8}
        self.game_speed = base_speed.get(self.settings.get("difficulty"), 5)
        
        self.player = Player(self.settings["car_color"])
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.active_powerup = None
        self.powerup_timer = 0
        self.shield_timer = 0

    def run(self):
        while True:
            if self.state == "MENU":
                self.main_menu()
            elif self.state == "GAME":
                self.play_game()
            elif self.state == "LEADERBOARD":
                self.show_leaderboard()
            elif self.state == "GAME_OVER":
                self.game_over_screen()

    def main_menu(self):
        screen.fill(WHITE)
        ui.draw_text(screen, "Racer", 40, SCREEN_WIDTH//2, 100, RED, True)
        
        btn_play = ui.Button("PLAY", 125, 200, 150, 50, GREEN)
        btn_lead = ui.Button("SCORES", 125, 270, 150, 50, GRAY)
        btn_quit = ui.Button("QUIT", 125, 340, 150, 50, BLACK)
        
        ui.draw_text(screen, f"Name: {self.username}", 20, SCREEN_WIDTH//2, 180, BLACK, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_play.is_clicked(pos): 
                    self.reset_game()
                    self.state = "GAME"
                if btn_lead.is_clicked(pos): 
                    self.state = "LEADERBOARD"
                if btn_quit.is_clicked(pos): 
                    pygame.quit()
                    sys.exit()

        for b in [btn_play, btn_lead, btn_quit]: 
            b.draw(screen, pygame.font.SysFont("Verdana", 20))
        pygame.display.update()

    def play_game(self):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        self.distance += 0.1
        self.game_speed += 0.001 
        
        if self.player.shielded:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_timer > 5000:
                self.player.shielded = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if random.randint(1, 60) == 1 and len(self.enemies) < 4:
            e = Enemy(self.game_speed)
            self.enemies.add(e)
            self.all_sprites.add(e)
  
        if random.randint(1, 150) == 1:
            c = Coin()
            self.coins.add(c)
            self.all_sprites.add(c)

        if random.randint(1, 300) == 1:
            po = Powerup(random.choice(["Nitro", "Shield", "Repair"]))
            self.powerups.add(po)
            self.all_sprites.add(po)

        if random.randint(1, 300) == 1 and len(self.hazards)<2:
            h = Hazard()
            self.hazards.add(h)
            self.all_sprites.add(h)

        self.player.move()
        self.enemies.update()
        self.coins.update()
        self.powerups.update()
        self.hazards.update()
        for e in self.enemies:
            e.move()

        coins_collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coins_collected:
            for c in coins_collected:
                self.coins_count += c.weight

        powerups_collected = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for po in powerups_collected:
            if po.type == "Nitro":
                self.game_speed += 3 
            elif po.type == "Shield":
                self.player.shielded = True
                self.shield_timer = pygame.time.get_ticks()
            elif po.type == "Repair":
                for h in self.hazards:
                    h.kill()

        enemies_hit = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemies_hit:
            pygame.mixer.Sound("crash.wav").play()
            if self.player.shielded:
                self.player.shielded = False
                for e in enemies_hit:
                    e.kill()
            else:
                p.save_score(self.username, SCORE, int(self.distance))
                self.state = "GAME_OVER"
                return

        for entity in self.all_sprites:
            screen.blit(entity.image, entity.rect)
 
        ui.draw_text(screen, f"SCORE: {SCORE}", 20, 10, 10, BLACK)
        ui.draw_text(screen, f"COINS: {self.coins_count}", 18, 10, 40, (180, 150, 0))
        ui.draw_text(screen, f"SPEED: {int(self.game_speed)}", 18, 10, 70, BLACK)
        
        if self.player.shielded:
            ui.draw_text(screen, "SHIELD ACTIVE!", 18, SCREEN_WIDTH//2, 20, (0, 255, 255), True)
        
        pygame.display.update()
        clock.tick(FPS)

    def game_over_screen(self):
        screen.fill(RED)
        ui.draw_text(screen, "CRASHED!", 40, SCREEN_WIDTH//2, 150, WHITE, True)
        ui.draw_text(screen, f"Final Score: {SCORE}", 25, SCREEN_WIDTH//2, 220, WHITE, True)
        ui.draw_text(screen, f"Coins Collected: {self.coins_count}", 20, SCREEN_WIDTH//2, 260, WHITE, True)
        ui.draw_text(screen, f"Distance: {int(self.distance)}m", 20, SCREEN_WIDTH//2, 300, WHITE, True)
        
        btn_retry = ui.Button("RETRY", 125, 350, 150, 50, BLACK)
        btn_menu = ui.Button("MENU", 125, 420, 150, 50, GRAY)
        
        btn_scores = ui.Button("SCORES", 125, 490, 150, 50, (100, 100, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_retry.is_clicked(pos): 
                    self.reset_game()
                    self.state = "GAME"
                if btn_menu.is_clicked(pos): 
                    self.state = "MENU"
                if btn_scores.is_clicked(pos):
                    self.state = "LEADERBOARD"

        btn_retry.draw(screen, pygame.font.SysFont("Verdana", 18))
        btn_menu.draw(screen, pygame.font.SysFont("Verdana", 18))
        btn_scores.draw(screen, pygame.font.SysFont("Verdana", 18))
        pygame.display.update()

    def show_leaderboard(self):
        screen.fill(WHITE)
        ui.draw_text(screen, "TOP SCORES", 30, SCREEN_WIDTH//2, 50, BLACK, True)
        
        scores = p.get_leaderboard()
        
        if not scores:
            ui.draw_text(screen, "No scores yet!", 20, SCREEN_WIDTH//2, 150, GRAY, True)
        else:
            ui.draw_text(screen, "Rank", 18, 50, 100, BLACK)
            ui.draw_text(screen, "Name", 18, 150, 100, BLACK)
            ui.draw_text(screen, "Score", 18, 250, 100, BLACK)
            ui.draw_text(screen, "Distance", 18, 330, 100, BLACK)
            
            for i, entry in enumerate(scores[:10]): 
                y_pos = 150 + i * 35
                ui.draw_text(screen, f"{i+1}", 18, 50, y_pos, BLACK)
                ui.draw_text(screen, entry["name"][:10], 18, 150, y_pos, BLACK)
                ui.draw_text(screen, str(entry["score"]), 18, 250, y_pos, BLACK)
                ui.draw_text(screen, str(entry.get("distance", 0)), 18, 330, y_pos, BLACK)
        
        btn_back = ui.Button("BACK", 125, 500, 150, 50, BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.is_clicked(pygame.mouse.get_pos()):
                    self.state = "MENU"
        
        btn_back.draw(screen, pygame.font.SysFont("Verdana", 18))
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()