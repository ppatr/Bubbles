import pygame   #importiert die Pygamme Bibliothek in das Skript   
import os
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE)

class Settings(object):
    def __init__(self):
        self.width = 700
        self.height = 400
        self.fps = 60
        self.title = "Bubbles"
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "background.jpg")).convert()
        self.background_rect = self.background.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
#        self.bubble = Bubble(settings)

#        self.all_bubbles = pygame.sprite.Group()
#        self.all_bubbles.add(self.bubble)

    def run(self):
        while not self.done:
            self.clock.tick(self.settings.fps)
            for event in self.pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True

            self.draw()

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.pygame.display.flip()

#class Bubble(pygame.sprite.Sprite):
#    def __init__(self, settings):
#        pygame.sprite.Sprite.__init__(self)
#        self.settings = settings
#        self.pygame = pygame
#        self.image = pygame.image.load(os.path.join(self.settings.images_path, "bubble.png")).convert_alpha()
#        self.image = pygame.transform.scale(self.image, (55, 30))
#        self.rect = image.get_rect()


if __name__ == '__main__':
    settings = Settings()
    pygame.init()
    game = Game(pygame, settings)
    game.run()

    pygame.quit()