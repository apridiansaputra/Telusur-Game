import pygame

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
