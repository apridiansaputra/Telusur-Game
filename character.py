import pygame
from gameObject import GameObject
from soundManager import SoundManager

class Character(GameObject):
    def __init__(self, position=(10, 50)):
        super().__init__(position, (120, 120))
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_speed = 5
        self.image_frames_left = [pygame.image.load(f"./assets/character/adventurer_walk_left{i+1}.png").convert_alpha() for i in range(2)]
        self.image_frames_right = [pygame.image.load(f"./assets/character/adventurer_walk_right{i+1}.png").convert_alpha() for i in range(2)]
        self.image_frames_up = [pygame.image.load(f"./assets/character/adventurer_walk_up{i+1}.png").convert_alpha() for i in range(2)]
        self.image_frames_down = [pygame.image.load(f"./assets/character/adventurer_walk_down{i+1}.png").convert_alpha() for i in range(2)]
        self.original_image = self.image_frames_right[self.frame_index]
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.has_key = False
        self.sound_manager = SoundManager()
        self.last_direction = "right"

    def move(self, dx, dy, walls, screen_width, screen_height, camera_x, camera_y):
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            self.frame_counter += 1
            if dx > 0:
                self.last_direction = "right"
            elif dx < 0:
                self.last_direction = "left"
            elif dy < 0:
                self.last_direction = "up"
            elif dy > 0 :
                self.last_direction = "down"
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.image_frames_right) 
                if self.last_direction == "right":
                    self.original_image = self.image_frames_right[self.frame_index]
                elif self.last_direction == "left":
                    self.original_image = self.image_frames_left[self.frame_index]
                elif self.last_direction == "up":
                    self.original_image = self.image_frames_up[self.frame_index]
                elif self.last_direction == "down":
                    self.original_image = self.image_frames_down[self.frame_index]
                self.image = pygame.transform.scale(self.original_image, self.rect.size)

        for wall in walls:
            if wall.desc != "surface" and self.rect.colliderect(wall.rect):
                self.rect.x, self.rect.y = old_x, old_y
                break

        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width - camera_x))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height - camera_y))

    def collect_key(self, keys):
        for key in keys:
            if self.rect.colliderect(key.rect):
                key.collected = True
                self.has_key = True
                self.sound_manager.play_key_pickup_sound()
                keys.remove(key)
                break

    def check_door_collision(self, door):
        return self.has_key and self.rect.colliderect(door.rect)