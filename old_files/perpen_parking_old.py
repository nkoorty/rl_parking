import pygame
import numpy as np
import math
from car import Car
from parked_car import ParkedCar
from old_files.parallel_parking_old import Environment

class ParkingEnv(Environment):
    def __init__(self):
        pygame.init()
        self.screen_width = 400
        self.screen_height = 600   
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = (230, 230, 230)
        self.car = Car(self.screen, self.screen_width/2 + 40, self.screen_height - 250)
        self.distance_to_bezier_curve = 0

        # Draw parked cars
        self.parked_car1 = ParkedCar(self.screen, 340, 195, -90)
        self.parked_car2 = ParkedCar(self.screen, 340, 335, -90)
        self.parked_car3 = ParkedCar(self.screen, 340, 405, -90)
        self.parked_car4 = ParkedCar(self.screen, 60, 195, 90)
        self.parked_car5 = ParkedCar(self.screen, 60, 265, 90)
        self.parked_car6 = ParkedCar(self.screen, 60, 335, 90)
        self.parked_car7 = ParkedCar(self.screen, 60, 405, 90)

        self.P0 = (240, 350)
        self.P1 = (240, 255)
        self.P2 = (340, 265)

    def draw(self, car):
        self.screen.fill(self.bg_color)

        lane_width = 80
        lane_height = self.screen_height
        space_width = 120
        space_height = 70

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
        self.car.draw()

        self.draw_line_to_target()
        self.draw_parking_box()
        pygame.display.flip()

    def draw_parking_box(self):
        x, y, width, height = 325, 250, 30, 30

        parking_box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        parking_box_color = (255, 255, 255, 128)
        border_thickness = 2
        pygame.draw.rect(parking_box_surface, parking_box_color, (0, 0, width, height), border_thickness)

        self.screen.blit(parking_box_surface, (x, y))

    def draw_line_to_target(self):
        car_midpoint_x, car_midpoint_y = self.car.x, self.car.y
        pygame.draw.line(self.screen, (0, 0, 255), (car_midpoint_x, car_midpoint_y), (340, 265), 5)

    def bezier_point(self, t, P0, P1, P2):
        x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t ** 2 * P2[0]
        y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t ** 2 * P2[1]
        return (x, y)
    
    @property
    def distance_to_bezier(self):
        x, y = self.car.x, self.car.y
        num_points = 100
        min_distance = float('inf')

        for i in range(num_points):
            t = i / (num_points - 1)
            point = self.bezier_point(t, self.P0, self.P1, self.P2)
            distance = math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
        return min_distance  

    def render(self, mode='human'):
        self.draw(self.car) 

    def step(self, action):
        # Update the car based on the action
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
        boundary_hit = self.car.handle_boundary_perpendicular()

        state = np.array([self.car.x, self.car.y, self.car.angle])

        target_x, target_y = 340, 265
        prev_distance = math.sqrt((self.car.prev_x - target_x)**2 + (self.car.prev_y - target_y)**2)
        distance = math.sqrt((self.car.x - target_x)**2 + (self.car.y - target_y)**2)

        in_right_parking_space = (self.car.x >= 320) and (self.car.x <= 355) and (self.car.y >= 260) and (self.car.y <= 270) and (84 <= abs(self.car.angle) % 360 <= 96)
        in_wrong_parking_space_right = ((self.car.x >= 260) and (self.car.x <= 400) and (((self.car.y >= 160) and (self.car.y <= 240)) or ((self.car.y >= 290) and (self.car.y <= 425))))

        p = 500
        crash_penalty = -300
        time_penalty = -0.5
        bezier_penalty = -2
        movement_penalty = 2

        parking_rotation = 0
        rotation_difference = abs(self.car.angle - parking_rotation)
        target_dir = math.atan2(target_y - self.car.y, target_x - self.car.x)
        direction_diff = abs(target_dir - self.car.angle)

        reward = 0
        done = False
        if in_right_parking_space:
            reward = p
            print("parked")
            done = True
        elif self.distance_to_bezier > 15:
            reward = crash_penalty
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
    
    def run(self):
        clock = pygame.time.Clock()
        fps = 30
        running = True
        episode = 0
        while running:
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
        pygame.quit()
    
    def quit(self):
        pygame.quit()
        exit()

if __name__ == "__main__":
    env = ParkingEnv()
    env.run()