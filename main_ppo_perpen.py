import os
import csv
import gym
import numpy as np
import pygame
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
from perpen_parking import ParkingEnv

class CustomParkingEnvironment(gym.Env):
    def __init__(self):
        super(CustomParkingEnvironment, self).__init__()
        self.env = ParkingEnv()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=np.array([0, 0, -360]),
                                                high=np.array([400, 600, 360]),
                                                dtype=np.float32)
        self.current_step = 0 
        self.max_episode_steps = 190

    def step(self, action):
        state, reward, done = self.env.step(action)
        self.current_step += 1 
        if self.current_step >= self.max_episode_steps: 
            done = True 
        
        return state, reward, done, {}

    def reset(self):
        state = self.env.reset()
        self.current_step = 0
        return state

    def render(self, mode='human'):
        self.env.render()  

def main():
    file = "perpen_19_ppo"
    env = make_vec_env(CustomParkingEnvironment, n_envs=1)

    hyperparams = {
    "learning_rate": 0.0003,
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.0,
    "vf_coef": 0.5,
    "max_grad_norm": 0.5,
    }

    model_file_path = f"past_runs/{file}.zip"
    if os.path.exists(model_file_path):
        model = PPO.load(model_file_path, env, **hyperparams, tensorboard_log="data/")
    else:
        model = PPO("MlpPolicy", env, verbose=1, **hyperparams, tensorboard_log="data/")

    total_episodes = 5000
    total_timesteps = 100000

    log_dir = "data/"
    os.makedirs(log_dir, exist_ok=True)

    model.learn(total_timesteps=total_timesteps, tb_log_name=f"{file}")
    model.save(model_file_path) 

    clock = pygame.time.Clock()

    fps = 30
    episode_length = 0

    for episode in range(total_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
            total_reward += reward

            clock.tick(fps)
        episode_length += 1

        print(f"Episode {episode+1}/{total_episodes}, Score: {total_reward}")

if __name__ == "__main__":
    main()