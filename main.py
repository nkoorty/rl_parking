from environment import Environment
from agent import Agent
from car import Car
import time

def main():
    # Create environment and agent objects
    env = Environment()
    agent = Agent()
    
    # Set number of episodes to train for
    num_episodes = 1000
    
    for episode in range(num_episodes):
        # Reset environment and get initial state
        state = env.reset()
        
        done = False
        while not done:
            env.draw()
            """
            # Choose action based on agent's policy
            action = agent.act(state)
            
            # Take action in environment and observe next state and reward
            next_state, reward, done = env.step(action)
            
            # Store experience in replay buffer
            agent.replay_buffer.add(state, action, reward, next_state, done)
            
            # Update state
            state = next_state
            
            # Train agent using experiences from replay buffer
            if len(agent.replay_buffer) > agent.batch_size:
                experiences = agent.replay_buffer.sample(agent.batch_size)
                agent.learn(experiences)
            """
    time.sleep(5)
if __name__ == '__main__':
    main()