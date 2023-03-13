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
        self.friction = 0.01

    def update(self):
        # Apply friction
        if self.speed > 0:
            self.speed -= self.friction * self.speed
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.friction * abs(self.speed)
            if self.speed > 0:
                self.speed = 0

        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < self.min_speed:
            self.speed = self.min_speed
        
        angle_radians = math.radians(self.angle)
        new_x = self.x + self.speed * math.sin(-angle_radians)
        new_y = self.y - self.speed * math.cos(angle_radians)

        if new_y < 15 or new_y > 495: # (y-45)Since y is y-height/2
            if new_x < 120:
                new_x = 120
            elif new_x > 280 - self.width:
                new_x = 280 - self.width
        else:
            if new_x < 60:
                new_x = 60
            elif new_x > 340 - self.width:
                new_x = 340 - self.width

        if new_y + 1/5 * self.height < 0:
            new_y = - 1/5 * self.height
        elif new_y > self.screen.get_height() - 4/5*self.height:
            new_y = self.screen.get_height() - 4/5*self.height

        self.x = new_x
        self.y = new_y

    def rotate_left(self):
        self.angle -= 5

    def rotate_right(self):
        self.angle += 5

    def draw(self):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated_image.get_rect(center=(self.x + self.width / 2, self.y + self.height/2))
        self.screen.blit(rotated_image, rect)
        