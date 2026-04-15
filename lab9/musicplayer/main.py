import pygame
from pygame import mixer

pygame.init()
mixer.init()
mixer.music.set_volume(1)
font = pygame.font.SysFont("comicsansms", 20)


playlist=["FallOutBoy-ThisAin'tAScene,It'sAnArmsRace.mp3", "My Chemical Romance - Bulletproof Heart.mp3", "Pierce the Veil - A Match Into Water.mp3"]

screen = pygame.display.set_mode((800, 600))

running = True
i=0

text = font.render("FallOutBoy-ThisAin'tAScene,It'sAnArmsRace", True, (255, 255, 255))


text1 = font.render("My Chemical Romance - Bulletproof Heart", True, (255, 255, 255))

text2 = font.render("Pierce the Veil - A Match Into Water", True, (255, 255, 255))


while running:
    if i==0:
        screen.fill((0, 0, 0))
        screen.blit(text, (0, 0))
    elif i==1:
        screen.fill((0, 0, 0))
        screen.blit(text1, (0, 0))
    elif i==2:
        screen.fill((0, 0, 0))
        screen.blit(text2, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                mixer.music.load(playlist[i])
                song=playlist[i]
                mixer.music.play()

            elif event.key == pygame.K_s:
                mixer.music.pause()

            elif event.key == pygame.K_n:
                mixer.music.unload()
                mixer.music.load(playlist[i+1])
                mixer.music.play()
                i+=1

            elif event.key == pygame.K_b:
                mixer.music.unload()
                mixer.music.load(playlist[i-1])
                mixer.music.play()
                i-=1
            elif event.key == pygame.K_q:
                running = False
                pygame.quit()

        elif event.type == pygame.QUIT:
            running = False
            pygame.quit()
        pygame.display.flip()