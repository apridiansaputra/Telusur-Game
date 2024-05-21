import sys
sys.path.append('D:\PBO\Tubes\Telusur-Game')
import main
import pygame

# Initialize Pygame
pygame.init()

# Initialize the display
pygame.display.init()

def test_character_move():
    pygame.display.set_mode()
    character = main.Character()
    walls = [main.Wall((100, 100), "Wall 1", "Theme 1"), main.Wall((200, 200), "Wall 2", "Theme 2")]
    screen_width = 800
    screen_height = 600
    camera_x = 0
    camera_y = 0

    # Set the video mode
    pygame.display.set_mode((screen_width, screen_height))

    # Test moving character to the right
    character.move(1, 0, walls, screen_width, screen_height, camera_x, camera_y)
    assert character.position == (11, 50)

    # Test moving character to the left
    character.move(-1, 0, walls, screen_width, screen_height, camera_x, camera_y)
    assert character.position == (10, 50)

    # Test moving character upwards
    character.move(0, -1, walls, screen_width, screen_height, camera_x, camera_y)
    assert character.position == (10, 49)

    # Test moving character downwards
    character.move(0, 1, walls, screen_width, screen_height, camera_x, camera_y)
    assert character.position == (10, 50)

def test_character_collect_key():
    character = main.Character()
    key = main.Key((100, 100))
    keys = [key]

    # Test collecting a key
    character.collect_key(keys)
    assert character.inventory == [key]

def test_character_check_door_collision():
    character = main.Character()
    door = main.Door((100, 100))

    # Test collision with door when character has no keys
    assert character.check_door_collision(door) == False

    # Test collision with door when character has a key
    character.inventory.append(main.Key((200, 200)))
    assert character.check_door_collision(door) == True

def test_wall_draw():
    wall = main.Wall((100, 100), "Wall 1", "Theme 1")
    screen = main.Screen()
    camera_x = 0
    camera_y = 0

    # Test drawing wall on screen
    wall.draw(screen, camera_x, camera_y)
    assert screen.drawn_objects == [(100, 100, "Wall 1", "Theme 1")]

if __name__ == "__main__":
    test_character_move()
    test_character_collect_key()
    test_character_check_door_collision()
    test_wall_draw()