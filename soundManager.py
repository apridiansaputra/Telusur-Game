import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.menu_sound = pygame.mixer.Sound('./assets/audio/backsound-first.mp3')
        self.game_sound = pygame.mixer.Sound('./assets/audio/awesomeness.wav')
        self.wall_hit_sound = pygame.mixer.Sound("./assets/audio/wall.wav")
        self.key_pickup_sound = pygame.mixer.Sound("./assets/audio/stepwater_1.wav")
        self.success_sound = pygame.mixer.Sound('./assets/audio/stepwood_1.wav')

    def play_menu_sound(self):
        self.menu_sound.play(-1)

    def stop_menu_sound(self):
        self.menu_sound.stop()

    def play_game_sound(self):
        self.game_sound.play(-1)

    def stop_game_sound(self):
        self.game_sound.stop()

    def play_wall_hit_sound(self):
        self.wall_hit_sound.play()

    def play_key_pickup_sound(self):
        self.key_pickup_sound.play()

    def play_success_sound(self):
        self.success_sound.play()

    def stop_success_sound(self):
        self.success_sound.stop()

    def stop_key_pickup_sound(self):
        self.key_pickup_sound.stop()

    def stop_wall_hit_sound(self):
        self.wall_hit_sound.stop()