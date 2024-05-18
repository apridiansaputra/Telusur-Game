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
        self.original_image = pygame.image.load("./assets/player-1.png")
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.has_key = False
        self.sound_manager = SoundManager()

    def move(self, dx, dy, walls, screen_width, screen_height, camera_x, camera_y):
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += dx
        self.rect.y += dy

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

class Wall(GameObject):
    def __init__(self, pos, desc):
        self.desc = desc
        if self.desc == "horizontal":
            image_path = "./assets/wall-grass-horizontal.jpg"
        elif self.desc == "vertical":
            image_path = "./assets/wall-grass-vertikal.png"
        elif self.desc == "surface":
            image_path = "./assets/surface-paving.png"
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
        super().__init__(pos, (120, 120))
        self.color = (0, 0, 0)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, self.color, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))

class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font_title = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 60)
        self.font_info = pygame.font.Font(None, 48)
        self.font_timer = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 14)
        self.font_score = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 72)

        self.main_screen = pygame.image.load("./assets/main-homescreen.png")
        self.winner_screen = pygame.image.load("./assets/winner-screen.png")
        self.gameover_screen = pygame.image.load("./assets/gameover-screen.png")
        self.map_image = pygame.image.load("./assets/Maps-BG.png")

        self.start_button = pygame.image.load("./assets/start-button.png")
        self.exit_button = pygame.image.load("./assets/exit-button.png")
        self.winner_play_again = pygame.image.load("./assets/win-play-again.png")
        self.winner_exit = pygame.image.load("./assets/win-exit.png")
        self.fail_play_again = pygame.image.load("./assets/retry-button.png")
        self.fail_exit = pygame.image.load("./assets/exit-button.png")

        self.start_button = pygame.transform.scale(self.start_button, (200, 100))
        self.exit_button = pygame.transform.scale(self.exit_button, (200, 100))
        self.winner_play_again = pygame.transform.scale(self.winner_play_again, (200, 100))
        self.winner_exit = pygame.transform.scale(self.winner_exit, (200, 100))
        self.fail_play_again = pygame.transform.scale(self.fail_play_again, (200, 100))
        self.fail_exit = pygame.transform.scale(self.fail_exit, (200, 100))

    def draw_initial_screen(self, game_status=None, score=None, score_position=None):
        if game_status == "success":
            self.screen.blit(self.winner_screen, (0, 0))
            start_button_image = self.winner_play_again
            exit_button_image = self.winner_exit
        elif game_status == "fail":
            self.screen.blit(self.gameover_screen, (0, 0))
            start_button_image = self.fail_play_again
            exit_button_image = self.fail_exit
        else:
            self.screen.blit(self.main_screen, (0, 0))
            start_button_image = self.start_button
            exit_button_image = self.exit_button

        if game_status == "success" and score is not None:
            score_text = self.font_score.render(str(score), True, (255, 255, 255))
            if score_position is None:
                score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            else:
                score_rect = score_text.get_rect(center=score_position)
            self.screen.blit(score_text, score_rect)

        start_button_rect = start_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 150))
        self.screen.blit(start_button_image, start_button_rect)

        exit_button_rect = exit_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 220))
        self.screen.blit(exit_button_image, exit_button_rect)

        pygame.display.flip()
        return start_button_rect, exit_button_rect

    def draw_timer(self, time_left):
        timer_text = self.font_timer.render(f"Sisa Waktu: {time_left} detik", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))

    def draw_map_overlay(self, time_left):
        self.screen.blit(self.map_image, (0, 0))
        timer_text = self.font_timer.render(f"Sisa Waktu: {time_left} detik", True, (255, 255, 255))
        self.screen.blit(timer_text, (self.map_image.get_width() + 10, 10))
        pygame.display.flip()

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
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

