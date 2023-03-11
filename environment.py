import pygame
from car import Car

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

        # Creating the Car object
        self.car = Car(self.screen, self.screen_width/2, self.screen_height - 100)
    
    def draw(self, car):
        # Fill screen with background color
        self.screen.fill(self.bg_color)
        
        # Set lane and parking space dimensions
        lane_width = 80
        lane_height = self.screen_height
        space_width = 60
        space_height = 120
        
        # Set colors for lanes and parking spaces
        lane_color = (100, 100, 100)
        space_color = (92, 122, 171)
        line_color = (255, 255, 255)
        border_color = (255, 255, 0)
        target_color = (60, 207, 43)

        # Left empty space
        left_empty_space = pygame.Rect(0, 0, (self.screen_width / 2) - lane_width, self.screen_height)
        pygame.draw.rect(self.screen, (48, 48, 48), left_empty_space)

        # Right empty space
        right_empty_space = pygame.Rect((self.screen_width / 2) + lane_width, 0, (self.screen_width / 2) - lane_width, self.screen_height)
        pygame.draw.rect(self.screen, (48, 48, 48), right_empty_space)
        
        # Draw left lane
        pygame.draw.rect(self.screen, lane_color, ((self.screen_width/2) - (lane_width), 0, lane_width, lane_height))
        
        # Draw right lane
        pygame.draw.rect(self.screen, lane_color, ((self.screen_width/2), 0, lane_width, lane_height))
        
        # Draw striped line
        line_height = 20
        line_spacing = 10
        num_lines = int(lane_height / (line_height + line_spacing))
        line_y = (self.screen_height - num_lines * (line_height + line_spacing)) / 2
        for i in range(num_lines):
            line_rect = pygame.Rect((self.screen_width / 2) - 1.5, line_y, 3, line_height)
            pygame.draw.rect(self.screen, line_color, line_rect)
            line_y += line_height + line_spacing
        
        # Draw multiple parking spaces on the right
        num_spaces = 4  # Change this value to adjust the number of parking spaces
        space_x = (self.screen_width / 2) + lane_width 
        space_y = (self.screen_height - num_spaces * (space_height)) / 2 
        for i in range(num_spaces):
            if i == 1:
                parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
                pygame.draw.rect(self.screen, space_color, parking_space_rect)
                pygame.draw.rect(self.screen, target_color, parking_space_rect, 2)
            else:
                parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
                pygame.draw.rect(self.screen, space_color, parking_space_rect)
                pygame.draw.rect(self.screen, border_color, parking_space_rect, 2)
            space_y += space_height - 2

        # Draw multiple parking spaces on the left
        num_spaces = 4  # Change this value to adjust the number of parking spaces
        space_x = (self.screen_width / 2) - lane_width - space_width 
        space_y = (self.screen_height - num_spaces * (space_height)) / 2  
        for i in range(num_spaces):
            parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
            pygame.draw.rect(self.screen, space_color, parking_space_rect)
            pygame.draw.rect(self.screen, border_color, parking_space_rect, 2)
            space_y += space_height - 2

        self.car.draw()

        # Update the screen
        pygame.display.flip()

    """
    def reset(self):
        # Reset environment to initial state
        pass

    def step(self, action):
        # Take action in environment and observe next state and reward
        pass
    """
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
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.car.move_forwards()
            elif keys[pygame.K_DOWN]:
                self.car.move_backwards()
            elif keys[pygame.K_RIGHT]:
                self.car.move_right()
            elif keys[pygame.K_LEFT]:
                self.car.move_left()  
            else:
                self.car.acceleration = 0

            # Draw the environment
            self.draw(Car)
            self.car.update()
            
            # Wait to maintain frame rate
            clock.tick(fps)
        
        # Quit Pygame
        pygame.quit()

if __name__ == "__main__":
    env = Environment()
    env.run()