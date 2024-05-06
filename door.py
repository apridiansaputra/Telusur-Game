import pygame
from gameObject import GameObject

class Door(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (60, 60))
        self.color = (0, 0, 0)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, self.color, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))
