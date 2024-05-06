import pygame
from gameObject import GameObject

class Wall(GameObject):
    def __init__(self, pos, desc):
        if desc == "horizontal":
            image_path = "./assets/horizontal-2.png"
        elif desc == "vertical":
            image_path = "./assets/vertikal-2.png"
        super().__init__(pos, (120, 120))
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
