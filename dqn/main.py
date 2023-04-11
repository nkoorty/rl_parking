from parallel_parking import Environment
from perpen_parking import ParkingEnv
from agent_test import DQNAgent_Test
from dqn.agent import DQNAgent
import pygame
import os
import csv

def main():
    env = Environment()
    agent = DQNAgent(state_size=3, action_size=4)

    model_file_path = "past_runs/parallel_4.h5"
    episode_count_file = "episode_count.csv"
    if os.path.exists(model_file_path):
        agent.load_model(model_file_path)

    # Load previous episode count from file
    episode_count_map = {}
    if os.path.exists(episode_count_file):
        with open(episode_count_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                model, count = row
                episode_count_map[model] = int(count)

    total_episodes = episode_count_map.get(model_file_path, 0)

    episodes = 10000
    max_steps = 80 

    clock = pygame.time.Clock()
    fps = 30

    for episode in range(episodes):
        state = env.reset()
        done = False
        step = 0
        total_reward = 0

        pygame.key.set_repeat(10, 10)
        while not done and step < max_steps:
            delay = 0
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)

            state = next_state
            step += 1
            total_reward += reward
            env.draw(env.car, episode+1, total_reward)
            print(round(env.car.x, 2), round(env.car.y, 2), round(env.car.angle, 2), round(env.car.speed,2))

            clock.tick(fps)
            pygame.time.delay(delay)

        agent.learn(batch_size=8)

        total_episodes += 1
        if total_episodes % 5 == 0:
            agent.save_model(model_file_path)
            episode_count_map[model_file_path] = total_episodes
            with open(episode_count_file, "w") as f:
                writer = csv.writer(f)
                for model, count in episode_count_map.items():
                    writer.writerow([model, count])

            print(f"Episode {episode+1}/{total_episodes}, Score: {reward}")

    agent.save_model("past_runs/parallel_4.h5")
    env.quit()

if __name__ == "__main__":
    main()