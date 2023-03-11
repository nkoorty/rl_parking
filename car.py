import pygame

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.acceleration = 0
        self.max_speed = 5
        self.min_speed = -2
        self.width = 30
        self.height = 50

    def update(self):
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < self.min_speed:
            self.speed = self.min_speed
        self.y -= self.speed

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def draw(self, surface):
        rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        pygame.draw.rect(surface, (255, 0, 0), rect)