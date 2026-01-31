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
        self.image = pygame.transform.scale(rand.choice(mask_images), (width, height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw_updatescreen(self):
        SCREEN.blit(self.image, self.rect)

    
    def movement(self):
        if self.rect.y < 550:
            self.rect.y += self.velocity
        else:
            self.velocity = rand.randint(3, 10)
            self.rect.y = 0

    def update(self):
        self.movement()
        self.draw_updatescreen()

test = Mask(100, 0, 100, 100, 2, mask_images)
test2 = Mask(400, 0, 100, 100, 2, mask_images)
test3 = Mask(800, 0, 100, 100, 2, mask_images)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    SCREEN.fill("white")

    test.update()
    test2.update()
    test3.update()

    clock.tick(60)

    pygame.display.update()