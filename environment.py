import pygame

class Environment:
    def __init__(self):
        # Initialize PyGame
        pygame.init()
        
        # Set screen dimensions
        self.screen_width = 400
        self.screen_height = 600
        
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
        
        # Draw left lane
        pygame.draw.rect(self.screen, lane_color, (0, 0, lane_width, lane_height))
        
        # Draw right lane
        pygame.draw.rect(self.screen, lane_color, (self.screen_width - lane_width, 0, lane_width, lane_height))
        
        # Draw parking space
        pygame.draw.rect(self.screen, space_color, ((self.screen_width - lane_width - space_width), (self.screen_height - space_height) / 2, space_width, space_height))
        
        # Update the screen
        pygame.display.flip()


    def reset(self):
        # Reset environment to initial state
        pass

    def step(self, action):
        # Take action in environment and observe next state and reward
        pass

    def run(self):
        # Set up the game clock
        clock = pygame.time.Clock()
        
        # Set the frame rate
        fps = 30
        
        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Draw the environment
            self.draw()
            
            # Wait to maintain frame rate
            clock.tick(fps)
        
        # Quit Pygame
        pygame.quit()

if __name__ == "__main__":
    env = Environment()
    env.run()