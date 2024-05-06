import pygame
from gameObject import GameObject

class Key(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (60, 60))
        self.original_image = pygame.image.load("./assets/kunci.png")
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.collected = False
