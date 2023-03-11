import pygame

class Environment:
    def __init__(self):
        # Initialize PyGame
        pygame.init()
        
        # Set screen dimensions
        self.screen_width = 600
        self.screen_height = 400
        
        # Create screen object
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Set background color
        self.bg_color = (230, 230, 230)
    
    def draw(self):
        # Fill screen with background color
        self.screen.fill(self.bg_color)
        
        # Set lane and parking space dimensions
        lane_width = 50
        lane_height = self.screen_height
        space_width = 40
        space_height = 80
        
        # Set colors for lanes and parking spaces
        lane_color = (100, 100, 100)
        space_color = (255, 255, 255)