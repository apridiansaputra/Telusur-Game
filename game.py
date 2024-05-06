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

