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
        self.steering_angle = 0
        self.max_steering_angle = 30
        self.turn_rate = 5
        self.handling = 0.9
        self.brake_power = 0.5
        self.inertia = 0.1

    def update(self):
        # Apply friction and inertia
        if self.speed > 0:
            self.speed -= self.friction * self.speed + self.inertia * self.speed ** 2
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.friction * abs(self.speed) + self.inertia * self.speed ** 2
            if self.speed > 0:
                self.speed = 0

        # Apply acceleration and braking
        if self.acceleration > 0:
            self.speed += self.acceleration * self.handling
            if self.speed > self.max_speed:
                self.speed = self.max_speed
        elif self.acceleration < 0:
            self.speed += self.acceleration * self.brake_power
            if self.speed < self.min_speed:
                self.speed = self.min_speed

        # Apply steering
        self.steering_angle += self.turn_rate * self.angle
        if self.steering_angle > self.max_steering_angle:
            self.steering_angle = self.max_steering_angle
        elif self.steering_angle < -self.max_steering_angle:
            self.steering_angle = -self.max_steering_angle
        self.angle += self.steering_angle * self.speed / self.width
        self.steering_angle *= self.handling

        # Update position
        angle_radians = math.radians(self.angle)
        new_x = self.x + self.speed * math.sin(-angle_radians)
        new_y = self.y - self.speed * math.cos(angle_radians)

        self.x = new_x
        self.y = new_y

    def handle_boundary(self):
        new_x = self.x
        new_y = self.y

        if new_y < 15 or new_y > 495: # (y-45) Since y is y-height/2
            if new_x < 120:
                new_x = 120
            if new_x > 280 - self.width:
                new_x = 280 - self.width
        else:
            if (60 <= new_x <= 120 or 280 <= new_x <= 340)and new_y < 60:
                new_y = 60
            if (60 <= new_x <= 120 or 280 <= new_x <= 340) and new_y > 540:
                new_y = 540   

            if new_x < 60:
                new_x = 60
            if new_x > 340 - self.width:
                new_x = 340 - self.width

        if new_y + 1/5 * self.height < 0:
            new_y = - 1/5 * self.height
        if new_y > self.screen.get_height() - 4/5*self.height:
            new_y = self.screen.get_height() - 4/5*self.height

        self.x = new_x
        self.y = new_y

    def is_parked(self):
        tolerance = 10
        top_left = (280 - tolerance, 180 - tolerance)
        bottom_right = (340 + tolerance, 300 + tolerance)
        return (top_left[0] <= self.x <= bottom_right[0] and top_left[1] <= self.y <= bottom_right[1])

    def rotate_left(self):
        self.angle -= 5

    def rotate_right(self):
        self.angle += 5

    def draw(self):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated_image.get_rect(center=(self.x + self.width / 2, self.y + self.height/2))
        self.screen.blit(rotated_image, rect)
