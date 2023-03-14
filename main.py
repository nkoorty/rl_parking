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
    episodes = 1000
    max_steps = 400  # Set your desired maximum number of steps per episode

    # Create a clock to control rendering speed
    clock = pygame.time.Clock()
    fps = 100

    for episode in range(episodes):
        state = env.reset()
        done = False
        step = 0
        while not done and step < max_steps:
            action = agent.act(state)

            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.learn(batch_size=2)

            state = next_state
            step += 1

            # Draw the environment and control the rendering speed
            env.draw(env.car)
            clock.tick(fps)
        # Print progress
        print(f"Episode {episode+1}/{episodes}, Score: 0")


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