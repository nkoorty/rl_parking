import pygame
import numpy as np
import math
from car import Car
from parked_car import ParkedCar

class Environment:
    def __init__(self):
        pygame.init()

        self.screen_width = 400
        self.screen_height = 600   
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = (230, 230, 230)
        self.car = Car(self.screen, self.screen_width/2 + 40, self.screen_height - 250)

        # Draw parked cars
        self.parked_car1 = ParkedCar(self.screen, 315, 120, 0)
        self.parked_car2 = ParkedCar(self.screen, 315, 360, 0)
        self.parked_car3 = ParkedCar(self.screen, 315, 480, 0)
        self.parked_car4 = ParkedCar(self.screen, 85, 120, 0)
        self.parked_car5 = ParkedCar(self.screen, 85, 240, 0)
        self.parked_car6 = ParkedCar(self.screen, 85, 360, 0)
        self.parked_car7 = ParkedCar(self.screen, 85, 480, 0)

        self.P0 = (240, 350)
        self.P1 = (240, 290)
        self.P2 = (280, 270)
        self.P3 = (315, 260)
        self.P4 = (315, 240)

        pygame.font.init()

    def draw(self, car):
        self.screen.fill(self.bg_color)
        
        lane_width = 80
        lane_height = self.screen_height
        space_width = 70
        space_height = 120

        lane_color = (100, 100, 100)
        space_color = (92, 122, 171)
        line_color = (255, 255, 255)
        border_color = (255, 255, 0)
        target_color = (60, 207, 43)

        left_empty_space = pygame.Rect(0, 0, (self.screen_width / 2) - lane_width, self.screen_height)
        pygame.draw.rect(self.screen, (48, 48, 48), left_empty_space)
        right_empty_space = pygame.Rect((self.screen_width / 2) + lane_width, 0, (self.screen_width / 2) - lane_width, self.screen_height)
        pygame.draw.rect(self.screen, (48, 48, 48), right_empty_space)
        
        pygame.draw.rect(self.screen, lane_color, ((self.screen_width/2) - (lane_width), 0, lane_width, lane_height))
        pygame.draw.rect(self.screen, lane_color, ((self.screen_width/2), 0, lane_width, lane_height))

        line_height = 20
        line_spacing = 10
        num_lines = int(lane_height / (line_height + line_spacing))
        line_y = (self.screen_height - num_lines * (line_height + line_spacing)) / 2
        for i in range(num_lines):
            line_rect = pygame.Rect((self.screen_width / 2) - 1.5, line_y, 3, line_height)
            pygame.draw.rect(self.screen, line_color, line_rect)
            line_y += line_height + line_spacing

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

        pygame.draw.rect(self.screen, target_color, target_space_rect, 2)

        space_x = (self.screen_width / 2) - lane_width - space_width 
        space_y = (self.screen_height - num_spaces * (space_height)) / 2  
        for i in range(num_spaces):
            parking_space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
            pygame.draw.rect(self.screen, space_color, parking_space_rect)
            pygame.draw.rect(self.screen, border_color, parking_space_rect, 2)
            space_y += space_height - 2

        for i in range(1, 8):
            parked_car = getattr(self, 'parked_car' + str(i))
            parked_car.draw()
        car.draw()

        self.draw_line_to_target()
        self.draw_parking_box()
        pygame.display.flip()

    def draw_line_to_target(self):
        car_midpoint_x, car_midpoint_y = self.car.x, self.car.y
        pygame.draw.line(self.screen, (0, 0, 255), (car_midpoint_x, car_midpoint_y), (315, 240), 5)

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
        x, y, width, height = 295, 225, 40, 30

        parking_box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        parking_box_color = (255, 255, 255, 128)
        border_thickness = 2
        pygame.draw.rect(parking_box_surface, parking_box_color, (0, 0, width, height), border_thickness)

        self.screen.blit(parking_box_surface, (x, y))

    def distance_to_parking_spot(self, car_position, parking_spot_position):
        return np.linalg.norm(car_position - parking_spot_position)

    def reset(self):
        self.car.x = self.screen_width/2 + 40
        self.car.y = self.screen_height - 250
        self.car.angle = 0

        state = np.array([self.car.x, self.car.y, self.car.angle])
        return state

    def distance_to_bezier(self, x, y):
        num_points = 100
        min_distance = float('inf')

        for i in range(num_points):
            t = i / (num_points - 1)
            point = self.bezier_point(t, self.P0, self.P1, self.P2, self.P3, self.P4)
            distance = math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
        return min_distance   
     
    def step(self, action):
        acceleration = 0
        angle = self.car.angle
        if action == 0:
            acceleration += 2
        elif action == 1:
            acceleration -= 1
        elif action == 2:
            angle += 5
        elif action == 3:
            angle -= 5

        self.car.acceleration = acceleration
        self.car.angle = angle
        self.car.update()
        boundary_hit = self.car.handle_boundary()
        state = np.array([self.car.x, self.car.y, self.car.angle])

        target_x, target_y = 315, 240
  
        prev_distance = math.sqrt((self.car.prev_x - target_x)**2 + (self.car.prev_y - target_y)**2)
        distance = math.sqrt((self.car.x - target_x)**2 + (self.car.y - target_y)**2)
        bezier_distance = self.distance_to_bezier(self.car.x, self.car.y)

        car_rect = pygame.Rect(self.car.x - self.car.width / 2, self.car.y - self.car.height / 2, self.car.width, self.car.height)

        car_collision = False
        for i in range(1, 8):
            parked_car = getattr(self, 'parked_car' + str(i))
            if car_rect.colliderect(parked_car.rect):
                car_collision = True
            break

        in_lane = 215 <= self.car.x
        in_right_parking_space = (self.car.x >= 300) and (self.car.x <= 335) and (self.car.y >= 225) and (self.car.y <= 255) and (-10 <= abs(self.car.angle % 360) <= 10)
        in_wrong_parking_space_right = ((self.car.x >= 265) and (self.car.x <= 340) and (((self.car.y >= 40) and (self.car.y <= 200)) or ((self.car.y >= 285) and (self.car.y <= 560))))

        # Calculate the direction to the target
        target_dir = math.atan2(target_y - self.car.y, target_x - self.car.x)
        direction_diff = abs(target_dir - self.car.angle)

        # Normalize the difference to be between -pi and pi
        direction_diff = ((direction_diff + math.pi) % (2 * math.pi)) - math.pi

        p = 500
        crash_penalty = -300
        time_penalty = -1
        movement_penalty = 1.25

        reward = 0
        done = False
        if in_right_parking_space:
            reward = p
            print("parked")
            done = True
        elif boundary_hit or car_collision or in_wrong_parking_space_right:
            reward = crash_penalty
            print("collided")
            done = True
        elif bezier_distance > 20:
            reward -= 0.5
        elif direction_diff > 0.5:
            reward -= 0.5
        else:
            reward += time_penalty
            if distance < prev_distance:
                reward += movement_penalty
            else:
                reward -= movement_penalty 
        return state, reward, done
    
    def render(self, mode='human'):
        self.draw(self.car)
    
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

            self.draw(self.car)
            state = next_state

            if all(dones):
                episode += 1
                self.reset()

            clock.tick(fps)
        pygame.quit()
    
    def quit(self):
        pygame.quit()
        env.run()

if __name__ == "__main__":
    env = Environment()
    env.run()