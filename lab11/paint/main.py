import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
tool="brush" 

colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)

clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = 0
currY = 0

prevX = 0
prevY = 0

color = (255, 0, 0)

done = False

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def calculate_rhombus(x1, y1, x2, y2):
    width  = abs(x1 - x2)
    height = abs(y1 - y2)
    left_x = min(x1, x2)
    top_y  = min(y1, y2)

    top_point    = (left_x + width // 2, top_y)
    rigth_point  = (left_x + width, top_y + height // 2)
    bottom_point = (left_x + width // 2, top_y + height)
    left_point   = (left_x, top_y + height // 2)

    return (top_point, rigth_point, bottom_point, left_point)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
                print(tool)
            if event.key == pygame.K_r:
                tool = "rect"
                print(tool)
            if event.key == pygame.K_e:
                tool = "eraser"
                print(tool)
            if event.key == pygame.K_o:
                tool = "circle"
                print(tool)
            if event.key == pygame.K_s:
                tool = "square"
            if event.key == pygame.K_t:
                tool = "eq triangle"
            if event.key == pygame.K_y:
                tool = "right triangle"
            if event.key == pygame.K_h:
                tool = "rhombus"
            if event.key == pygame.K_1:
                color = (255, 0, 0)
            if event.key == pygame.K_2:
                color = (0, 255, 0)
            if event.key == pygame.K_3:
                color = (0, 0, 255)
            if event.key == pygame.K_4:
                color = (0, 255, 0)
            if event.key == pygame.K_5:
                color = (255, 255, 0)
            if event.key == pygame.K_6:
                color = (255, 255, 255)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("LMB pressed!")
            LMBpressed = True
            currX = event.pos[0]
            currY = event.pos[1]
            prevX = event.pos[0]
            prevY = event.pos[1]
        
        if event.type == pygame.MOUSEMOTION:
            print("Position of the mouse:", event.pos)
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("LMB released!")
            LMBpressed = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_EQUALS:
                print("increased thickness")
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                print("reduced thickness")
                THICKNESS -= 1
            if event.key == pygame.K_c:
                print("canvas cleared")
                screen.fill(colorBLACK)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if tool == "rect":
                    pygame.draw.rect(screen, color,
                                     (min(prevX, currX),
                                      min(prevY, currY),
                                      abs(prevX-currX),
                                      abs(prevY-currY)), 2)
                    
                elif tool == "circle":
                    r = int(((prevX-currX)**2 + (prevY-currY)**2)**0.5)
                    pygame.draw.circle(screen, color, (prevX, prevY), r, 2)

                elif tool == "square":
                    pygame.draw.rect(screen, color,
                                     (min(prevX, currX),
                                      min(prevX, currX),
                                      abs(prevX-currX),
                                      abs(prevX-currX)), 2)
                    
                elif tool == "eq triangle":
                    s = math.sqrt(abs((currX - prevX)**2 + (currY - prevY)**2))
                    h = s * math.sqrt(3) / 2
                    m = (currX + (s/2), currY)
                    pygame.draw.polygon(screen, color, ((prevX, currY), (currX, currY), (currX + (s/2), currY + h)), 2)

                elif tool == "right triangle":
                    pygame.draw.polygon(screen, color, ((prevX, prevY), (currX, currY), (prevX, currY)), 2)

                elif tool == "rhombus":
                    hx = math.sqrt((currX - prevX)**2)
                    hy = math.sqrt ((currY - prevY)**2)
                    pygame.draw.polygon(screen, color, calculate_rhombus(prevX, prevY, currX, currY), 2)
                    
    if LMBpressed and tool == "brush":
        pygame.draw.line(screen, color, (prevX, prevY), (currX, currY), THICKNESS)
    if LMBpressed and tool == "eraser":
        pygame.draw.line(screen, colorBLACK, (prevX, prevY), (currX, currY), THICKNESS)
    if tool == "brush" or tool == "eraser":
        prevX = currX
        prevY = currY

    pygame.display.flip()
    clock.tick(60)