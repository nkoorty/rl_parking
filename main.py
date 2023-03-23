from environments.environment import Environment
from agent import DQNAgent
import pygame
import os
import csv

def main():
    # Initialize environment and agent
    env = Environment()
    agent = DQNAgent(state_size=3, action_size=4)

    # Load the saved model if it exists
    model_file_path = "dqn_model.h5"
    episode_count_file = "episode_count.csv"
    if os.path.exists(model_file_path):
        agent.load_model(model_file_path)

    # Load previous episode count from file
    if os.path.exists(episode_count_file):
        with open(episode_count_file, "r") as f:
            reader = csv.reader(f)
            total_episodes = int(next(reader)[0])
    else:
        total_episodes = 0

    episodes = 5
    max_steps = 150 

    clock = pygame.time.Clock()
    fps = 30

    for episode in range(episodes):
        state = env.reset()
        done = False
        step = 0
        total_reward = 0
        while not done and step < max_steps:
            action = agent.act(state)

            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.learn(batch_size=4)

            state = next_state
            step += 1
            total_reward += reward
            env.draw(env.car, episode+1, total_reward)
            print(round(env.car.x, 2), round(env.car.y, 2), round(env.car.angle, 2))

            clock.tick(fps)

        # Save model and update total episode count
        total_episodes += 1
        if total_episodes % 5 == 0:
            agent.save_model("past_runs/dqn_model.h5")
            with open(episode_count_file, "w") as f:
                writer = csv.writer(f)
                writer.writerow([total_episodes])

            # Print progress
            print(f"Episode {episode+1}/{total_episodes}, Score: {reward}")

    agent.save_model("past_runs/dqn_model.h5")
    # Quit the game
    env.quit()

if __name__ == "__main__":
    main()