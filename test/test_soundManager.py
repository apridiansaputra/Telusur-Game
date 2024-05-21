import sys
sys.path.append('D:\PBO\Tubes\Telusur-Game')
import unittest
from soundManager import SoundManager

class TestSoundManager(unittest.TestCase):
    def setUp(self):
        self.sound_manager = SoundManager()

    def test_play_background_music(self):
        # Test that play_background_music method plays the background music
        self.sound_manager.play_background_music()
        # Add assertion here to check if the background music is playing

    def test_play_enter_sound(self):
        # Test that play_enter_sound method plays the enter sound
        self.sound_manager.play_enter_sound()
        # Add assertion here to check if the enter sound is playing

    def test_play_wall_hit_sound(self):
        # Test that play_wall_hit_sound method plays the wall hit sound
        self.sound_manager.play_wall_hit_sound()
        # Add assertion here to check if the wall hit sound is playing

    def test_play_key_pickup_sound(self):
        # Test that play_key_pickup_sound method plays the key pickup sound
        self.sound_manager.play_key_pickup_sound()
        # Add assertion here to check if the key pickup sound is playing

    def test_play_success_sound(self):
        # Test that play_success_sound method plays the success sound
        self.sound_manager.play_success_sound()
        # Add assertion here to check if the success sound is playing

    def test_stop_background_music(self):
        # Test that stop_background_music method stops the background music
        self.sound_manager.stop_background_music()
        # Add assertion here to check if the background music is stopped

    def test_stop_all_sounds(self):
        # Test that stop_all_sounds method stops all sounds
        self.sound_manager.stop_all_sounds()
        # Add assertion here to check if all sounds are stopped

if __name__ == '__main__':
    unittest.main()