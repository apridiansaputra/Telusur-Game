import pygame
import os
import sys
import random
import time
from character import Character
from wall import Wall
from key import Key
from screen import Screen
from soundManager import SoundManager
from door import Door


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
             "surface": "./assets/theme/surface-grass-2.png"},
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
        self.score_position = (self.screen.screen.get_width() // 2, self.screen.screen.get_height() // 2 + 10)
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
                        if self.game_status == "success": 
                            self.reset_game() 
                            self.current_screen = "game"
                            self.sound_manager.stop_menu_sound()
                            self.sound_manager.play_game_sound()
                            self.map_start_time = time.time()
                            return
                        else:
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
                self.screen.draw_map_overlay(self.map_image, 12 - map_elapsed_time)
                if map_elapsed_time >= 12: 
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

                screen_size = self.screen.screen.get_size()
                image = pygame.image.load(self.selected_theme["surface"]).convert_alpha()
                scaled_image = pygame.transform.scale(image, screen_size)
                self.screen.screen.blit(scaled_image, (0, 0))

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

