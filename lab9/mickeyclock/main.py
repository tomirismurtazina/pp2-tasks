import pygame
from datetime import datetime
pygame.init()
screen=pygame.display.set_mode((1200, 900))

running=True
clock=pygame.time.Clock()
image=pygame.image.load("mickeyclock.jpeg")

class clockcl:
	def __init__(self, size, position, width, height):
		self.size = size
		self.position = position
		self.rotation_surface = pygame.Surface((width, height), pygame.SRCALPHA)
		self.minute = 0
		self.second = 0

	def update(self):
		now = datetime.now()
		self.minute = now.minute
		self.second = now.second

	def draw(self, screen):
		self.draw_minute_hand(screen, self.minute)
		self.draw_second_hand(screen, self.second)


	def draw_minute_hand(self, screen, minute):
		self.draw_hand(screen, 10, 250, 6*minute, (0, 0, 0))

	def draw_hand(self, screen, hand_width, hand_length, angle, color):
		rect_x = self.position[0] - hand_width // 2
		rect_y = self.position[1] - hand_length

		self.rotation_surface.fill((0, 0, 0, 0))
		pygame.draw.rect(self.rotation_surface, color, (rect_x, rect_y, hand_width, hand_length))
		rotated_surface = pygame.transform.rotate(self.rotation_surface, -angle)
		rotated_rect = rotated_surface.get_rect(center = self.position)
		screen.blit(rotated_surface, rotated_rect)

	def draw_second_hand(self, window, second):
		hand_width = 5
		hand_length = self.size * 1.05
		angle = second * 6
		self.draw_hand(window, hand_width, hand_length, angle, (0, 0, 0))

clockobj = clockcl(300, (600, 440), 1200, 900)

while running:
    screen.fill((255, 255, 255))
    screen.blit(image, (-100, -100))
    clockobj.update()
    clockobj.draw(screen)
    pygame.display.flip()
    clock.tick(15)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        
pygame.quit()