import pygame
import os
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE)
import random

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
        self.done = False

        self.all_bubbles = pygame.sprite.Group()

    def run(self):
        while not self.done:
            for event in self.pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                    if event.key == K_SPACE:
                        self.addBubble()
            self.draw()

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.all_bubbles.draw(self.screen)
        self.pygame.display.flip()

    def addBubble(self):
        self.all_bubbles.add(Bubble(self.settings, self))

class Bubble(pygame.sprite.Sprite):
    def __init__(self, settings, game):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.pygame = pygame

        self.setSize()
        self.setImage()
        self.generateCords()

    def setSize(self):
        self.width = 10
        self.height = 10

    def generateCords(self):
        self.rect.left = random.randint(0, self.settings.width - self.width)
        self.rect.top = random.randint(0, self.settings.height - self.height)

    def setImage(self):
        circleFiles = ["redCircle.png", "blueCircle.png", "greenCircle.png", "yellowCircle.png"]
        self.image = pygame.image.load(os.path.join(self.settings.images_path, circleFiles[random.randint(0, len(circleFiles)) - 1])).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()


    def increaseSize(self):
        self.width += 2
        self.height += 2

if __name__ == '__main__':
    settings = Settings()
    pygame.init()
    game = Game(pygame, settings)
    game.run()

    pygame.quit()