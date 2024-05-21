import pygame

class Screen:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720 
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.font_title = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 60)
        self.font_info = pygame.font.Font(None, 48)
        self.font_timer = pygame.font.Font("./assets/fonts/AoboshiOne-Regular.ttf", 18)
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

        self.timer_bg = pygame.image.load("./assets/timer_backgoround.png").convert_alpha()

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
            start_button_rect = start_button_image.get_rect(center=(screen_width // 2 - 80, screen_height // 2 + 160))
            self.screen.blit(start_button_image, start_button_rect)
            exit_button_image = self.winner_exit
            exit_button_rect = exit_button_image.get_rect(center=(screen_width // 2 + 80, screen_height // 2 + 160))
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
            score_text = self.font_score.render(str(score), True, (139,	106, 72))
            if score_position is None:
                score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
            else:
                score_rect = score_text.get_rect(center=score_position)
            self.screen.blit(score_text, score_rect)

        if game_status != "success":
            start_button_rect = start_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 10))
            self.screen.blit(start_button_image, start_button_rect)

            exit_button_rect = exit_button_image.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            self.screen.blit(exit_button_image, exit_button_rect)

        pygame.display.flip()
        return start_button_rect, exit_button_rect
    
    def draw_timer(self, time_left):
        timer_text = self.font_timer.render(f"waktu: {time_left} detik", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(topleft=(10, 10))
        timer_bg_new = pygame.transform.scale(self.timer_bg, (timer_rect.width + 20, timer_rect.height + 20))
        self.screen.blit(timer_bg_new, (timer_rect.x - 10, timer_rect.y - 10))
        self.screen.blit(timer_text, timer_rect)

    def draw_map_overlay(self, map_image, time_left):
        self.screen.blit(pygame.transform.scale(map_image, (self.screen.get_width(), self.screen.get_height())), (0, -10))
        timer_text = self.font_timer.render(f"{time_left}", True, (255, 255, 255))
        self.screen.blit(timer_text, (map_image.get_width() + 10, 10))
        pygame.display.flip()