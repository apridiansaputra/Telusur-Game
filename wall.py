import pygame
from gameObject import GameObject

class Wall(GameObject):
    def __init__(self, pos, desc, theme):
        self.desc = desc
        if self.desc == "horizontal":
            image_path = theme["horizontal"]
        elif self.desc == "vertical":
            image_path = theme["vertical"]
        elif self.desc == "surface":
            image_path = theme["surface"]
        super().__init__(pos, (150, 150))
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, self.rect.size)