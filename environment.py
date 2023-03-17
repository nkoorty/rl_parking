import pygame
import numpy as np
from car import Car

class Environment:
    def __init__(self):
        pygame.init()
        
        self.screen_width = 400
        self.screen_height = 600
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = (230, 230, 230)
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

        # Draw empty spaces
        left_empty_space = pygame.Rect(0, 0, (self.screen_width / 2) - lane_width, self.screen_height)
        pygame.draw.rect(self.screen, (48, 48, 48), left_empty_space)
        right_empty_space = pygame.Rect((self.screen_width / 2) + lane_width, 0, (self.screen_width / 2) - lane_width, self.screen_height)
        pygame.draw.rect(self.screen, (48, 48, 48), right_empty_space)
        
        # Draw lanes
        pygame.draw.rect(self.screen, lane_color, ((self.screen_width/2) - (lane_width), 0, lane_width, lane_height))
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
        num_spaces = 4 
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
        num_spaces = 4  
        space_x = (self.screen_width / 2) - lane_width - space_width 
        space_y = (self.screen_height - num_spaces * (space_height)) / 2  
        for i in range(num_spaces):
            parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
            pygame.draw.rect(self.screen, space_color, parking_space_rect)
            pygame.draw.rect(self.screen, border_color, parking_space_rect, 2)
            space_y += space_height - 2

        self.car.draw()
        pygame.display.flip()

    def reset(self):
        # Reset car position and angle
        self.car.x = self.screen_width/2
        self.car.y = self.screen_height - 100
        self.car.angle = 0

        # Return initial state
        state = np.array([self.car.x, self.car.y, self.car.angle])
        return state

    def step(self, action):
        # Take action in the environment and observe the next state and reward
        # Update the car based on the action
        acceleration = 0
        angle = self.car.angle
        if action == 0:
            acceleration += 1
        elif action == 1:
            acceleration -= 0.5
        elif action == 2:
            angle += 2
        elif action == 3:
            angle -= 2

        self.car.acceleration = acceleration
        self.car.angle = angle
        self.car.update()
        boundary_hit = self.car.handle_boundary()
        # Get the new state and reward
        state = np.array([self.car.x, self.car.y, self.car.angle])
        reward = 10.0 if self.car.is_parked() else -0.1
        done = False
        if boundary_hit or self.car.is_parked():
            done = True
        return state, reward, done
    
    def run(self):
        clock = pygame.time.Clock()
        fps = 30
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            state = np.array([self.car.x, self.car.y, self.car.angle])
            action = np.random.choice(4)
            next_state, reward, done = self.step(action)

            self.draw(self.car)
            state = next_state
   
            if done:
                self.reset()

            clock.tick(fps)
        # Quit Pygame
        pygame.quit()
    
    def quit(self):
        pygame.quit()
        exit()

if __name__ == "__main__":
    env = Environment()
    env.run()

