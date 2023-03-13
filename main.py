from environment import Environment
from agent import Agent
import random

def main():
    # Create environment and agent objects
    env = Environment()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = Agent(state_size, action_size, seed=0)
    
    # Set number of episodes to train for
    num_episodes = 1000
    
    for episode in range(num_episodes):
        # Reset environment and get initial state
        state = env.reset()
        
        done = False
        while not done:
            # Choose action based on agent's policy
            action = agent.act(state)
            
            # Take action in environment and observe next state and reward
            next_state, reward, done, _ = env.step(action)
            
            # Store experience in replay buffer
            agent.buffer.append((state, action, reward, next_state, done))
            
            # Update state
            state = next_state
            
            # Train agent using experiences from replay buffer
            if len(agent.buffer) > agent.batch_size:
                experiences = random.sample(agent.buffer, k=agent.batch_size)
                agent.learn(experiences)

if __name__ == '__main__':
    main()
    