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
        space_width = 70
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


        car.draw()

        P0 = (240, 350)
        P1 = (240, 290)
        P2 = (280, 260)
        P3 = (310, 245)
        P4 = (310, 230)

        num_segments = 100
        for i in range(num_segments):
            t1 = i / num_segments
            t2 = (i + 1) / num_segments

            point1 = self.bezier_point(t1, P0, P1, P2, P3, P4)
            point2 = self.bezier_point(t2, P0, P1, P2, P3, P4)
            pygame.draw.line(self.screen, (255, 255, 255, 128), point1, point2, 2)

        self.draw_line_to_bezier()
        self.draw_parking_box()
        self.draw_text(f"Episode: {episode}", 10, 10)
        self.draw_text(f"Reward: {reward:.2f}", 10, 35)
        pygame.display.flip()

    def draw_line_to_bezier(self):
        car_midpoint_x, car_midpoint_y = self.car.x, self.car.y
        num_points = 100
        closest_point = None
        closest_distance = float('inf')
        
        P0 = (240, 350)
        P1 = (240, 290)
        P2 = (280, 270)
        P3 = (310, 260)
        P4 = (310, 240)

        for i in range(num_points):
            t = i / (num_points - 1)
            point = self.bezier_point(t, P0, P1, P2, P3, P4)
            distance = math.sqrt((car_midpoint_x - point[0])**2 + (car_midpoint_y - point[1])**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_point = point

        pygame.draw.line(self.screen, (0, 0, 255), (car_midpoint_x, car_midpoint_y), closest_point, 5)

    def bezier_point(self, t, P0, P1, P2, P3, P4):
        if t < 0.5:
            t_scaled = t * 2
            x = (1 - t_scaled) ** 2 * P0[0] + 2 * (1 - t_scaled) * t_scaled * P1[0] + t_scaled ** 2 * P2[0]
            y = (1 - t_scaled) ** 2 * P0[1] + 2 * (1 - t_scaled) * t_scaled * P1[1] + t_scaled ** 2 * P2[1]
        else:
            t_scaled = (t - 0.5) * 2
            x = (1 - t_scaled) ** 2 * P2[0] + 2 * (1 - t_scaled) * t_scaled * P3[0] + t_scaled ** 2 * P4[0]
            y = (1 - t_scaled) ** 2 * P2[1] + 2 * (1 - t_scaled) * t_scaled * P3[1] + t_scaled ** 2 * P4[1]
        return (x, y)

    def draw_parking_box(self):
        x, y, width, height = 290, 225, 40, 30

        parking_box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        parking_box_color = (255, 255, 255, 128)
        border_thickness = 2
        pygame.draw.rect(parking_box_surface, parking_box_color, (0, 0, width, height), border_thickness)

        self.screen.blit(parking_box_surface, (x, y))

    def distance_to_parking_spot(self, car_position, parking_spot_position):
        return np.linalg.norm(car_position - parking_spot_position)

    def global_rotation_error(self, car_rotation, tangent_rotation):
        error = abs(car_rotation - tangent_rotation) % 360
        if error > 180:
            error = 360 - error
        return error

    def reset(self):
        # Reset car position and angle
        self.car.x = self.screen_width/2 + 40
        self.car.y = self.screen_height - 250
        self.car.angle = 0

        # Return initial state
        state = np.array([self.car.x, self.car.y, self.car.angle])
        return state

    def distance_to_bezier(self, x, y):
        P0 = (240, 350)
        P1 = (240, 290)
        P2 = (280, 260)
        P3 = (310, 245)
        P4 = (310, 230)

        num_points = 100
        min_distance = float('inf')

        for i in range(num_points):
            t = i / (num_points - 1)
            point = self.bezier_point(t, P0, P1, P2, P3, P4)
            distance = math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
        return min_distance   
     
    def step(self, action):
        acceleration = 0
        angle = self.car.angle
        if action == 0:
            acceleration += 1.25
        elif action == 1:
            acceleration -= 0.75
        elif action == 2:
            angle += 3
        elif action == 3:
            angle -= 3

        self.car.acceleration = acceleration
        self.car.angle = angle
        self.car.update()
        boundary_hit = self.car.handle_boundary()
        # Calculate next states
        state = np.array([self.car.x, self.car.y, self.car.angle])

        target_x, target_y = 310, 240
  
        prev_distance = math.sqrt((self.car.prev_x - target_x)**2 + (self.car.prev_y - target_y)**2)
        distance = math.sqrt((self.car.x - target_x)**2 + (self.car.y - target_y)**2)

        in_lane = 215 <= self.car.x
        in_right_parking_space = (self.car.x >= 290) and (self.car.x <= 330) and (self.car.y >= 200) and (self.car.y <= 280) and (-20 <= abs(self.car.angle % 360) <= 20)
        in_wrong_parking_space_right = ((self.car.x >= 260) and (self.car.x <= 300) and (((self.car.y >= 40) and (self.car.y <= 200)) or ((self.car.y >= 285) and (self.car.y <= 560))))

        # Constants for reward calculation
        p = 500
        crash_penalty = -300
        time_penalty = -1
        movement_penalty = 0.75
        # smoothness_penalty = -2
        # direction_penalty = -2

        # Calculate angular velocity
        # angular_velocity = abs(self.car.angle - self.car.prev_angle)

        # Calculate rotation difference
        # parking_rotation = 0
        # rotation_difference = abs(self.car.angle - parking_rotation)

        # Calculate the direction to the target
        target_dir = math.atan2(target_y - self.car.y, target_x - self.car.x)
        direction_diff = abs(target_dir - self.car.angle)

        # Normalize the difference to be between -pi and pi
        direction_diff = ((direction_diff + math.pi) % (2 * math.pi)) - math.pi

        # Calculate reward
        reward = 0
        done = False
        if in_right_parking_space:
            reward = p
            print("parked")
            done = True
        elif boundary_hit:
            reward = crash_penalty
            print("collided")
            done = True
        else:
            reward += time_penalty
            if distance < prev_distance:
                reward += movement_penalty
            else:
                reward -= movement_penalty 
        return state, reward, done
    
    def render(self, mode='human'):
        self.draw(self.car, 0, 0)
    
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
            next_state, reward, dones = self.step(action)

            self.draw(self.car, 0, 0)
            state = next_state

            if all(dones):
                episode += 1
                self.reset()

            clock.tick(fps)
        # Quit Pygame
        pygame.quit()
    
    def quit(self):
        pygame.quit()
        env.run()

if __name__ == "__main__":
    env = Environment()
    env.run()