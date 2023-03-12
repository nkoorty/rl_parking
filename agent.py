import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random
from collections import deque

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, seed):
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Agent:
    def __init__(self, state_size, action_size, seed):
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)

        # Q-Network
        self.q_network = QNetwork(state_size, action_size, seed)

        # Target Network
        self.target_network = QNetwork(state_size, action_size, seed)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()

        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)

        # Replay buffer
        self.buffer = deque(maxlen=10000)

        # Hyperparameters
        self.gamma = 0.99
        self.tau = 0.001
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.batch_size = 64

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size-1)
        else:
            state = torch.from_numpy(state).float().unsqueeze(0)
            self.q_network.eval()
            with torch.no_grad():
                action_values = self.q_network(state)
            self.q_network.train()
            return np.argmax(action_values.numpy())
        
    def learn(self, experiences):
        # Unpack experiences
        states, actions, rewards, next_states, dones = experiences

        # Convert to PyTorch tensors
        states = torch.from_numpy(states).float()
        actions = torch.from_numpy(actions).long()
        rewards = torch.from_numpy(rewards).float()
        next_states = torch.from_numpy(next_states).float()
        dones = torch.from_numpy(dones.astype(np.uint8)).float()

        # Compute Q-values for current states using the Q-network
        q_values = self.q_network(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        # Compute target Q-values for next states using the target network
        target_q_values = self.target_network(next_states)
        max_q_values = torch.max(target_q_values, 1)[0]
        target_q_values = rewards + (self.gamma * max_q_values * (1 - dones))

        # Compute loss
        loss = torch.nn.functional.mse_loss(q_values, target_q_values)

        # Update Q-network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Update target network
        self.update_target_network()

    def update_target_network(self):
        for target_param, param in zip(self.target_network.parameters(), self.q_network.parameters()):
            target_param.data.copy_(self.tau * param.data + (1.0 - self.tau) * target_param.data)

    def add_experience(self, state, action, reward, next_state, done):
        # Add the experience to the replay buffer
        self.buffer.append((state, action, reward, next_state, done))

        # If the replay buffer is full, sample a batch of experiences and learn from them
        if len(self.buffer) >= self.batch_size:
            experiences = random.sample(self.buffer, k=self.batch_size)
            self.learn(experiences)