class Game:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption("Telusur")
        self.sound_manager = SoundManager()
        self.screen = Screen()
        self.clock = pygame.time.Clock()
        self.surface = pygame.image.load("./assets/surface-soil.png")
        self.time_limit = 60
        self.obstacles = [
            ["  HHHHHHHHHHHHHHHHHHV",
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

            ["  HHHHHHHHHHHHHHHHHHV",
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

            ["  HHHHHHHHHHHHHHHHHHV",
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
        self.sound_manager.play_menu_sound()
        self.sound_manager.stop_game_sound()

        x = y = 0
        for row in self.selected_obstacle:
            for col in row:
                if col == "H":
                    self.walls.append(Wall((x, y), "horizontal"))
                if col == "V":
                    self.walls.append(Wall((x, y), "vertical"))
                if col == " ":
                    self.walls.append(Wall((x, y), "surface"))
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
        self.score_position = (self.screen.screen.get_width() // 2, 100)
        self.show_map = True
        self.map_start_time = None

    def main_game_loop(self):
        while True:
            if self.current_screen == "initial":
                self.handle_initial_screen()
            elif self.current_screen == "game":
                self.run_game()
                self.reset_game()
                self.current_screen = "initial"

    def handle_initial_screen(self):
        start_button_rect, exit_button_rect = self.screen.draw_initial_screen(self.game_status, self.score, self.score_position)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        self.current_screen = "game"
                        self.sound_manager.stop_menu_sound()
                        self.sound_manager.play_game_sound()
                        self.map_start_time = time.time()
                        return
                    elif exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            self.screen.draw_initial_screen(self.game_status, self.score, self.score_position)
            pygame.display.flip()

    def run_game(self):
        self.start_time = time.time()
        running_game = True

        while running_game:
            self.clock.tick(60)
            elapsed_time = int(time.time() - self.start_time)
            time_left = max(self.time_limit - elapsed_time, 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running_game = False

            if self.show_map:
                map_elapsed_time = int(time.time() - self.map_start_time)
                self.screen.draw_map_overlay(15 - map_elapsed_time)
                if map_elapsed_time >= 15:
                    self.show_map = False
                    self.start_time = time.time()
            else:
                key = pygame.key.get_pressed()
                dx, dy = 0, 0
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    dx = -5
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    dx = 5
                if key[pygame.K_UP] or key[pygame.K_w]:
                    dy = -5
                if key[pygame.K_DOWN] or key[pygame.K_s]:
                    dy = 5
                self.character.move(dx, dy, self.walls, 4270, 3500, self.camera_x, self.camera_y)
                self.character.collect_key(self.keys)

                self.camera_x = max(0, min(self.character.rect.x, 1730))
                self.camera_y = max(0, min(self.character.rect.y, 845))

                self.screen.screen.blit(self.surface, (0, 0))

                for wall in self.walls:
                    self.screen.screen.blit(wall.image, (wall.rect.x - self.camera_x, wall.rect.y - self.camera_y))

                self.screen.screen.blit(self.character.image, (self.character.rect.x - self.camera_x, self.character.rect.y - self.camera_y))

                for key in self.keys:
                    if not key.collected:
                        self.screen.screen.blit(key.image, (key.rect.x - self.camera_x, key.rect.y - self.camera_y))

                self.close_door.draw(self.screen.screen, self.camera_x, self.camera_y)

                self.screen.draw_timer(time_left)

                pygame.display.flip()

                if self.character.check_door_collision(self.close_door):
                    self.score = time_left * 5
                    self.current_screen = "success"
                    self.game_status = "success"
                    running_game = False

                if time_left <= 0:
                    self.score = 0
                    self.current_screen = "fail"
                    self.game_status = "fail"
                    running_game = False

        self.sound_manager.stop_game_sound()
        self.sound_manager.play_menu_sound()
        self.handle_initial_screen()

    def set_score_position(self, position):
        self.score_position = position

    def start(self):
        self.main_game_loop()

if __name__ == "__main__":
    game = Game()
    game.start()
