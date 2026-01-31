import pygame, random as rand
import sys

"""
TO-DO:
xxx Make spinning squares.
xxx Add images to squares
xxx Make clickable squares.
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
covid_images = []
face_images = []

for i in range(1, 20):
    img = pygame.image.load(f"Masquerade/mask_{i}.png").convert_alpha()
    mask_images.append(img)

for i in range(1, 9):
    img = pygame.image.load(f"COVID/covid_{i}.png").convert_alpha()
    covid_images.append(img)

for i in range(1, 9):
    img = pygame.image.load(f"Faces/face_{i}.png").convert_alpha()
    face_images.append(img)

allmasks = [mask_images, covid_images, face_images]

class Mask:
    def __init__(self, x, y, width, height, velocity, allmasks):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.original_image = pygame.transform.scale(rand.choice(allmasks), (width, height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.angle = 0
        self.rotation_speed = rand.randint(-3, 3)
        self.hitbox = (self.rect.x, self.rect.y, 55, 55)

    def draw_updatescreen(self):
        SCREEN.blit(self.image, self.rect)
        self.hitbox = (self.rect.x + 5, self.rect.y + 5, 100, 100)
        pygame.draw.rect(SCREEN, "red", self.hitbox, 2)

    def movement(self):
        if self.rect.y < 800:
            self.rect.y += self.velocity
        else:
            self.velocity = rand.randint(3, 10)
            self.rect.y = 0
            self.original_image = pygame.transform.scale(rand.choice(rand.choice(allmasks)), (self.width, self.height))
    
    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center = old_center)
    
    def interaction(self, mouse_pos, mouse_clicked):
        if mouse_pos[1] < self.hitbox[1] + self.hitbox[3] and mouse_pos[1] > self.hitbox[1]:
            if mouse_pos[0] > self.hitbox[0] and mouse_pos[0] < self.hitbox[0] + self.hitbox[2]:
                if mouse_clicked:
                    self.rect.y = 0
                    self.original_image = pygame.transform.scale(rand.choice(rand.choice(allmasks)), (self.width, self.height))

    def update(self):
        self.movement()
        self.rotate()
        self.draw_updatescreen()
        self.interaction(mouse_pos, mouse_clicked)


objects = []

x_coordinates = [i for i in range(100, 1800, 200)]
for x in x_coordinates:
    objects.append(Mask(x, 0, 100, 100, 2, allmasks[rand.randint(0, 2)]))

mouse_clicked = False

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_clicked = True
    else:
        mouse_clicked = False

    
    SCREEN.fill(BACKGROUND_COLOUR)

    for object in objects:
        object.update()

    floor = pygame.draw.rect(SCREEN, "white", (0, 900, 1950, 10))

    clock.tick(60)

    pygame.display.update()