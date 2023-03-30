from tensorflow.python.keras.models import load_model
import tensorflow as tf
import numpy as np
import random
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.95
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
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
        epsilon = self.epsilon if epsilon is None else epsilon
        if np.random.rand() <= epsilon:
            return random.randrange(self.action_size)
        else:
            state = np.reshape(state, (1, -1)) 
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])
    
    def learn(self, batch_size):
        if len(self.memory) < batch_size:
            return

        if batch_size <= 0:
            return

        batch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                next_state = np.reshape(next_state, (1, -1))
                q_next = self.model.predict(next_state)[0]
                target = reward + self.gamma * np.amax(q_next)

            state = np.reshape(state, (1, -1))
            q_values = self.model.predict(state)
            q_values[0][action] = target
            
            self.model.fit(state, q_values, epochs=1, verbose=0)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load_model(self, file_path):
        self.model.load_weights(file_path)
        
    def save_model(self, file_path):
        self.model.save_weights(file_path)