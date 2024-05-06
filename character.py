import pygame
from gameObject import GameObject

class Character(GameObject):
    def __init__(self, position=(50, 50)):
        super().__init__(position, (110, 110))
        self.original_image = pygame.image.load("./assets/palyer-1.png")
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.has_key = False

    def move(self, dx, dy, walls, screen_width, screen_height, camera_x, camera_y):
        old_x, old_y = self.rect.x, self.rect.y

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x, self.rect.y = old_x, old_y
                break

        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width - camera_x))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height - camera_y))

    def collect_key(self, keys):
        for key in keys:
            if self.rect.colliderect(key.rect):
                key.collected = True
                self.has_key = True
                keys.remove(key)
                break