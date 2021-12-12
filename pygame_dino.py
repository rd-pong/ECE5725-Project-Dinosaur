# Run this in RPi only.

import time
import pygame
import os
import random
import sys
import keyboard
import RPi.GPIO as GPIO

#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb1')
#os.putenv('SDL_MOUSEDRV', 'TSLIB')  # Track mouse clicks on piTFT
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cb_27(channel):
    sys.exit()

pygame.init()

GPIO.add_event_detect(27, GPIO.RISING, callback=cb_27, bouncetime=300)

# Global Constants
SCREEN_HEIGHT = 240  # 0.291
SCREEN_WIDTH = 320
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BOMB = [pygame.image.load(os.path.join("Assets/Bomb", "bomb1.jpg"))]

RIVER = [pygame.image.load(os.path.join("Assets/River", "River1.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

CRY = pygame.image.load(os.path.join("Assets/Cry", "DinoDead.png"))

HEALTH = [pygame.image.load(os.path.join("Assets/Health", "Health.png")),
          pygame.image.load(os.path.join("Assets/Health", "Health.png")),
          pygame.image.load(os.path.join("Assets/Health", "Health.png")),
          pygame.image.load(os.path.join("Assets/Health", "Health.png"))]

OVER = pygame.image.load(os.path.join("Assets/Over", "Over.png"))

GOLDEN = [pygame.image.load(os.path.join("Assets/Health", "Golden3.png"))]

DIAMOND = [pygame.image.load(os.path.join("Assets/Health", "Diamond.png")),pygame.image.load(os.path.join("Assets/Health", "Diamond.png"))]

FLAME = [pygame.image.load(os.path.join("Assets/Other", "Flame.png"))]

SMALL_FLAME = pygame.image.load(os.path.join("Assets/Other", "Flame2.png"))
# initialize the rect of health icon
health_rect = [[SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 116], [SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 - 116],
               [SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 116]]


class Dinosaur:
    X_POS = 23.28  # dino X position
    Y_POS = 90.21 + 30 + 20  # dino Y position
    Y_POS_DUCK = 98.94 + 30 + 20  # duck Y position
    JUMP_VEL = 2.47  # jump variable

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False  # jump once
        self.dino_jump2 = False  # jump twice

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump(userInput)

        if self.step_index >= 10:
            self.step_index = 0
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self, userInput):
        self.image = self.jump_img
        if self.dino_jump:  # first jump
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.2037
        if userInput[pygame.K_DOWN] and self.dino_jump and not self.dino_jump2:  # second jump
            self.jump_vel = self.JUMP_VEL  # reset the direction of speed
            self.dino_jump2 = True

        if self.dino_rect.y > 120 + 20:  # dino touch the ground after jump
            self.dino_jump = False
            self.dino_jump2 = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = 90.21 + 30 + 20

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def getYPos(self):
        return self.dino_rect.y


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(232, 291)
        self.y = random.randint(14 + 10, 29 + 30)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(727, 873)
            self.y = random.randint(14 + 10, 29 + 30)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

### Obstacles
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 94.575 + 30 + 20

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 87.3 + 30 + 20

class Bomb(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 50.925 + 30 + 24

class River(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 101.85 + 30 + 20

class Health(Obstacle):
    def __init__(self, image):
        self.type = 3
        super().__init__(image, self.type)
        self.rect.y = random.randint(40, 120 + 20)

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 72.75 + 30 + 20
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

### Attacks
class Attack:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = 50

    def update(self):
        self.rect.x += 10
        if self.rect.x > 320:
            attacks.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Flame(Attack):
    def __init__(self, image, Y_pos):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = Y_pos - 15

### Treasures
class Treasure:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            treasures.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Golden(Treasure):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(40, 120 + 20)

class Diamond(Treasure):
    def __init__(self, image):
        self.type = 1
        super().__init__(image, self.type)
        self.rect.y = random.randint(40, 120 + 20)



def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, health, health_num, cheat, treasures, obstacle, attack, attacks
    run = True
    cheat = False
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 6
    health_num = 3
    x_pos_bg = 0
    y_pos_bg = 105.58 + 30 + 20
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 11)
    font2 = pygame.font.Font('freesansbold.ttf', 14)
    font3 = pygame.font.Font('freesansbold.ttf', 21)
    obstacles = []
    treasures = []
    attacks = []
    death_count = 0
    flame_num = 5

    def score():
        global points, game_speed
        if not cheat:
            points += 1
        if points % 130 == 0:
            game_speed += 0.3

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (271, 12.64)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    start_time = time.time()
    while run:
        # judge the behavior of the player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    points = 777
                    cheat = ~cheat
                if event.key == pygame.K_SPACE and not attacks and flame_num > 0:
                    flame_num -= 1
                    attacks.append(Flame(FLAME, player.dino_rect.y))
        SCREEN.fill((255, 255, 255))
        # draw cheat mode text
        if cheat:
            cheat_text = font.render("cheat mode", True, (255, 0, 0))
            cheatRect = cheat_text.get_rect()
            cheatRect.center = (270, 24.64)
            SCREEN.blit(cheat_text, cheatRect)
        userInput = pygame.key.get_pressed()
        # add flame every 500 points
        if points % 1000 == 0 and points != 0:
            flame_num += 1
        last_point = points
        player.draw(SCREEN)
        player.update(userInput)
        # add obstacles
        if len(obstacles) == 0:
            if random.randint(0, 5) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 5) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 5) == 2:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 5) == 3:
                obstacles.append(River(RIVER))
            elif random.randint(0, 5) == 4:
                obstacles.append(Bomb(BOMB))
            elif random.randint(0, 8) == 5:
                obstacles.append(Health(HEALTH))
        # update obstacles and judge whether collide or not
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(70)
                if not cheat:# add health
                    if obstacle.type == 3:
                        if health_num < 3:
                            health_num += 1
                        else:
                            points += 500
                    else:
                        health_num -= 1
                obstacles.pop()
                if (health_num == 0):
                    death_count += 1
                    menu(death_count)
        # update flame attack
        for attack in attacks:
            attack.draw(SCREEN)
            attack.update()
            if(obstacles):
                if attack.rect.colliderect(obstacles[0].rect):
                    obstacles.pop()
        # add treasures and update treasures
        if (time.time() - start_time > 3):
            if len(treasures) == 0:
                if random.randint(0,5) < 4:
                    treasures.append(Golden(GOLDEN))
                elif random.randint(0,5) == 5 or random.randint(0,5) == 4:
                    treasures.append(Diamond(DIAMOND))
            for treasure in treasures:
                treasure.draw(SCREEN)
                treasure.update()
                if treasure.rect.colliderect(obstacle.rect):
                    treasures.pop()
                if player.dino_rect.colliderect(treasure.rect) and treasure.type == 0:
                    if not cheat:
                        points += 100
                    treasures.pop()
                if player.dino_rect.colliderect(treasure.rect) and treasure.type == 1:
                    if not cheat:
                        points += 400
                    treasures.pop()
        # update health icon
        for i in range(0, health_num):
            SCREEN.blit(HEALTH[0], health_rect[i])

        # draw the flame count
        SCREEN.blit(SMALL_FLAME, [SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 116])
        flame_text = font2.render(str(flame_num), True, (255, 165, 0))
        flameRect = flame_text.get_rect()
        flameRect.center = (215, 14.64)
        SCREEN.blit(flame_text, flameRect)
        flame_text2 = font3.render("*", True, (255, 165, 0))
        flameRect2 = flame_text2.get_rect()
        flameRect2.center = (202, 19.64)
        SCREEN.blit(flame_text2, flameRect2)
        # add flame every 500 points (in case a treasure is eaten)
        if points // 1000 != last_point // 1000:
            flame_num += 1

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, title
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 14)
        title_font = pygame.font.Font('freesansbold.ttf', 22)
        # initialize the start menu and death menu
        if death_count == 0:
            title = title_font.render("Baby Dino Adventure", True, (0, 0, 0))
            text = font.render("Press any Key to Start", True, (0, 0, 0))
            titleRect = title.get_rect()
            titleRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
            SCREEN.blit(title, titleRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 5.82, SCREEN_HEIGHT // 2 - 40.74 + 30))
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 5.82 - 40, SCREEN_HEIGHT // 2 - 40.74 + 30))
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 5.82 + 40, SCREEN_HEIGHT // 2 - 40.74 + 30))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 14.55)
            SCREEN.blit(score, scoreRect)
            SCREEN.blit(OVER, (SCREEN_WIDTH // 2 - 10.82, SCREEN_HEIGHT // 2 - 87.74))
            SCREEN.blit(CRY, (SCREEN_WIDTH // 2 - 10.82, SCREEN_HEIGHT // 2 - 47.74))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
        SCREEN.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)