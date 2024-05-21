import sys
sys.path.append('D:\PBO\Tubes\Telusur-Game')
import unittest
from screen import Screen

class TestScreen(unittest.TestCase):
    def setUp(self):
        self.screen = Screen()

    def test_draw_initial_screen(self):
        # Test case 1: game_status and score are None
        self.screen.draw_initial_screen()
        # Add assertions here

        # Test case 2: game_status and score are provided
        self.screen.draw_initial_screen(game_status="Start", score=0)
        # Add assertions here

    def test_draw_result_screen(self):
        # Test case 1: message and score are provided
        self.screen.draw_result_screen("Game Over", 100)
        # Add assertions here

        # Test case 2: message and score are empty
        self.screen.draw_result_screen("", 0)
        # Add assertions here

    def test_draw_timer(self):
        # Test case 1: time_left is positive
        self.screen.draw_timer(60)
        # Add assertions here

        # Test case 2: time_left is zero
        self.screen.draw_timer(0)
        # Add assertions here

        # Test case 3: time_left is negative
        self.screen.draw_timer(-10)
        # Add assertions here

    def test_draw_initial_screen_with_invalid_score(self):
        # Test case: score is not an integer
        self.screen.draw_initial_screen(game_status="Start", score="Invalid")
        # Add assertions here

    def test_draw_result_screen_with_invalid_score(self):
        # Test case: score is not an integer
        self.screen.draw_result_screen("Game Over", "Invalid")
        # Add assertions here

    def test_draw_timer_with_invalid_time(self):
        # Test case: time_left is not an integer
        self.screen.draw_timer("Invalid")
        # Add assertions here

    def test_draw_timer_with_large_time(self):
        # Test case: time_left is a large positive number
        self.screen.draw_timer(999999999)
        # Add assertions here

    def test_draw_timer_with_large_negative_time(self):
        # Test case: time_left is a large negative number
        self.screen.draw_timer(-999999999)
        # Add assertions here

    def test_draw_initial_screen_with_game_status(self):
        # Test case: game_status is provided, score is None
        self.screen.draw_initial_screen(game_status="Start")
        # Add assertions here

        # Test case: game_status is an empty string, score is None
        self.screen.draw_initial_screen(game_status="")
        # Add assertions here

    def test_draw_result_screen_with_empty_message(self):
        # Test case: message is an empty string, score is provided
        self.screen.draw_result_screen("", 100)
        # Add assertions here

        # Test case: message is an empty string, score is zero
        self.screen.draw_result_screen("", 0)
        # Add assertions here

    def test_draw_initial_screen_with_both_parameters_none(self):
        # Test case: both game_status and score are None
        self.screen.draw_initial_screen(game_status=None, score=None)
        # Add assertions here

    def test_draw_result_screen_with_both_parameters_none(self):
        # Test case: both message and score are None
        self.screen.draw_result_screen(message=None, score=None)
        # Add assertions here

if __name__ == '__main__':
    unittest.main()