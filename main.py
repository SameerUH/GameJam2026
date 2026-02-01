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

instructions_lines = [
    "The Masquerade Maskers have broken into the ball! Help save the civillians by clicking on the masks before they reach the ground.",
    "Instructions:",
    "1. Click on the falling masks to score points.",
    "2. Catch Masquerade masks for +20 points.",
    "3. Catch COVID masks for +5 points (Rare!!).",
    "4. Avoid Faces, as they deduct -10 points.",
    "5. If your score drops below 0, it's game over.",
    "6. Press ESC to pause/resume the game.",
    "7. Press R to restart after game over.",
    "Enjoy the game and good luck!",
    "PRESS SPACE TO START"]


running = "running"
paused = "paused"
game_over = "game over"
instructions = "instructions"

game_state = instructions

clock = pygame.time.Clock()

SCREENWIDTH = 1000
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT], pygame.RESIZABLE)

BACKGROUND_COLOUR = (182, 151, 121)

velocity = 2

mask_images = []
covid_images = []
face_images = []
mask_weights = [6, 1, 4]  # Masquerade, COVID, Face

def get_random_mask(allmasks, weights):
    category = rand.choices(allmasks, weights=weights, k=1)[0]
    return rand.choice(category)

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
        image, self.filename = get_random_mask(allmasks, mask_weights)
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
            self.velocity = rand.randint(3, 5)
            self.rect.y = 0
            image, self.filename = get_random_mask(allmasks, mask_weights)
            self.original_image = pygame.transform.scale(image, (self.width, self.height))
            if "Masquerade" in old_filename:
                return -10
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
                    image, self.filename = get_random_mask(allmasks, mask_weights)
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
high_score = 100

player_score_font = pygame.font.Font('freesansbold.ttf', 50)
player_score_text = player_score_font.render("SCORE: " + str(player_score), True, "black")
player_score_rect = player_score_text.get_rect()
player_score_rect.center = (150, 950)

overlay_font = pygame.font.Font('freesansbold.ttf', 80)
small_font = pygame.font.Font('freesansbold.ttf', 40)

paused_text = overlay_font.render("PAUSED", True, "black")
paused_rect = paused_text.get_rect()
paused_rect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)

gameover_text = overlay_font.render("GAME OVER", True, "black")
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)

restart_text = small_font.render("Press R to Restart", True, "black")
restart_text_rect = restart_text.get_rect()
restart_text_rect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2 + 100)

instructions_font = pygame.font.Font('freesansbold.ttf', 20)


while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state != game_over:
                if game_state == running:
                    game_state = paused
                elif game_state == paused:
                    game_state = running
            if event.key == pygame.K_SPACE and game_state == instructions:
                game_state = running
    

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_clicked = True
    else:
        mouse_clicked = False

    
    SCREEN.fill(BACKGROUND_COLOUR)

    screen_rect = SCREEN.get_rect()


    if game_state == instructions:
        overlay = pygame.Surface((screen_rect.size))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        for i, line in enumerate(instructions_lines):
            instruction_text = instructions_font.render(line, True, "white")
            instruction_rect = instruction_text.get_rect(center=(screen_rect.centerx, 100 + i * 50))
            SCREEN.blit(instruction_text, instruction_rect)

    if game_state == running:
        for object in objects:
            player_score += object.update()
        
        if player_score > high_score:
            high_score = player_score
    
    if player_score < 0:
        game_state = game_over

    if game_state == paused:
        paused_rect = paused_text.get_rect(center=screen_rect.center)
        SCREEN.blit(paused_text, paused_rect)
    elif game_state == game_over:
        gameover_rect = gameover_text.get_rect(center=screen_rect.center)
        SCREEN.blit(gameover_text, gameover_rect)
        restart_text_rect = restart_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 100))
        SCREEN.blit(restart_text, restart_text_rect)
        score_text = small_font.render(f"High Score: {high_score}", True, "black")
        score_text_rect = score_text.get_rect(center=(screen_rect.centerx, 50))
        SCREEN.blit(score_text, score_text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_score = 100

            for object in objects:
                object.rect.y = 0

            game_state = running

    floor = pygame.draw.rect(SCREEN, "white", (0, 900, 1950, 10))
    player_score_text = player_score_font.render("SCORE: " + str(player_score), True, "black")
    SCREEN.blit(player_score_text, (player_score_rect))

    clock.tick(60)

    pygame.display.update()