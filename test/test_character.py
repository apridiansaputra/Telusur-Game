import sys
sys.path.append('D:\PBO\Tubes\Telusur-Game')
import unittest
import pygame
from character import Character

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.character = Character()

    def test_character_initialization(self):
        self.assertEqual(self.character.position, (50, 50))
        self.assertFalse(self.character.has_key)

    def test_character_movement(self):
        walls = []
        screen_width = 800
        screen_height = 600
        camera_x = 0
        camera_y = 0

        # Test moving character to the right
        self.character.move(10, 0, walls, screen_width, screen_height, camera_x, camera_y)
        self.assertEqual(self.character.position, (60, 50))

        # Test moving character to the left
        self.character.move(-10, 0, walls, screen_width, screen_height, camera_x, camera_y)
        self.assertEqual(self.character.position, (50, 50))

        # Test moving character upwards
        self.character.move(0, -10, walls, screen_width, screen_height, camera_x, camera_y)
        self.assertEqual(self.character.position, (50, 40))

        # Test moving character downwards
        self.character.move(0, 10, walls, screen_width, screen_height, camera_x, camera_y)
        self.assertEqual(self.character.position, (50, 50))

    def test_collect_key(self):
        class Key:
            def __init__(self, rect):
                self.rect = rect
                self.collected = False

        keys = [Key(pygame.Rect(50, 50, 10, 10)), Key(pygame.Rect(100, 100, 10, 10))]
        self.character.rect = pygame.Rect(55, 55, 10, 10)

        self.character.collect_key(keys)
        self.assertTrue(self.character.has_key)
        self.assertTrue(keys[0].collected)
        self.assertFalse(keys[1].collected)
        self.assertEqual(len(keys), 1)

if __name__ == '__main__':
    unittest.main()