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
    path = f"Masquerade/mask_{i}.png"
    img = pygame.image.load(f"Masquerade/mask_{i}.png").convert_alpha()
    mask_images.append((img, path))

for i in range(1, 9):
    path = f"COVID/covid_{i}.png"
    img = pygame.image.load(f"COVID/covid_{i}.png").convert_alpha()
    covid_images.append((img, path))

for i in range(1, 9):
    path = f"Faces/face_{i}.png"
    img = pygame.image.load(f"Faces/face_{i}.png").convert_alpha()
    face_images.append((img, path))

allmasks = [mask_images, covid_images, face_images]

class Mask:
    def __init__(self, x, y, width, height, velocity, allmasks):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        image, self.filename = rand.choice(rand.choice(allmasks))
        self.original_image = pygame.transform.scale(image, (self.width, self.height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.angle = 0
        self.rotation_speed = rand.randint(-3, 3)
        self.hitbox = (self.rect.x - 5, self.rect.y - 10, 110, 110)

    def draw_updatescreen(self):
        SCREEN.blit(self.image, self.rect)
        self.hitbox = (self.rect.x - 5, self.rect.y - 10, 110, 110)
        #pygame.draw.rect(SCREEN, "red", self.hitbox, 2)

    def movement(self):
        if self.rect.y < 800:
            self.rect.y += self.velocity
            return 0
        else:
            old_filename = self.filename
            self.velocity = rand.randint(3, 10)
            self.rect.y = 0
            image, self.filename = rand.choice(rand.choice(allmasks))
            self.original_image = pygame.transform.scale(image, (self.width, self.height))
            if "Masquerade" in old_filename:
                return -20
            return 0
    
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
                    image, self.filename = rand.choice(rand.choice(allmasks))
                    self.original_image = pygame.transform.scale(image, (self.width, self.height))
                    if "COVID" in self.filename:
                        return 5
                    elif "Masquerade" in self.filename:
                        return 20
                    elif "face" in self.filename:
                        return -10

        return 0

    def update(self):
        self.rotate()
        self.draw_updatescreen()
        score = self.interaction(mouse_pos, mouse_clicked)
        score += self.movement()
        return score


objects = []

x_coordinates = [i for i in range(100, 1800, 200)]
for x in x_coordinates:
    objects.append(Mask(x, 0, 100, 100, 2, allmasks))

mouse_clicked = False

player_score = 100
player_score_font = pygame.font.Font('freesansbold.ttf', 50)
player_score_text = player_score_font.render("SCORE: " + str(player_score), True, "black")
player_score_rect = player_score_text.get_rect()
player_score_rect.center = (150, 950)

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
        player_score += object.update()

    floor = pygame.draw.rect(SCREEN, "white", (0, 900, 1950, 10))
    player_score_text = player_score_font.render("SCORE: " + str(player_score), True, "black")
    SCREEN.blit(player_score_text, (player_score_rect))

    clock.tick(60)

    pygame.display.update()