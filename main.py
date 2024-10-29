from sys import exit
import pygame
pygame.init()
# COLORS
WIDTH = 600
HEIGHT = 500
FPS = 60
BG_COLOR = (10,20,195)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (250,10,10)
GREEN = (10, 220, 10)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Global Savior")
screen.fill(BG_COLOR)
clock = pygame.time.Clock()
# 
ball_direction_x = 3
ball_direction_y = 3
# 
platform_x = 200
platform_y = 450
move_right = False
move_left = False
run = True
# 
class Area:
    def __init__(self, x,y,width,height,color):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = color
        if color:
            self.fill_color = color
    
    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(screen, self.fill_color, self.rect)
    
    def collidePoint(self,x,y):
        return self.rect.collidepoint(x,y)
    
    def collideRect(self, rect):
        return self.rect.colliderect(rect)
    

class Label(Area):
    def set_text(self, text, fsize=14, text_color=BLACK):
        self.image = pygame.font.SysFont('verdana',fsize).render(text,True,text_color)
        
    def draw(self, shift_x=0,shift_y=0):
        self.fill()
        screen.blit(self.image,(self.rect.x + shift_x, self.rect.y + shift_y))
        
        
class Picture(Area):
    def __init__(self, filename, x, y, width, height):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=BG_COLOR)
        self.image = pygame.image.load(filename)
        
    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))
        
ball = Picture('ball.png',160,200,50,50)
platform = Picture('platform.png',platform_x,platform_y,50,50)
start_x = 5
start_y = 5
# 
count = 9   
monsters = []
for j in range(3):
    y = start_y +(55*j)
    x = start_x + (27.5 *j)
    for i in range(count):
        enemy = Picture('enemy.png', x,y,50,50)
        monsters.append(enemy)
        x += 55 
    count -= 1
    
while run:
    ball.fill()
    platform.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False
    
    if move_right:
        platform.rect.x += 5
        
    if move_left:
        platform.rect.x -= 5
        
    ball.rect.x += ball_direction_x
    ball.rect.y += ball_direction_y
    if ball.rect.y < 0:
        ball_direction_y *= -1
    
    if ball.rect.x > 450 or ball.rect.x < 0:
        ball_direction_x *= -1
    
    if ball.rect.y > 400:
        time_text = Label(150,150,50,50, BG_COLOR)
        time_text.set_text('You Lost!', 60, RED)
        time_text.draw(10,10)
        # run = False
        
    if len(monsters) == 0:
        time_text = Label(150,150,50,50, BG_COLOR)
        time_text.set_text('You Lost!', 60, GREEN)
        time_text.draw(10,10)
        run = False
        
    if ball.rect.colliderect(platform.rect):
        ball_direction_y *= -1
        
    for monster in monsters:
        monster.draw()
        if monster.rect.colliderect(ball.rect):
            monsters.remove(monster)
            monster.fill()
            ball_direction_y *= -1
    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(FPS)
