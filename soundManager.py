import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("./assets/audio/backsound-first.mp3")
        self.enter_sound = pygame.mixer.Sound("./assets/audio/awesomeness.wav")
        self.wall_hit_sound = pygame.mixer.Sound("./assets/audio/wall.wav")
        self.key_pickup_sound = pygame.mixer.Sound("./assets/audio/stepwater_1.wav")
        self.success_sound = pygame.mixer.Sound("./assets/audio/stepwood_1.wav")

    def play_background_music(self):
        self.background_music.play(-1)

    def play_enter_sound(self):
        self.enter_sound.play()

    def play_wall_hit_sound(self):
        self.wall_hit_sound.play()

    def play_key_pickup_sound(self):
        self.key_pickup_sound.play()

    def play_success_sound(self):
        self.success_sound.play()

    def stop_background_music(self):
        self.background_music.stop()

    def stop_all_sounds(self):
        pygame.mixer.stop()
