import pygame
from gameObject import GameObject

class Key(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (150, 150))
        self.original_image = pygame.image.load("./assets/key-kehidupan.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.collected = False