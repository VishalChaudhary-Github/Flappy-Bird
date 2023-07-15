import random
import pygame
pygame.init()

# Creating the game window and setting title & icon
game_window = pygame.display.set_mode((288, 512))
icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption('Flappy Bird')

# Loading Background image and message
bg_image = random.choice(('sprites/background-day.png', 'sprites/background-night.png'))
message = pygame.image.load('sprites/message.png')
background = pygame.image.load(bg_image)

# Loading Bird images
bluebird = ('sprites/bluebird-upflap.png', 'sprites/bluebird-midflap.png', 'sprites/bluebird-downflap.png')
redbird = ('sprites/redbird-upflap.png', 'sprites/redbird-midflap.png', 'sprites/redbird-downflap.png')
yellowbird = ('sprites/yellowbird-upflap.png', 'sprites/yellowbird-midflap.png', 'sprites/yellowbird-downflap.png')

# Loading pipe images and setting positions
pipes = ('sprites/pipe-green.png', 'sprites/pipe-red.png')
positions = ((-170, 250), (-220, 200), (-245, 175), (-120, 300), (-95, 325))

# loading score
score_img = ('sprites/0.png', 'sprites/1.png', 'sprites/2.png', 'sprites/3.png', 'sprites/4.png',
             'sprites/5.png', 'sprites/6.png', 'sprites/7.png', 'sprites/8.png', 'sprites/9.png')

# Loading game over image
game_over_img = pygame.image.load('sprites/gameover.png')

# Loading Sound effects
hit = pygame.mixer.Sound('audio/hit.ogg')
die = pygame.mixer.Sound('audio/die.ogg')
point = pygame.mixer.Sound('audio/point.ogg')
wing = pygame.mixer.Sound('audio/wing.ogg')
swoosh = pygame.mixer.Sound('audio/swoosh.ogg')


def score_render(value, surface):
    if len(str(value)) == 1:
        img = score_img[value]
        score_surf = pygame.image.load(img)
        surface.blit(score_surf, (136, 78))
    else:
        i = iter(str(value))
        first = next(i)
        second = next(i)
        img1 = score_img[int(first)]
        img2 = score_img[int(second)]
        surf1 = pygame.image.load(img1)
        surf2 = pygame.image.load(img2)
        surface.blit(surf1, (120, 78))
        surface.blit(surf2, (140, 78))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 127
        self.y_pos = 188
        self.images = random.choice((bluebird, redbird, yellowbird))
        self.flap_change = 0
        self.change = 1
        self.vel = 0
        self.gravity = 0
        self.angle = 0
        self.angle_change = 30
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 30, 20)

    def draw(self, surface):
        flap = pygame.image.load(self.images[self.flap_change])
        flap_angle = pygame.transform.rotate(flap, self.angle)
        surface.blit(flap_angle, (self.x_pos, self.y_pos))
        self.flap_change += self.change
        if self.flap_change >= 2:
            self.change = -1
        elif self.flap_change <= 0:
            self.change = 1

    def update(self):
        self.y_pos += self.vel
        self.vel += self.gravity
        if self.vel > 12:
            self.angle -= self.angle_change
        if self.angle <= -90:
            self.angle_change = 0

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos + 6


class Base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 0
        self.y_pos = 400
        self.speed = -5
        self.image = pygame.image.load('sprites/base.png')
        self.rect = pygame.Rect(self.x_pos, self.y_pos - 10, 336, 112 + 10)

    def draw(self, surface):
        surface.blit(self.image, (self.x_pos, self.y_pos))

    def update(self):
        if self.x_pos <= -47:
            self.x_pos = 0
        self.x_pos += self.speed
        self.rect.x = self.x_pos


class Pipe(pygame.sprite.Sprite):
    pos_list = []
    score_bool = True

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed_x = 0
        self.image = pygame.image.load(random.choice(pipes))
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 52, 320)

    def draw(self, surface):
        if self.y_pos < 0:
            rotated_img = pygame.transform.rotate(self.image, 180)
            surface.blit(rotated_img, (self.x_pos, self.y_pos))
        elif self.y_pos > 0:
            surface.blit(self.image, (self.x_pos, self.y_pos))

    def update(self):
        if self.x_pos <= -52:
            self.x_pos = 288
            Pipe.score_bool = True
            if self.y_pos < 0:
                y_up, y_down = random.choice(positions)
                self.y_pos = y_up
                Pipe.pos_list.append(y_down)
            elif self.y_pos > 0:
                self.y_pos = Pipe.pos_list[0]
                Pipe.pos_list.clear()
        self.x_pos += self.speed_x

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


base = Base()
bird = Bird()

pipe_pos = random.choice(positions)
up = Pipe(288, pipe_pos[0])
down = Pipe(288, pipe_pos[1])

rand_pos = random.choice(positions)
other_up = Pipe(454, rand_pos[0])
other_down = Pipe(454, rand_pos[1])

group_for_collision_detection = pygame.sprite.Group()
group_for_collision_detection.add(up, down, other_up, other_down)
clock = pygame.time.Clock()

# Game Loop
hit_die_play_once = True
score = 0
game_start = False
game_over = False
down_fall = False
running = True
while running:
    clock.tick(25.0)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_start:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    swoosh.play()
                    game_start = True
        if game_start and (not game_over):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.vel = -12
                    bird.gravity = 1.5
                    bird.angle = 30
                    bird.angle_change = 30
                    up.speed_x = -6.5
                    down.speed_x = -6.5
                    other_up.speed_x = -6.5
                    other_down.speed_x = -6.5
                    wing.play()

    # Game Logic
    base.update()
    bird.update()
    up.update()
    down.update()
    other_up.update()
    other_down.update()
    if ((up.x_pos <= bird.x_pos) or (other_up.x_pos <= bird.x_pos)) and Pipe.score_bool:
        score += 1
        point.play()
        Pipe.score_bool = False

    if pygame.sprite.collide_rect(bird, base):
        bird.vel = 0
        bird.gravity = 0
        bird.change = 0
        game_over = True

    bird_pipes_collision = pygame.sprite.spritecollide(bird, group_for_collision_detection, dokill=False)
    if len(bird_pipes_collision) >= 1:
        if hit_die_play_once:
            hit.play()
        game_over = True

    if game_over:
        up.speed_x = 0
        down.speed_x = 0
        other_up.speed_x = 0
        other_down.speed_x = 0
        base.speed = 0
        if hit_die_play_once:
            die.play()
            hit_die_play_once = False

    # Rendering the graphics
    game_window.blit(background, (0, 0))
    if not game_start:
        game_window.blit(message, (52, 66))
    if game_start:
        up.draw(game_window)
        down.draw(game_window)
        other_up.draw(game_window)
        other_down.draw(game_window)
    base.draw(game_window)
    if game_start:
        bird.draw(game_window)
        score_render(score, game_window)
    if game_over:
        game_window.blit(game_over_img, (48, 188))

    # Updating the Display
    pygame.display.flip()

pygame.quit()