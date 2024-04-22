import pygame
import os

class Character:
    def __init__(self):
        self.player  = pygame.Rect(32, 32, 32, 32)
        self.has_key = False

    def movePlayer(self, dx, dy):
        if dx != 0:
            self.move(dx, 0)
        if dy != 0:
            self.move(0, dy)

        for wall in walls:
            if self.player.colliderect(wall.shape):
                if dx > 0:
                    self.player.right = wall.shape.left
                if dx < 0:
                    self.player.left = wall.shape.right
                if dy > 0:
                    self.player.bottom = wall.shape.top
                if dy < 0:
                    self.player.top = wall.shape.bottom

        if not self.has_key:
            if self.player.left < 0:
                self.player.left = 0
            if self.player.right > 640:
                self.player.right = 640
            if self.player.top < 0:
                self.player.top = 0
            if self.player.bottom > 480:
                self.player.bottom = 480

    def move(self, dx, dy):
        self.player.x += dx
        self.player.y += dy

class Wall:
    def __init__(self, pos) :
        walls.append(self)
        self.shape = pygame.Rect(pos[0], pos[1], 32, 32)

class Key:
    def __init__(self, pos) :
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.collect_key = False


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Labirin PBO")
screen = pygame.display.set_mode((640, 480))

clock   = pygame.time.Clock()
character  = Character()
walls   = []
keys    = []


obstacle = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W                K W",
    "W       WWWWWW     W",
    "W   WWWW       W   W",
    "W   W        WWWW  W",
    "W WWW  WWWW        W",
    "W   W     W W      W",
    "W   W     W   WWW WW",
    "W   WWW WWW   W W  W",
    "W     W   W   W W  W",
    "WWW   W   WWWWW W  W",
    "W W      WW        W",
    "W W   WWWW   WWW   W",
    "W      W   E   W   W",
    "WWWWWWWWWWWWWWWWWWWW",
]

x = y = 0
for row in obstacle:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            close_door = pygame.Rect(x, y, 32, 32)
        if col == "K":
            keys.append(Key((x, y)))
        x += 32
    y += 32
    x = 0


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        character.movePlayer(-4, 0)
    if key[pygame.K_RIGHT]:
        character.movePlayer(4, 0)
    if key[pygame.K_UP]:
        character.movePlayer(0, -4)
    if key[pygame.K_DOWN]:
        character.movePlayer(0, 4)

    for key in keys:
        if not key.collect_key and character.player.colliderect(key.rect):
            key.collect_key = True
            character.has_key = True

    if character.has_key and character.player.colliderect(close_door):
        running = False
                                                              
    screen.fill((0, 0, 0))

    for wall in walls:
        pygame.draw.rect(screen, (65, 176, 110), wall.shape)

    for key in keys:
        if not key.collect_key:
            pygame.draw.rect(screen, (255, 196, 112), key.rect)
    
    pygame.draw.rect(screen, (81, 68, 52), close_door)
    pygame.draw.rect(screen, (255, 112, 112), character.player)
    pygame.display.flip()
    clock.tick(360)

pygame.quit()


# Cara agar ada homescreen sebelum dan setelah permainan
# Cara mengubah rectangel pygame jadi gambar 
# Cara nambah obstacle/bentuk sesuai level
# Cara nampilin waktu & kondisi game over saat waktu selesai
# Cara nampilin score akhir