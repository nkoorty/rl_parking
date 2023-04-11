import pygame
import math

WIDTH_BIAS = 25
HEIGHT_BIAS = 45

class Car:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.width = 50
        self.height = 90
        self.car_image = pygame.image.load('assets/car.png')
        self.car_image = pygame.transform.scale(self.car_image, (self.width, self.height))
        self.x = x + self.width/2 
        self.y = y + self.height/2
        self.speed = 0
        self.acceleration = 0
        self.max_speed = 5
        self.min_speed = -2
        self.angle = 0 % 360
        self.friction = 0.01

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_angle = self.angle
    
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

        # Update position
        angle_radians = math.radians(self.angle)
        new_x = self.x + self.speed * math.sin(-angle_radians)
        new_y = self.y - self.speed * math.cos(angle_radians)

        self.x = new_x
        self.y = new_y

    def handle_boundary(self):
        new_x = self.x
        new_y = self.y

        collided = False

        if new_y < 60 or new_y > 540: # (y-45) Since y is y-height/2
            if new_x < 120 + WIDTH_BIAS:
                new_x = 120 + WIDTH_BIAS
                collided = True
            if new_x > 280 - WIDTH_BIAS:
                new_x = 280 - WIDTH_BIAS
                collided = True
        else:
            if (60 <= new_x <= 125 or 280 <= new_x <= 315) and new_y < 60 + HEIGHT_BIAS:
                new_y = 60 + HEIGHT_BIAS
                collided = True
            if (60 <= new_x <= 125 or 280 <= new_x <= 315) and new_y > 540 - HEIGHT_BIAS:
                new_y = 540 - HEIGHT_BIAS
                collided = True   

            if new_x < 85:
                new_x = 85
                collided = True
            if new_x > 340 - WIDTH_BIAS:
                new_x = 340 - WIDTH_BIAS
                collided = True

        if new_y - HEIGHT_BIAS < 0:
            new_y = HEIGHT_BIAS
            collided = True
        if new_y + HEIGHT_BIAS > self.screen.get_height() :
            new_y = self.screen.get_height() - HEIGHT_BIAS
            collided = True

        self.x = new_x
        self.y = new_y

        return collided 
    
    def handle_boundary_perpendicular(self):
        new_x = self.x
        new_y = self.y

        collided = False

        if new_y < 180 or new_y > 420: # (y-45) Since y is y-height/2
            if new_x < 120 + WIDTH_BIAS:
                new_x = 120 + WIDTH_BIAS
                collided = True
            if new_x > 280 - WIDTH_BIAS:
                new_x = 280 - WIDTH_BIAS
                collided = True
        else:
            if (0 <= new_x <= 140 or 290 <= new_x <= 400) and new_y < 170 + HEIGHT_BIAS:
                new_y = 170 + HEIGHT_BIAS
                collided = True
            if (0 <= new_x <= 140 or 290 <= new_x <= 400) and new_y > 420 - HEIGHT_BIAS:
                new_y = 420 - HEIGHT_BIAS
                collided = True   

            if new_x < 45:
                new_x = 45
                collided = True
            if new_x > 380 - WIDTH_BIAS:
                new_x = 380 - WIDTH_BIAS
                collided = True

        if new_y - HEIGHT_BIAS < 0:
            new_y = HEIGHT_BIAS
            collided = True
        if new_y + HEIGHT_BIAS > self.screen.get_height() :
            new_y = self.screen.get_height() - HEIGHT_BIAS
            collided = True

        self.x = new_x
        self.y = new_y
        return collided 
    
    def draw(self):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        self.screen.blit(rotated_image, rect)
