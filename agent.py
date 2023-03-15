import tensorflow as tf
import numpy as np
import random
from collections import deque

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
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, epsilon=None):
        # Use the provided epsilon value if not None, otherwise use the agent's epsilon
        epsilon = self.epsilon if epsilon is None else epsilon

        # Choose action based on epsilon-greedy policy
        if np.random.rand() <= epsilon:
            return random.randrange(self.action_size)
        else:
            state = np.reshape(state, (1, -1))  # Add this line to reshape the state
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])
    
    def learn(self, batch_size):
        if len(self.memory) < batch_size:
            return

        if batch_size <= 0:
            return
        # Sample a batch from replay memory
        batch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in batch:
            # Calculate target Q-values
            target = reward
            if not done:
                next_state = np.reshape(next_state, (1, -1))  # Add this line to reshape the next_state
                q_next = self.model.predict(next_state)[0]
                target = reward + self.gamma * np.amax(q_next)
                
            # Calculate predicted Q-values
            state = np.reshape(state, (1, -1))  # Add this line to reshape the state
            q_values = self.model.predict(state)
            q_values[0][action] = target
            
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

    def save_weights(self, weights_file):
        self.model.save_weights(weights_file)