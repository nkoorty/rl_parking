import pygame
import numpy as np
import math
from car import Car

class Environment:
    def __init__(self):
        pygame.init()
        
        self.screen_width = 400
        self.screen_height = 600
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = (230, 230, 230)
        self.car = Car(self.screen, self.screen_width/2 + 40, self.screen_height - 250)

        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
    
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw(self, car, episode, reward):
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
            parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
            pygame.draw.rect(self.screen, space_color, parking_space_rect)
            if i == 1:
                target_space_rect = parking_space_rect
            else:
                pygame.draw.rect(self.screen, border_color, parking_space_rect, 2)
            space_y += space_height - 2

        # Draw the green border after drawing all the parking spaces
        pygame.draw.rect(self.screen, target_color, target_space_rect, 2)

        # Draw multiple parking spaces on the left
        space_x = (self.screen_width / 2) - lane_width - space_width 
        space_y = (self.screen_height - num_spaces * (space_height)) / 2  
        for i in range(num_spaces):
            parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
            pygame.draw.rect(self.screen, space_color, parking_space_rect)
            pygame.draw.rect(self.screen, border_color, parking_space_rect, 2)
            space_y += space_height - 2

        self.car.draw()

        target_x, target_y = 310, 240
        self.draw_line_to_target(car, target_x, target_y)
        self.draw_parking_box()
        self.draw_text(f"Episode: {episode}", 10, 10)
        self.draw_text(f"Reward: {reward:.2f}", 10, 35)
        pygame.display.flip()

    def draw_line_to_target(self, car, target_x, target_y, color=(255, 0, 0)):
        car_midpoint_x, car_midpoint_y = self.car.x, self.car.y
        pygame.draw.line(self.screen, color, (car_midpoint_x, car_midpoint_y), (target_x, target_y), 5)


    def draw_parking_box(self):
        x, y, width, height = 290, 225, 40, 30

        parking_box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        parking_box_color = (255, 255, 255, 128)
        border_thickness = 2
        pygame.draw.rect(parking_box_surface, parking_box_color, (0, 0, width, height), border_thickness)

        self.screen.blit(parking_box_surface, (x, y))

    def reset(self):
        # Reset car position and angle
        self.car.x = self.screen_width/2 + 40
        self.car.y = self.screen_height - 250
        self.car.angle = 0

        # Return initial state
        state = np.array([self.car.x, self.car.y, self.car.angle])
        return state

    def step(self, action):
        # Update the car based on the action
        acceleration = 0
        angle = self.car.angle
        if action == 0:
            acceleration += 2
        elif action == 1:
            acceleration -= 1
        elif action == 2:
            angle += 10
        elif action == 3:
            angle -= 10

        self.car.acceleration = acceleration
        self.car.angle = angle
        self.car.update()
        boundary_hit = self.car.handle_boundary()
        # Get the new state and reward
        state = np.array([self.car.x, self.car.y, self.car.angle])

        # Calculate distance to target parking spot
        target_x, target_y = 310, 240
        distance = math.sqrt((self.car.x - target_x)**2 + (self.car.y - target_y)**2)

        # Define zones and penalties
        in_lane = 215 <= self.car.x
        in_right_parking_space = (self.car.x >= 290) and (self.car.x <= 330) and (self.car.y >= 200) and (self.car.y <= 280) and (-20 <= self.car.angle % 360 <= 20)
        in_wrong_parking_space_right = ((self.car.x >= 260) and (self.car.x <= 300) and (((self.car.y >= 40) and (self.car.y <= 200)) or ((self.car.y >= 280) and (self.car.y <= 560))))

        target_angle = 0
        angle_error = abs(self.car.angle % 360 - target_angle)
        speed_error = abs(self.car.speed)

        # Calculate reward
        reward = 0
        reward -= 0.001 * distance
        reward -= 0.002 * angle_error
        reward -= 0.002 * speed_error
        reward -= 0.1

        # Intermediate rewards
        if in_lane:
            reward += 0.05
        if 290 <= self.car.x <= 330:
            reward += 1

        if in_right_parking_space:
            reward += 10
            print("parked")
        elif boundary_hit or in_wrong_parking_space_right:
            reward -= 10
            print("boundary or wrong parking space")

        # Clip reward to a minimum and maximum value
        reward = np.clip(reward, -10, 10)
        
        done = False
        if boundary_hit or in_right_parking_space or in_wrong_parking_space_right or not in_lane: #or in_wrong_parking_space_left:
            done = True
        return state, reward, done
    
    def run(self):
        clock = pygame.time.Clock()
        fps = 30
        running = True
        episode = 0
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
                episode += 1
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