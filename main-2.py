import pygame
import os
import sys
import random
import time


class GameObject:
    def __init__(self, position, scale):
        self.rect = pygame.Rect(position[0], position[1], scale[0], scale[1])


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


class Wall(GameObject):
    def __init__(self, pos, desc):
        if desc == "horizontal":
            image_path = "./assets/horizontal-2.png"
        elif desc == "vertical":
            image_path = "./assets/vertikal-2.png"
        super().__init__(pos, (120, 120))
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, self.rect.size)


class Key(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (60, 60))
        self.original_image = pygame.image.load("./assets/kunci.png")
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.collected = False


class Door(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (60, 60))
        self.color = (0, 0, 0)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, self.color, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))


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


class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font_title = pygame.font.Font("./assets/fonts/Gameplay.ttf", 60)
        self.font_info = pygame.font.Font(None, 48)
        self.original_image = pygame.image.load("./assets/homescreen.png")
        self.start_button_image = pygame.image.load("./assets/play-button.png")
        self.exit_button_image = pygame.image.load("./assets/exit-button.png")

        self.start_button_image = pygame.transform.scale(self.start_button_image, (600, 500))
        self.exit_button_image = pygame.transform.scale(self.exit_button_image, (600, 500))

    def draw_initial_screen(self, game_status=None, score=None):
        self.screen.blit(self.original_image, (0, 0))

        if game_status == "success" and score is not None:
            result_text = self.font_info.render(f"Selamat! Skor Anda: {score}", True, (255, 255, 255))
            result_rect = result_text.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(result_text, result_rect)
        elif game_status == "fail":
            result_text = self.font_info.render("Game Over!", True, (255, 255, 255))
            result_rect = result_text.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(result_text, result_rect)

        start_button_rect = self.start_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(self.start_button_image, start_button_rect)

        exit_button_rect = self.exit_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 140))
        self.screen.blit(self.exit_button_image, exit_button_rect)

        pygame.display.flip()
        return start_button_rect, exit_button_rect

    def draw_result_screen(self, message, score):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        card_width = 600
        card_height = 400
        card_x = (self.screen.get_width() - card_width) // 2
        card_y = (self.screen.get_height() - card_height) // 2
        pygame.draw.rect(self.screen, (105, 105, 105), (card_x, card_y, card_width, card_height))

        title_text = self.font_title.render(f"{message} Skor Anda: {score}", True, (210, 180, 140))
        text_rect = title_text.get_rect(center=(self.screen.get_width() // 2, card_y + 100))
        self.screen.blit(title_text, text_rect)

        play_again_button = pygame.Rect(card_x + 75, card_y + 200, 450, 70)
        pygame.draw.rect(self.screen, (139, 69, 19), play_again_button)
        play_again_text = self.font_title.render("Main Lagi", True, (255, 255, 255))
        text_rect = play_again_text.get_rect(center=play_again_button.center)
        self.screen.blit(play_again_text, text_rect)

        exit_button = pygame.Rect(card_x + 125, card_y + 300, 350, 70)
        pygame.draw.rect(self.screen, (139, 69, 19), exit_button)
        exit_text = self.font_title.render("Keluar", True, (255, 255, 255))
        text_rect = exit_text.get_rect(center=exit_button.center)
        self.screen.blit(exit_text, text_rect)

        pygame.display.flip()
        return play_again_button, exit_button

    def draw_timer(self, time_left):
        timer_text = self.font_info.render(f"Waktu: {time_left}", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))


class Game:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption("Labirin PBO")

        self.sound_manager = SoundManager()
        self.screen = Screen()
        self.clock = pygame.time.Clock()
        self.surface = pygame.image.load("./assets/surface-soil.png")
        self.time_limit = 60 

        self.obstacles = [
            [" HHHHHHHHHHHHHHHHHHHV",
             "                    V",
             "V HHHHHHHHHHHHHHHHH V",
             "V                   V",
             "V                   V",
             "V HHV  HHHHHHHHHHHV V",
             "V   V             V V",
             "V   VK            H V",
             "V   HHV HHHHV       V",
             "V     H     HHHHHHH H",
             "V                    E",
             "VVVVVVVVVVVVVVVVVVVVV"],

            [" HHHHHHHHHHHHHHHHHHHV",
             "                    V",
             "V HHHHHHHHHHHHHHHHH V",
             "V                   V",
             "V HHHHHHHHHHHHHHHHH V",
             "V                   V",
             "V V   V V         V V",
             "V V   V V         V V",
             "V HHHHV HHHVHHHHHHV V",
             "V     H   KV      H H",
             "V          V         E",
             "VVVVVVVVVVVVVVVVVVVVV"],

            [" HHHHHHHHHHHHHHHHHHHV",
             "                    V",
             "V HHHHHHHHHHHHHHHHH V",
             "V                   V",
             "V HHHHHHHHHHHHHHHHH V",
             "V                   V",
             "V V   V V         V V",
             "V V   V V         V V",
             "V VHHHV HHHHHHHHHHV V",
             "V H  KH           V H",
             "V                 V  E",
             "VVVVVVVVVVVVVVVVVVVVV"]
        ]

        self.reset_game()

    def reset_game(self):
        self.character = Character()
        self.walls = []
        self.keys = []
        self.selected_obstacle = random.choice(self.obstacles)

        x = y = 0
        for row in self.selected_obstacle:
            for col in row:
                if col == "H":
                    self.walls.append(Wall((x, y), "horizontal"))
                if col == "V":
                    self.walls.append(Wall((x, y), "vertical"))
                if col == "K":
                    self.keys.append(Key((x, y)))
                if col == "E":
                    self.close_door = Door((x, y))
                x += 120
            y += 120
            x = 0

        self.camera_x = 0
        self.camera_y = 0
        self.current_screen = "initial"
        self.start_time = time.time()
        self.game_status = None
        self.score = 0

    def main_game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.current_screen == "initial":
                        start_button, exit_button = self.screen.draw_initial_screen(self.game_status, self.score)
                        if start_button.collidepoint(mouse_pos):
                            self.sound_manager.play_enter_sound()
                            self.sound_manager.stop_background_music()
                            self.current_screen = "game" 
                            return True
                        elif exit_button.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()

            if self.current_screen == "initial":
                self.screen.draw_initial_screen(self.game_status, self.score)
            elif self.current_screen == "game":
                break

    def start_game(self):
        self.sound_manager.play_background_music() 
        self.main_game_loop()
        self.sound_manager.play_wall_hit_sound()
        self.sound_manager.play_key_pickup_sound()

if __name__ == "__main__":
    game = Game()
    while True:
        game.start_game()