import pygame

class GameObject:
    def __init__(self, position, scale):
        self.rect = pygame.Rect(position[0], position[1], scale[0], scale[1])