import pygame
import os
import threading
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN)
import random

class Settings(object):
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.fps = 60
        self.title = "Bubbles"
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")
        self.sounds_path = os.path.join(self.file_path, "sounds")

    def get_dim(self):
        return (self.width, self.height)


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pygame = pygame
        self.settings = settings
        self.image_orig = pygame.image.load(os.path.join(self.settings.images_path, "crosshair.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (48, 48))
        self.rect = self.image.get_rect()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if self.rect.collidepoint(*mouse_pos) and mouse_clicked[0]:
            self.image_orig = pygame.image.load(os.path.join(self.settings.images_path, "crosshair_red.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image_orig, (48, 48))
            self.rect = self.image.get_rect()
        else:
            self.image_orig = pygame.image.load(os.path.join(self.settings.images_path, "crosshair.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image_orig, (48, 48))
            self.rect = self.image.get_rect()



class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "background.jpg")).convert()
        self.background_rect = self.background.get_rect()
        self.done = False

        self.all_bubbles = pygame.sprite.Group()
        

    def run(self):
        counter = 10
        timer_interval = 50
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event , timer_interval)
        

        while not self.done:
            self.all_bubbles.update()
            mouse.update()
            mouse.sprite.rect.centerx, mouse.sprite.rect.centery = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)

            for event in self.pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True


                elif event.type == timer_event:
                    counter -= 1
                    if counter == 0:
                        counter = 10
                        self.addBubble()
                    
            self.draw()

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        
        text = font.render("Score:" + " " + str(score), True, fontcolor)
        self.screen.blit(text, (settings.width//2 - text.get_rect().centerx, settings.height//10 - text.get_rect().centery))
        self.all_bubbles.draw(self.screen)
        mouse.draw(self.screen)
        self.pygame.display.flip()

    def addBubble(self):
        self.all_bubbles.add(Bubble(self.settings, self))

class Bubble(pygame.sprite.Sprite):
    def __init__(self, settings, game):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.pygame = pygame
        self.diameter = 5
        self.time_between_bubble_grow = 25
        self.time_next_bubble_grow = pygame.time.get_ticks()
       

        self.setImage()
        self.generateCords()
        self.scale()

    def generateCords(self):
        self.rect.left = random.randint(0, self.settings.width - self.diameter)
        self.rect.top = random.randint(0, self.settings.height - self.diameter)

    def setImage(self):
        self.image_orig = pygame.image.load(os.path.join(self.settings.images_path, "Bubble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (self.diameter, self.diameter))
        self.rect = self.image.get_rect()

    def scale(self):
        if self.can_grow():
            self.diameter += random.randint(1, 4)
            c = self.rect.center
            self.image = pygame.transform.scale(self.image_orig, (self.diameter, self.diameter))
            self.rect = self.image.get_rect()
            self.rect.center = c

            self.time_next_bubble_grow = pygame.time.get_ticks() + self.time_between_bubble_grow

    def update(self):
        self.scale()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if self.rect.collidepoint(*mouse_pos) and mouse_clicked[0]:
            pop = pygame.image.load(os.path.join(self.settings.images_path, "bubblepop.png")).convert_alpha()
            pop = pygame.transform.scale(pop, (self.diameter, self.diameter))
            self.image = pop
            self.rect = self.image.get_rect()

            game.screen.blit(pop, (mouse_pos))
            self.kill()
            global score
            score += 1
            play = pygame.mixer.Sound(os.path.join(self.settings.sounds_path, "hitmarker.mp3"))
            pygame.mixer.Sound.play(play)

    def can_grow(self):
        return pygame.time.get_ticks() >= self.time_next_bubble_grow

        
if __name__ == '__main__':
    settings = Settings()
    pygame.init()
    
    score = 0
    fontsize = 32
    fontcolor = [255, 255, 255]
    font = pygame.font.Font(pygame.font.get_default_font(), fontsize)
    
   

    game = Game(pygame, settings)
    mouse = pygame.sprite.GroupSingle(Mouse())
    game.run()

    pygame.quit()