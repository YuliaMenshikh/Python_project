import pygame
from pygame.locals import *
import random
import sys
from images import Images

class StrawberryJump:
    FIELD_X_MIN = -25
    FIELD_X_MAX = 825
    MAX_MOVEMENT_RIGHT = 15
    MAX_MOVEMENT_LEFT = -15
    RIGHT_DIRECTION = 0
    LEFT_DIRECTION = 1
    DOWN_DIRECTION = 1
    UP_DIRECTION = 0
    DIFFERENCE = 200
    CHECK_DIFFERENCE = 600
    JUMP = 15
    SPRING_JUMP = 40
    PLATFORM_SPEED = 7
    MONSTER_SPEED = 5
    MONSTER_SPEED_UP = 2
    MAX_MONSTER_OFFSET = 20
    MOVE_CAM = 10
    GREEN_PLATFORM = 0
    BLUE_PLATFORM = 1
    RED_PLATFORM = 2
    PLATFORM_X_MIN = 0
    PLATFORM_X_MAX = 700
    MONSTER_X_MIN = 0
    MONSTER_X_MAX = 720
    MONSTER_1 = 1
    MONSTER_2 = 2
    MONSTER_3 = 3
    SCORE_PLACE = (25, 25)
    PLAYER_WIDTH = 10
    PLATFORM_WIDTH = 15
    PLATFORM_HIGHT = 5
    SPRING_WIDTH = 5
    MONSTER_WIDTH = 5

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        self.score = 0
        self.direction = 0
        self.coordX = 400
        self.coordY = 300
        self.platforms = [[400, 500, 0, 0]] #[положение по оси X, по оси Y, вид, напрвление движения/ сломана или нет]
        self.springs = [] #[положение по оси X, по оси Y, состояние]
        self.monsters = []#[положение по оси X, по  Y, сдвиг по Y, up/down, вид, напрвление движения]
        self.cam = 0
        self.jump = 0
        self.gravity = 0
        self.movement = 0
        self.isRed = 0
        self.images = Images()

    def move(self):
        """движение по оси X"""
        key = pygame.key.get_pressed()

        if key[K_RIGHT]:
            if self.movement < self.MAX_MOVEMENT_RIGHT:
                self.movement += 1
            self.direction = self.RIGHT_DIRECTION
        elif key[K_LEFT]:
            if self.movement > self.MAX_MOVEMENT_LEFT:
                self.movement -= 1
            self.direction = self.LEFT_DIRECTION
        else:
            if self.movement > 0:
                self.movement -= 1
            elif self.movement < 0:
                self.movement += 1

    def physics(self):
        """падение/прыжок"""
        if not self.jump:
            self.coordY += self.gravity
            self.gravity += 1
        elif self.jump:
            self.coordY -= self.jump
            self.jump -= 1

    def side_control(self):
        if self.coordX > self.FIELD_X_MAX:
            self.coordX = self.FIELD_X_MIN
        elif self.coordX < self.FIELD_X_MIN:
            self.coordX = self.FIELD_X_MAX

    def draw_red_player(self):
        if not self.direction:
            if self.jump:
                self.screen.blit(self.images.player_right_1_red, (self.coordX, self.coordY - self.cam))
            else:
                self.screen.blit(self.images.player_right_red, (self.coordX, self.coordY - self.cam))
        else:
            if self.jump:
                self.screen.blit(self.images.player_left_1_red, (self.coordX, self.coordY - self.cam))
            else:
                self.screen.blit(self.images.player_left_red, (self.coordX, self.coordY - self.cam))
        self.isRed -= 2

    def draw_player(self):
        if not self.direction:
            if self.jump:
                self.screen.blit(self.images.player_right_1, (self.coordX, self.coordY - self.cam))
            else:
                self.screen.blit(self.images.player_right, (self.coordX, self.coordY - self.cam))
        else:
            if self.jump:
                self.screen.blit(self.images.player_left_1, (self.coordX, self.coordY - self.cam))
            else:
                self.screen.blit(self.images.player_left, (self.coordX, self.coordY - self.cam))

    def player(self):
        """передвижение игрока"""
        self.side_control()
        self.move()
        self.physics()

        self.coordX += self.movement
        if self.coordY - self.cam <= self.DIFFERENCE:
            self.cam -= self.MOVE_CAM
        
        if (self.isRed):
            self.draw_red_player()
        else:
            self.draw_player()

    def check_platforms(self):
        """генерация новых платформ и пружин"""
        for p in self.platforms:
            check = self.platforms[1][1] - self.cam
            if check > self.CHECK_DIFFERENCE:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = self.GREEN_PLATFORM
                elif platform < 900:
                    platform = self.BLUE_PLATFORM
                else:
                    platform = self.RED_PLATFORM

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100

    def draw_platform(self):
        """прорисовка платформ"""
        for p in self.platforms:
            if p[2] == self.GREEN_PLATFORM:
                self.screen.blit(self.images.green_platform, (p[0], p[1] - self.cam))
            elif p[2] == self.BLUE_PLATFORM:
                self.screen.blit(self.images.blue_platform, (p[0], p[1] - self.cam))
            elif p[2] == self.RED_PLATFORM:
                if not p[3]:
                    self.screen.blit(self.images.red_platform, (p[0], p[1] - self.cam))
                else:
                    self.screen.blit(self.images.red_platform_1, (p[0], p[1] - self.cam))

    def update_platforms(self):
        """обновление платформ"""
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.images.green_platform.get_width() - self.PLATFORM_WIDTH, self.images.green_platform.get_height() - self.PLATFORM_HIGHT)
            position = pygame.Rect(self.coordX, self.coordY, self.images.player_right.get_width() - self.PLAYER_WIDTH, self.images.player_right.get_height())
            if rect.colliderect(position) and self.gravity and self.coordY < (p[1] - self.cam):
                if p[2] != self.RED_PLATFORM:
                    self.jump = self.JUMP
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == self.BLUE_PLATFORM:
                if p[-1] == self.RIGHT_DIRECTION:
                    p[0] += self.PLATFORM_SPEED
                    if p[0] > self.PLATFORM_X_MAX:
                        p[-1] = self.LEFT_DIRECTION
                else:
                    p[0] -= self.PLATFORM_SPEED
                    if p[0] <= self.PLATFORM_X_MIN:
                        p[-1] = self.RIGHT_DIRECTION
        self.draw_platform()
        self.check_platforms()

    def draw_springs(self):
        """прорисовка пружин"""
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.images.spring_1, (spring[0], spring[1] - self.cam))
            else:
                self.screen.blit(self.images.spring, (spring[0], spring[1] - self.cam))
            position = pygame.Rect(self.coordX, self.coordY, self.images.player_right.get_width(), self.images.player_right.get_height())
            rect = pygame.Rect(spring[0], spring[1], self.images.spring.get_width() - self.SPRING_WIDTH, self.images.spring.get_height())
            if rect.colliderect(position):
                self.jump = self.SPRING_JUMP
                self.cam -= 10 * self.MOVE_CAM

    def draw_monster(self):
        """прорисовка монстров"""
        for m in self.monsters:
            if m[4] == self.MONSTER_1:
                self.screen.blit(self.images.monster1, (m[0], m[1] - self.cam - m[2]))
                rect = pygame.Rect(m[0], m[1], self.images.monster1.get_width() - self.MONSTER_WIDTH, self.images.monster1.get_height())
            elif m[4] == self.MONSTER_2:
                self.screen.blit(self.images.monster2, (m[0], m[1] - self.cam - m[2]))
                rect = pygame.Rect(m[0], m[1], self.images.monster2.get_width() - self.MONSTER_WIDTH, self.images.monster2.get_height())
            else:
                self.screen.blit(self.images.monster3, (m[0], m[1] - self.cam - m[2]))
                rect = pygame.Rect(m[0], m[1], self.images.monster3.get_width() - self.MONSTER_WIDTH, self.images.monster3.get_height())
            position = pygame.Rect(self.coordX, self.coordY, self.images.player_right.get_width(),
                                   self.images.player_right.get_height())
            if rect.colliderect(position):
                self.isRed = 60

    def generate_monster(self):
        """генерация монстров"""
        for m in self.monsters:
            check = self.monsters[0][1] - self.cam
            if check > 600:
                monst = random.randint(0, 300)
                if monst < 100:
                    monst = self.MONSTER_1
                elif monst < 200:
                    monst = self.MONSTER_2
                else:
                    monst = self.MONSTER_3
                self.monsters.append([random.randint(0, 600), self.monsters[-1][1] - 700, 0, 0, monst, 1])
                self.monsters.pop(0)

    def move_monster(self):
        """передвижение монстров"""
        for m in self.monsters:
            if m[-1] == self.RIGHT_DIRECTION:
                m[0] += self.MONSTER_SPEED
                if m[0] > self.MONSTER_X_MAX:
                    m[-1] = self.LEFT_DIRECTION
            else:
                m[0] -= self.MONSTER_SPEED
                if m[0] <= self.MONSTER_X_MIN:
                    m[-1] = self.RIGHT_DIRECTION

            if m[3] == self.DOWN_DIRECTION:
                m[2] += self.MONSTER_SPEED_UP
                if m[2] > self.MAX_MONSTER_OFFSET:
                    m[3] = self.UP_DIRECTION
            else:
                m[2] -= self.MONSTER_SPEED_UP
                if m[2] < -self.MAX_MONSTER_OFFSET:
                    m[3] = self.DOWN_DIRECTION

    def update_monster(self):
        """передвижение, генерация монстров"""
        self.move_monster()
        self.draw_monster()
        self.generate_monster()

    def generate_monsters(self):
        monst = random.randint(0, 300)
        if monst < 100:
            monst = self.MONSTER_1
        elif monst < 200:
            monst = self.MONSTER_2
        else:
            monst = self.MONSTER_3
        self.monsters.append([0, random.randint(0, 400), 0, 0, monst, 1])

    def generate_platforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = self.GREEN_PLATFORM
            elif platform < 900:
                platform = self.BLUE_PLATFORM
            else:
                platform = self.RED_PLATFORM
            self.platforms.append([x, on, platform, 0])
            on -= 60
    
    def run(self):
        clock = pygame.time.Clock()
        self.generate_platforms()
        self.generate_monsters()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.coordY - self.cam > 700:
                self.cam = 0
                self.score = 0
                self.isRed = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.monsters = []
                self.generate_platforms()
                self.generate_monsters()
                self.coordX = 400
                self.coordY = 300
            self.screen.blit(self.images.sc, [0, 0])
            self.draw_springs()
            self.update_platforms()
            self.update_monster()
            self.player()
            self.screen.blit(self.font.render(str(self.score), -1, (255, 255, 255)), self.SCORE_PLACE)
            pygame.display.flip()
