import pygame, random as rand
import sys

pygame.init()
clock = pygame.time.Clock()

SCREENWIDTH = 1000
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT], pygame.RESIZABLE)

velocity = 2


class Mask:
    def __init__(self, x, y, width, height, colour, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.velocity = velocity

    def draw_updatescreen(self):
        self.shape = pygame.Surface((self.x, self.y))
        self.shape.fill(self.colour)
        self.originalshape = self.shape.copy()
        self.rect = self.shape.get_rect()
        self.rect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)

    
    def movement(self):
        if self.y < 550:
            self.y += self.velocity
        else:
            self.velocity = rand.randint(3, 10)
            self.y = 0

    def update(self, x, y, width, height, colour, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.velocity = velocity

    def functions(self):
        self.draw_updatescreen()
        self.movement()
        self.update(self.x, self.y, self.width, self.height, self.colour, self.velocity)

test = Mask(100, 0, 50, 50, (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)), 2)
test2 = Mask(400, 0, 50, 50, (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)), 2)
test3 = Mask(800, 0, 50, 50, (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)), 2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    SCREEN.fill("white")

    test.functions()
    test2.functions()
    test3.functions()

    clock.tick(60)

    pygame.display.update()