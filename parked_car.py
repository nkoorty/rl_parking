import pygame

class ParkedCar:
    def __init__(self, screen, x, y, angle = 0):
        self.screen = screen
        self.width = 50
        self.height = 90
        self.car_image = pygame.image.load('assets/car_other.png')
        self.car_image = pygame.transform.scale(self.car_image, (self.width, self.height))
        self.x = x 
        self.y = y 
        self.angle = angle
        self.update_rect()
    
    def draw(self):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        self.screen.blit(rotated_image, self.rect)

    def update_rect(self):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        self.rect = rotated_image.get_rect(center=(self.x, self.y))
