import pygame
import os
import sys
import random
import time

class GameObject:
    def __init__(self, position, scale):
        self.rect = pygame.Rect(position[0], position[1], scale[0], scale[1])


class Character(GameObject):
    def __init__(self, position=(10, 50)):
        super().__init__(position, (120, 120))
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_speed = 5
        self.image_frames_left = [pygame.image.load(f"./assets/character/adventurer_walk_left{i+1}.png").convert_alpha() for i in range(2)]
        self.image_frames_right = [pygame.image.load(f"./assets/character/adventurer_walk_right{i+1}.png").convert_alpha() for i in range(2)]
        self.image_frames_up = [pygame.image.load(f"./assets/character/adventurer_walk_up{i+1}.png").convert_alpha() for i in range(2)]
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
            if dx > 0 or dy > 0:
                self.last_direction = "right"
            elif dx < 0:
                self.last_direction = "left"
            elif dy < 0:
                self.last_direction = "up"
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.image_frames_right) 
                if self.last_direction == "right":
                    self.original_image = self.image_frames_right[self.frame_index]
                elif self.last_direction == "left":
                    self.original_image = self.image_frames_left[self.frame_index]
                elif self.last_direction == "up":
                    self.original_image = self.image_frames_up[self.frame_index]
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

class Key(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (60, 60))
        self.original_image = pygame.image.load("./assets/kunci.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, self.rect.size)
        self.collected = False

class Door(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (180, 180))
        self.color = (0, 0, 0)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, self.color, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))

