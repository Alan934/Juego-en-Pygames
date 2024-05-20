import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy Bird')

ground_scroll = 0
scroll_speed = 3
flying = False
game_over = False
pipe_gap = 250
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency

bg = pygame.image.load('img/selva.jpeg')
ground_img = pygame.image.load('img/Suelo.png')
ground_img = pygame.transform.scale(ground_img, (1000,61))

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        bird_img = pygame.image.load('img/Pajaro.png')
        self.image = pygame.transform.scale(bird_img, (88, 66))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        
    def update(self):
        #if flying == True:
            #gravedad
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 875:
                self.rect.y += int(self.vel)
        
        #if game_over == False:
            #salto
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, position):
        pygame.sprite.Sprite.__init__(self)
        pipe_img = pygame.image.load('img/Tubo2.png')
        rotated_pipe_img = pygame.transform.rotate(pipe_img, 180)
        self.image = pygame.transform.scale(rotated_pipe_img, (110, 450))
        self.rect = self.image.get_rect()
        #posicion 1 es arriba y posicion -1 es abajo
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:            
            self.rect.topleft = [x, y + int(pipe_gap/2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))

bird_group.add(flappy)

run = True
while run:
    clock.tick(fps)    
    #fondo
    screen.blit(bg, (0,0))
    
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)    
    
    #Suelo
    screen.blit(ground_img, (ground_scroll,875))
    
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
           
    #Pajaro choca con suelo
    if flappy.rect.bottom >= 875:
        game_over = True
        flying = False    
    
    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height/2)+pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2)+pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    
    pygame.display.update()        

pygame.quit()