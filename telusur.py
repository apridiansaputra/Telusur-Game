import pygame
import os

class Character:
    def __init__(self):
        self.original_image = pygame.image.load("./assets/player.png")
        self.image = pygame.transform.scale(self.original_image, (60,60))
        self.player = self.image.get_rect()
        self.player.topleft = (0, 0)
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
            if self.player.right > 960:
                self.player.right = 960
            if self.player.top < 0:
                self.player.top = 0
            if self.player.bottom > 720:
                self.player.bottom = 720

    def move(self, dx, dy):
        self.player.x += dx
        self.player.y += dy

class Wall:
    def __init__(self, pos, desc) :
        walls.append(self)
        if desc == "horizontal":
            self.original_image = pygame.image.load("./assets/tembok-horizontal.png")
        if desc == "vertikal":
            self.original_image = pygame.image.load("./assets/tembok-vertikal.png")
        self.image = pygame.transform.scale(self.original_image, (60,60))
        self.shape = self.image.get_rect()
        self.shape.topleft = pos

class Key:
    def __init__(self, pos) :
        self.original_image = pygame.image.load("./assets/kunci.png")
        self.image = pygame.transform.scale(self.original_image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collect_key = False

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Labirin PBO")
screen = pygame.display.set_mode((960, 720))

clock   = pygame.time.Clock()
print(type(clock))
character  = Character()
walls   = []
keys    = []
background = pygame.image.load("./assets/surface.png").convert()


obstacle = [
    " HHHHHHHHHHHHHHV",
    "             K V",
    "V   HHHHHH     V",
    "V              V",
    "V              V",
    "V HHV  HHHH    V",
    "V   V       H  V",
    "V   V     H    V",
    "V   HHH HHH    V",
    "V     H   H    H",
    "V      H         E",
    "VVVVVVVVVVVVVVVV",
]

x = y = 0
for row in obstacle:
    for col in row:
        if col == "H":
            Wall((x, y), "horizontal")
        if col == "V":
            Wall((x, y), "vertikal")
        if col == "E":
            close_door = pygame.Rect(x, y, 60, 60)
        if col == "K":
            keys.append(Key((x, y)))
        x += 60
    y += 60
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
                                                              
    screen.blit(background, (0, 0))

    for wall in walls:
        screen.blit(wall.image, wall.shape)

    for key in keys:
        if not key.collect_key:
            screen.blit(key.image, key.rect)
    
    pygame.draw.rect(screen, (81, 68, 52), close_door)
    screen.blit(character.image, character.player)
    pygame.display.flip()
    clock.tick(360)

pygame.quit()


# Cara agar ada homescreen sebelum dan setelah permainan
# Cara mengubah rectangel pygame jadi gambar 
# Cara nambah obstacle/bentuk sesuai level
# Cara nampilin waktu & kondisi game over saat waktu selesai
# Cara nampilin score akhir