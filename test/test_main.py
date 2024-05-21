import sys
sys.path.append('D:\PBO\Tubes\Telusur-Game')
import unittest
from unittest.mock import patch
import main

class TestMain(unittest.TestCase):
    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_main(self, mock_init, mock_set_mode, mock_set_caption, mock_clock):
        # Arrange
        expected_caption = 'Telusur'
        
        # Act
        main.main()
        
        # Assert
        mock_init.assert_called_once()
        mock_set_mode.assert_called_once_with((main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
        mock_set_caption.assert_called_once_with(expected_caption)
        mock_clock.assert_called_once()

if __name__ == '__main__':
    unittest.main()