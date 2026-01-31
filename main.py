import pygame, random as rand
import sys

"""
TO-DO:
--- Make spinning squares.
--- Add images to squares
--- Make clickable squares.
--- Add sounds to game.
"""

pygame.init()
clock = pygame.time.Clock()

SCREENWIDTH = 1000
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT], pygame.RESIZABLE)

BACKGROUND_COLOUR = (182, 151, 121)

velocity = 2

mask_images = []

for i in range (1, 20):
    img = pygame.image.load(f"Masquerade/mask_{i}.png").convert_alpha()
    mask_images.append(img)

class Mask:
    def __init__(self, x, y, width, height, velocity, mask_images):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.original_image = pygame.transform.scale(rand.choice(mask_images), (width, height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.angle = 0
        self.rotation_speed = rand.randint(-3, 3)

    def draw_updatescreen(self):
        SCREEN.blit(self.image, self.rect)

    def movement(self):
        if self.rect.y < 550:
            self.rect.y += self.velocity
        else:
            self.velocity = rand.randint(3, 10)
            self.rect.y = 0
    
    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center = old_center)

    def update(self):
        self.movement()
        self.rotate()
        self.draw_updatescreen()

objects = []

x_coordinates = [100, 400, 800, 1000]
for x in x_coordinates:
    objects.append(Mask(x, 0, 100, 100, 2, mask_images))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    SCREEN.fill(BACKGROUND_COLOUR)

    for object in objects:
        object.update()

    clock.tick(60)

    pygame.display.update()