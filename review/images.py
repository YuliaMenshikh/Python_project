import pygame
import os

class Images:
    def __init__(self):
        self.sc = self.load_images("sc.png")
        self.green_platform = self.load_images("green.png")
        self.blue_platform = self.load_images("blue.png")
        self.red_platform = self.load_images("red.png")
        self.red_platform_1 = self.load_images("red_1.png")
        self.player_right = self.load_images("right1.png")
        self.player_right_1 = self.load_images("right2.png")
        self.player_left = self.load_images("left1.png")
        self.player_left_1 = self.load_images("left2.png")
        self.player_right_red = self.load_images("right1_red.png")
        self.player_right_1_red = self.load_images("right2_red.png")
        self.player_left_red = self.load_images("left1_red.png")
        self.player_left_1_red = self.load_images("left2_red.png")
        self.spring = self.load_images("spring.png")
        self.spring_1 = self.load_images("spring_1.png")
        self.monster1 = self.load_images("monster1.png")
        self.monster2 = self.load_images("monster2.png")
        self.monster3 = self.load_images("monster3.png")

    def load_images(self, image_name):
        return pygame.image.load(os.path.join('images', image_name)).convert_alpha()