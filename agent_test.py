import tensorflow as tf
import numpy as np
import random
from collections import deque

class DQNAgent_Test:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        self.memory = deque(maxlen=10000)
        self.memory_human = deque(maxlen=10000)  # New human memory
        self.pure_human_learning = True
        self.gamma = 0.97
        self.epsilon = 0.5
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.85
        self.learning_rate = 0.05
        self.update_target_freq = 1000  # Frequency for updating the target network
        self.update_target_freq_counter = 0  # Counter for updating the target network
        self.model = self._build_model()
        self.target_model = self._build_model()  # Create target network
        self.update_target_model()  # Initialize target network with same weights as the main network

    def _build_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32, input_dim=self.state_size, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        
        # Compile model
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        
        return model
    
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())  # Update target network with main network weights
    
    def remember(self, state, action, reward, next_state, done, human_action=None):
        if human_action is not None:
            self.memory_human.append((state, action, reward, next_state, done))
        else:
            self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, epsilon=None, human_action=None):
        epsilon = self.epsilon if epsilon is None else epsilon
        
        if human_action is not None:
            return human_action
        elif np.random.rand() <= epsilon:
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

        if self.pure_human_learning:
            if len(self.memory_human) < batch_size:
                return
            batch = random.sample(self.memory_human, batch_size)
        else:
            # Modify batch sampling to prioritize human input samples
            human_batch_size = int(batch_size * 0.9)
            if len(self.memory_human) >= human_batch_size:
                batch = random.sample(self.memory_human, human_batch_size)
                batch.extend(random.sample(self.memory, batch_size - human_batch_size))
            else:
                batch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                next_state = np.reshape(next_state, (1, -1))
                q_next = self.target_model.predict(next_state)[0]  # Use target network to predict next state Q-values
                target = reward + self.gamma * np.amax(q_next)

            state = np.reshape(state, (1, -1))
            q_values = self.model.predict(state)
            q_values[0][action] = target
            
            self.model.fit(state, q_values, epochs=1, verbose=0)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Update target network
        self.update_target_freq_counter += 1
        if self.update_target_freq_counter >= self.update_target_freq:
            self.update_target_model()
            self.update_target_freq_counter = 0
            
    def load_model(self, file_path):
        self.model.load_weights(file_path)
        
    def save_model(self, file_path):
        self.model.save_weights(file_path)