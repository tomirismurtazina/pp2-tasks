import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

x=375
y=275

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]: 
        x += 2
    if keys[pygame.K_LEFT]: 
        x -= 2
    if keys[pygame.K_DOWN]:
        y += 2
    if keys[pygame.K_UP]:
        y -= 2

    if x - 25 < 0:
        x = 25
    if x + 25 > 800:
        x = 800 - 25
    if y - 25 < 0:
        y = 25
    if y + 25 > 600:
        y = 600 - 25

    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)
    pygame.display.flip()
    screen.fill((255, 255, 255))