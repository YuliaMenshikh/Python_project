import pygame
from pygame.locals import *
import random
import sys

class StrawberryJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.font.init()
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
        self.move = 0
        self.isRed = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.sc = pygame.image.load("images/sc.png").convert_alpha()
        self.greenPlatform = pygame.image.load("images/green.png").convert_alpha()
        self.bluePlatform = pygame.image.load("images/blue.png").convert_alpha()
        self.redPlatform = pygame.image.load("images/red.png").convert_alpha()
        self.redPlatform_1 = pygame.image.load("images/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("images/right1.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("images/right2.png").convert_alpha()
        self.playerLeft = pygame.image.load("images/left1.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("images/left2.png").convert_alpha()
        self.playerRight_red = pygame.image.load("images/right1_red.png").convert_alpha()
        self.playerRight_1_red = pygame.image.load("images/right2_red.png").convert_alpha()
        self.playerLeft_red = pygame.image.load("images/left1_red.png").convert_alpha()
        self.playerLeft_1_red = pygame.image.load("images/left2_red.png").convert_alpha()
        self.spring = pygame.image.load("images/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("images/spring_1.png").convert_alpha()
        self.monster1 = pygame.image.load("images/monster1.png").convert_alpha()
        self.monster2 = pygame.image.load("images/monster2.png").convert_alpha()
        self.monster3 = pygame.image.load("images/monster3.png").convert_alpha()

    def Move(self):
        """движение по оси X"""
        key = pygame.key.get_pressed()

        if key[K_RIGHT]:
            if self.move < 15:
                self.move += 1
            self.direction = 0
        elif key[K_LEFT]:
            if self.move > -15:
                self.move -= 1
            self.direction = 1
        else:
            if self.move > 0:
                self.move -= 1
            elif self.move < 0:
                self.move += 1

    def Physics(self):
        """падение/прыжок"""
        if not self.jump:
            self.coordY += self.gravity
            self.gravity += 1
        elif self.jump:
            self.coordY -= self.jump
            self.jump -= 1

    def SideControl(self):
        if self.coordX > 825:
            self.coordX = -25
        elif self.coordX < -25:
            self.coordX = 825

    def Player(self):
        """передвижение и прорисовка игрока"""
        self.SideControl()
        self.Move()
        self.Physics()

        self.coordX += self.move
        if self.coordY - self.cam <= 200:
            self.cam -= 10
        
        if (self.isRed):
            if not self.direction:
                if self.jump:
                    self.screen.blit(self.playerRight_1_red, (self.coordX, self.coordY - self.cam))
                else:
                    self.screen.blit(self.playerRight_red, (self.coordX, self.coordY - self.cam))
            else:
                if self.jump:
                    self.screen.blit(self.playerLeft_1_red, (self.coordX, self.coordY - self.cam))
                else:
                    self.screen.blit(self.playerLeft_red, (self.coordX, self.coordY - self.cam))
            self.isRed -= 2
        else:
            if not self.direction:
                if self.jump:
                  self.screen.blit(self.playerRight_1, (self.coordX, self.coordY - self.cam))
                else:
                    self.screen.blit(self.playerRight, (self.coordX, self.coordY - self.cam))
            else:
                if self.jump:
                    self.screen.blit(self.playerLeft_1, (self.coordX, self.coordY - self.cam))
                else:
                    self.screen.blit(self.playerLeft, (self.coordX, self.coordY - self.cam))

    def updatePlatforms(self):
        """прорисовка платформ и генерация новых, генерация новых пружин"""
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.greenPlatform.get_width() - 15, self.greenPlatform.get_height() - 5)
            position = pygame.Rect(self.coordX, self.coordY, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(position) and self.gravity and self.coordY < (p[1] - self.cam):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 0:
                self.screen.blit(self.greenPlatform, (p[0], p[1] - self.cam))
            elif p[2] == 1:
                if p[-1] == 1:
                    p[0] += 7
                    if p[0] > 700:
                        p[-1] = 0
                else:
                    p[0] -= 7
                    if p[0] <= 0:
                        p[-1] = 1
                self.screen.blit(self.bluePlatform, (p[0], p[1] - self.cam))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.redPlatform, (p[0], p[1] - self.cam))
                else:
                    self.screen.blit(self.redPlatform_1, (p[0], p[1] - self.cam))

            check = self.platforms[1][1] - self.cam
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100

    def drawSprings(self):
        """прорисовка пружин"""
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cam))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cam))
            position = pygame.Rect(self.coordX, self.coordY, self.playerRight.get_width(), self.playerRight.get_height())
            rect = pygame.Rect(spring[0], spring[1], self.spring.get_width() - 5, self.spring.get_height())
            if rect.colliderect(position):
                self.jump = 40
                self.cam -= 100

    def drawMonster(self):
        """передвижение, генерация и прорисовка монстров"""
        for m in self.monsters:
            if m[-1] == 1:
                m[0] += 5
                if m[0] > 720:
                    m[-1] = 0
            else:
                m[0] -= 5
                if m[0] <= 0:
                    m[-1] = 1

            if m[3] == 1:
                m[2] += 2
                if m[2] > 20:
                    m[3] = 0
            else:
                m[2] -= 2
                if m[2] < -20:
                    m[3] = 1

            if m[4] == 1:
                self.screen.blit(self.monster1, (m[0], m[1] - self.cam - m[2]))
                rect = pygame.Rect(m[0], m[1], self.monster1.get_width() - 5, self.monster1.get_height())
            elif m[4] == 2:
                self.screen.blit(self.monster2, (m[0], m[1] - self.cam - m[2]))
                rect = pygame.Rect(m[0], m[1], self.monster2.get_width() - 5, self.monster2.get_height())
            else:
                self.screen.blit(self.monster3, (m[0], m[1] - self.cam - m[2]))
                rect = pygame.Rect(m[0], m[1], self.monster3.get_width() - 5, self.monster3.get_height())

            position = pygame.Rect(self.coordX, self.coordY, self.playerRight.get_width(), self.playerRight.get_height())
            if rect.colliderect(position):
                self.isRed = 60
            
            check = self.monsters[0][1] - self.cam
            if check > 600:
                monst = random.randint(0, 300)
                if monst < 100:
                    monst = 1
                elif monst < 200:
                    monst = 2
                else:
                    monst = 3
                self.monsters.append([random.randint(0, 600), self.monsters[-1][1] - 700, 0, 0, monst, 1])
                self.monsters.pop(0)

    def generateMonsters(self):
        monst = random.randint(0, 300)
        if monst < 100:
            monst = 1
        elif monst < 200:
            monst = 2
        else:
            monst = 3
        self.monsters.append([0, random.randint(0,400), 0, 0, monst, 1])

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 60
    
    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        self.generateMonsters()
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
                self.generatePlatforms()
                self.generateMonsters()
                self.coordX = 400
                self.coordY = 300
            self.screen.blit(self.sc, [0, 0])
            self.drawSprings()
            self.updatePlatforms()
            self.drawMonster()
            self.Player()
            self.screen.blit(self.font.render(str(self.score), -1, (255, 255, 255)), (25, 25))
            pygame.display.flip()


StrawberryJump().run()