class Screen:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720 
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.font_title = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 60)
        self.font_info = pygame.font.Font(None, 48)
        self.font_timer = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 14)
        self.font_score = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 72)

        self.main_screen = pygame.image.load("./assets/main-screen.png").convert_alpha()
        self.winner_screen = pygame.image.load("./assets/winner-screen.png").convert_alpha()
        self.gameover_screen = pygame.image.load("./assets/gameover-screen.png").convert_alpha()

        self.start_button = pygame.image.load("./assets/start-button.png").convert_alpha()
        self.exit_button = pygame.image.load("./assets/exit-button.png").convert_alpha()
        self.winner_play_again = pygame.image.load("./assets/win-play-again.png").convert_alpha()
        self.winner_exit = pygame.image.load("./assets/win-exit.png").convert_alpha()
        self.fail_play_again = pygame.image.load("./assets/retry-button.png").convert_alpha()
        self.fail_exit = pygame.image.load("./assets/exit-button.png").convert_alpha()

        self.start_button = pygame.transform.scale(self.start_button, (210, 80))
        self.exit_button = pygame.transform.scale(self.exit_button, (210, 80))
        self.winner_play_again = pygame.transform.scale(self.winner_play_again, (80, 80))
        self.winner_exit = pygame.transform.scale(self.winner_exit, (80, 80))
        self.fail_play_again = pygame.transform.scale(self.fail_play_again, (210, 80))
        self.fail_exit = pygame.transform.scale(self.fail_exit, (210, 80))

    def draw_initial_screen(self, game_status=None, score=None, score_position=None):
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()

        if game_status == "success":
            self.screen.blit(pygame.transform.scale(self.winner_screen, (screen_width, screen_height)), (0, 0))
            start_button_image = self.winner_play_again
            start_button_rect = start_button_image.get_rect(center=(screen_width // 2 - 80, screen_height // 2 + 100))
            self.screen.blit(start_button_image, start_button_rect)
            exit_button_image = self.winner_exit
            exit_button_rect = exit_button_image.get_rect(center=(screen_width // 2 + 80, screen_height // 2 + 100))
            self.screen.blit(exit_button_image, exit_button_rect)
            
        elif game_status == "fail":
            self.screen.blit(pygame.transform.scale(self.gameover_screen, (screen_width, screen_height)), (0, 0))
            start_button_image = self.fail_play_again
            exit_button_image = self.fail_exit
        else:
            self.screen.blit(pygame.transform.scale(self.main_screen, (screen_width, screen_height)), (0, 0))
            start_button_image = self.start_button
            exit_button_image = self.exit_button

        if game_status == "success" and score is not None:
            score_text = self.font_score.render(str(score), True, (255, 255, 255))
            if score_position is None:
                score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
            else:
                score_rect = score_text.get_rect(center=score_position)
            self.screen.blit(score_text, score_rect)

        if game_status != "success":
            start_button_rect = start_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 ))
            self.screen.blit(start_button_image, start_button_rect)

            exit_button_rect = exit_button_image.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            self.screen.blit(exit_button_image, exit_button_rect)

        pygame.display.flip()
        return start_button_rect, exit_button_rect

    def draw_timer(self, time_left):
        timer_text = self.font_timer.render(f"Sisa Waktu: {time_left} detik", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))

    def draw_map_overlay(self, map_image, time_left):
        self.screen.blit(pygame.transform.scale(map_image, (self.screen.get_width(), self.screen.get_height())), (0, -10))
        timer_text = self.font_timer.render(f"Sisa Waktu: {time_left} detik", True, (255, 255, 255))
        self.screen.blit(timer_text, (map_image.get_width() + 10, 10))
        pygame.display.flip()

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

class Game:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption("Telusur")
        self.sound_manager = SoundManager()
        self.screen = Screen()
        self.clock = pygame.time.Clock()
        self.time_limit = 60

        self.obstacles_and_maps = [
            (
                [" HHHVHHHHHHHHHHHHHVHHV",
                 "    V                 E",
                 "V V V HHHHHVHHHHV  V V",
                 "V V V      V    H  V V",
                 "V H HHHHHH V V     V V",
                 "V          V VHHHHHV V",
                 "V HHHHHHHHHH V     V V",
                 "V            V V  KV V",
                 "VHHHH HHHHHHHH HHHHV V",
                 "V                  V V",
                 "V V HHHHHHHHHHHHHHHH H",
                 "V V                  V",
                 "VVVVVVVVVVVVVVVVVVVVVV",],
                "./assets/map1.png"
            ),
            (
                [" HVHVHHHHHHVHHHHHHHHHV",
                 "  V V      V         V",
                 "V H HHHH V V HHHHHHHHH",
                 "V        V V          E",
                 "VHHHH HHHH VHHHH HHH V",
                 "V          V         V",
                 "VHHH  V V  V  HHHHHHHV",
                 "V     V V  V         V",
                 "V HH HH V  VHH   V   V",
                 "V       V  V     V K V",
                 "VHHH HHHV  HHH HHHHHHV",
                 "V       V            V",
                 "VVVVVVVVVVVVVVVVVVVVVV"],
                "./assets/map2.png"
            ),
            (
                [" HHHHHVHHHHHHHHHHHHHHV",
                 "      V              V",
                 "V V HHH V HHHHVHHHH HV",
                 "V V     V     V      V",
                 "V VHHHH V HHV V  VHH V",
                 "V V     V   V V  V   V",
                 "V V VHHHHHHHH V  V V V",
                 "V H H         V  V VKV",
                 "V     VVVHHV  V  V V V"
                 "VHV HHVHH    VV  V   V",
                 "V H   H   HHHHHHHHHHHH",
                 "V       V             E",
                 "VVVVVVVVVVVVVVVVVVVVVV"],
                "./assets/map3.png"
            ),
            (
                [" HHHHHHHHHHVHHHHHHHHHV",
                 "           V         V",
                 "VHHHHH  V  H   V  V  V",
                 "V       V      V  V  V",
                 "VHHHHHHHHHHH   V  V  V",
                 "V              V  V  V",
                 "VHHHHHHHHHHHHHHH  V  V",
                 "V                 VK V",
                 "V  HHHHHHHHHHHHVHHHHHH",
                 "V              V      E",
                 "V  HHHHHHHHV   H  HHHV",
                 "V          V         V",
                 "VVVVVVVVVVVVVVVVVVVVVV"],
                 "./assets/map4.png"
            ),
            (
                [" HHHHHHHHHHVHHHHHHHHHV",
                 "           V         V",
                 "VHHHHHH VH H HHV VVV V",
                 "V       V      V V V V",
                 "VHHHVHHHHHHH   H H HHV",
                 "V   V                V",
                 "V  HHHHHHHHHHHHHHHHV V",
                 "V                    V",
                 "V  HHHHVHH HHHHVHHHHHH",
                 "V     KV       V      E",
                 "V  HHHHHHHHV   H  HHHV",
                 "V          V         V",
                 "VVVVVVVVVVVVVVVVVVVVVV"],
                 "./assets/map5.png"
            )
        ]

        self.themes = [
            {"horizontal": "./assets/theme/wall-grass-horizontal.jpg", 
             "vertical": "./assets/theme/wall-grass-vertikal.png", 
             "surface": "./assets/theme/surface-grass.png"},

            {"horizontal": "./assets/theme/horizontal-new-sayning-2.png", 
             "vertical": "./assets/theme/vertikal-new-sayning-2.png", 
             "surface": "./assets/theme/surface-soil.png"},
        ]

        self.reset_game()

    def reset_game(self):
        self.character = Character()
        self.walls = []
        self.keys = []
        self.selected_obstacle, self.selected_map_image_path = random.choice(self.obstacles_and_maps)
        self.selected_theme = random.choice(self.themes)
        
        self.sound_manager.play_menu_sound()
        self.sound_manager.stop_game_sound()

        x = y = 0
        for row in self.selected_obstacle:
            for col in row:
                if col == "H":
                    self.walls.append(Wall((x, y), "horizontal", self.selected_theme))
                if col == "V":
                    self.walls.append(Wall((x, y), "vertical", self.selected_theme))
                if col == " ":
                    self.walls.append(Wall((x, y), "surface", self.selected_theme))
                if col == "K":
                    self.keys.append(Key((x, y)))
                if col == "E":
                    self.close_door = Door((x, y))
                x += 150
            y += 150
            x = 0

        self.map_image = pygame.image.load(self.selected_map_image_path).convert_alpha()
        self.camera_x = 0
        self.camera_y = 0
        self.current_screen = "initial"
        self.start_time = time.time()
        self.game_status = None
        self.score = 0
        self.score_position = (self.screen.screen.get_width() // 2, self.screen.screen.get_height() // 2)
        self.show_map = True
        self.map_start_time = None

    def main_game_loop(self):
        while True:
            if self.current_screen == "initial":
                self.handle_initial_screen()
            elif self.current_screen == "game":
                self.run_game()
                self.reset_game()
                if self.game_status != "success": 
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
               # elif event.type == pygame.VIDEORESIZE:
                   # self.screen.handle_resize(event)
                    
            self.screen.draw_initial_screen(self.game_status, self.score, self.score_position)
            pygame.display.flip()

    def run_game(self):
        self.start_time = time.time()
        running_game = True
        self.show_map = True

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
                self.screen.draw_map_overlay(self.map_image, 15 - map_elapsed_time)
                if map_elapsed_time >= 15: 
                    self.show_map = False
                    self.start_time = time.time() 
            else:
                key = pygame.key.get_pressed()
                dx, dy = 0, 0
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    dx = -10
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    dx = 10
                if key[pygame.K_UP] or key[pygame.K_w]:
                    dy = -10
                if key[pygame.K_DOWN] or key[pygame.K_s]:
                    dy = 10
                self.character.move(dx, dy, self.walls, 5370, 5500, self.camera_x, self.camera_y)
                self.character.collect_key(self.keys)

                self.camera_x = max(0, min(self.character.rect.x - self.screen.screen_width // 4, 2010))
                self.camera_y = max(0, min(self.character.rect.y - self.screen.screen_height // 4, 1100))

                self.screen.screen.fill("yellow")

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