import tensorflow as tf
import numpy as np
import random
from collections import deque
from car import Car

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        # Initialize replay memory
        self.memory = deque(maxlen=2000)
        
        # Discount factor
        self.gamma = 0.95
        
        # Exploration rate
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
        # Learning rate
        self.learning_rate = 0.001
        
        # Initialize the model
        self.model = self._build_model()
    def _build_model(self):
        # Define neural network architecture
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        
        # Compile model
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        
        return model
    
    def remember(self, state, action, reward, next_state, done):
        # Add experience to replay memory
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        # Choose action based on epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])
    
    def learn(self, batch_size):
        # Sample a batch from replay memory
        batch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in batch:
            # Calculate target Q-values
            target = reward
            if not done:
                q_next = self.model.predict(next_state)[0]
                target = reward + self.gamma * np.amax(q_next)
                
            # Calculate predicted Q-values
            q_values = self.model.predict(state)
            q_values[0][action] = target
            
            # Train the model on the batch
            self.model.fit(state, q_values, epochs=1, verbose=0)
            
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, name):
        # Load model weights
        self.model.load_weights(name)
        
    def save(self, name):
        # Save model weights
        self.model.save_weights(name)
