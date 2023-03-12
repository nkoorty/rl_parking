import pygame
import math

class Car:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.width = 50
        self.height = 90
        self.car_image = pygame.image.load('car.png')
        self.car_image = pygame.transform.scale(self.car_image, (self.width, self.height))
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.speed = 0
        self.acceleration = 0
        self.max_speed = 5
        self.min_speed = -2
        self.angle = 0

    def update(self):
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < self.min_speed:
            self.speed = self.min_speed

        if self.x < 0:
            self.x = 0
        elif self.x + self.width > self.screen.get_width():
            self.x = self.screen.get_width() - self.width
        
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen.get_height():
            self.y = self.screen.get_height() - self.height
        
        angle_radians = math.radians(self.angle)
        self.x += self.speed * math.sin(-angle_radians)
        self.y -= self.speed * math.cos(angle_radians)

    def rotate_left(self):
        self.angle -= 5

    def rotate_right(self):
        self.angle += 5

    def draw(self):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated_image.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.screen.blit(rotated_image, rect)