import gym
import json
import datetime as dt

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import dummy_vec_env

# from stabl .common.policies import MlpPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import PPO2

from env.StockTradingEnv import StockTradingEnv

import pandas as pd

df = pd.read_csv('./data/ADANIPORTS.csv')
# df = df.sort_values('Date')

# The algorithms require a vectorized environment to run
env = dummy_vec_env.DummyVecEnv([lambda: StockTradingEnv(df)])

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=20000)

obs = env.reset()
with open('log4.txt', 'w') as log:
    output = []
    for i in range(2000):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        renderLog = env.render()
        output.extend(renderLog)
    log.writelines(output)
    log.close()
