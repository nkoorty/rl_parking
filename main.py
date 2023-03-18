from environment import Environment
from agent import DQNAgent
import pygame
import os
import datetime

def main():
    # Initialize environment and agent
    env = Environment()
    agent = DQNAgent(state_size=3, action_size=4)

    # Train the agent
    episodes = 500
    max_steps = 300  # Set your desired maximum number of steps per episode
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


    # Save the trained agent's weights
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    weights_file = f"past_runs/weights_{current_time}.h5"
    agent.save_weights(weights_file)
    print(f"Agent's weights saved to {weights_file}")

    # Test the trained agent
    state = env.reset()
    done = False
    while not done:
        action = agent.act(state, epsilon=0)

        next_state, reward, done = env.step(action)

        state = next_state

    # Quit the game
    env.quit()

if __name__ == "__main__":
    main()