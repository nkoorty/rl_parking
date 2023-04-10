import os
import csv
import gym
import numpy as np
import pygame
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
from parallel_parking import Environment

class CustomParkingEnvironment(gym.Env):
    def __init__(self):
        super(CustomParkingEnvironment, self).__init__()
        self.env = Environment()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=np.array([0, 0, -360]),
                                                high=np.array([400, 600, 360]),
                                                dtype=np.float32)

    def step(self, action):
        state, reward, done = self.env.step(action)
        return state, reward, done, {}

    def reset(self):
        state = self.env.reset()
        return state

    def render(self, mode='human'):  # Updated render() method definition
        self.env.render()  # Updated render() method call

def main():
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

    model_file_path = "past_runs/parallel_7_ppo.zip"
    if os.path.exists(model_file_path):
        model = PPO.load(model_file_path, env, **hyperparams)
    else:
        model = PPO("MlpPolicy", env, verbose=1, **hyperparams)

    total_episodes = 10000
    total_timesteps = 400000
    model.learn(total_timesteps=total_timesteps)

    # Save the trained model
    model.save(model_file_path)

    clock = pygame.time.Clock()

    fps = 60
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