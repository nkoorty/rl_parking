from environment import Environment
from agent import DQNAgent
import pygame
import os

def main():
    # Initialize environment and agent
    env = Environment()
    agent = DQNAgent(state_size=3, action_size=4)

    # Load the saved model if it exists
    model_file_path = "dqn_model.h5"
    if os.path.exists(model_file_path):
        agent.load_model(model_file_path)

    # Train the agent
    episodes = 5
    max_steps = 150  # Set your desired maximum number of steps per episode
    #render_after_episode = 300  # Set the episode number after which you want to start rendering

    clock = pygame.time.Clock()
    fps = 10

    for episode in range(episodes):
        state = env.reset()
        done = False
        step = 0
        total_reward = 0
        while not done and step < max_steps:
            action = agent.act(state)

            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.learn(batch_size=2)

            state = next_state
            step += 1
            total_reward += reward
            env.draw(env.car, episode+1, total_reward)
            print(round(env.car.x, 2), round(env.car.y, 2), round(env.car.angle, 2))

            clock.tick(fps)

        # Print progress
        print(f"Episode {episode+1}/{episodes}, Score: {reward}")

    agent.save_model("past_runs/dqn_model.h5")
    # Quit the game
    env.quit()

if __name__ == "__main__":
    main()