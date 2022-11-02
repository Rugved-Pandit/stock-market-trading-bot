import gym
import json
import datetime as dt

from stable_baselines3 import PPO, A2C, DDPG, DQN, 
from stable_baselines3.common.vec_env import dummy_vec_env

# from stabl .common.policies import MlpPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import PPO2

from env.StockTradingEnv import StockTradingEnv

import pandas as pd
import matplotlib.pyplot as plt

from env.envenv import EnvEnv

df = pd.read_csv('./data/ADANIPORTS.csv')
# df = df.sort_values('Date')

# The algorithms require a vectorized environment to run
# env = dummy_vec_env.DummyVecEnv([lambda: StockTradingEnv(df)])
env = dummy_vec_env.DummyVecEnv([lambda: EnvEnv(df)])
# env = EnvEnv(df)

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=555555) #2021-02-04 13:07:00+05:30
# model.learn(total_timesteps=50) #2021-02-04 13:07:00+05:30

obs = env.reset()
with open('./logs/log57.txt', 'w') as log:
    output = []
    balance = []
    net_worth = []
    total_shares_sold = []
    shares_held = []

    num_shares_sold = []

    # for i in range(10):
    for i in range(650000-555600):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        renderLog = env.render()

        output.extend(renderLog)
        balance.extend(env.get_attr('balance'))
        # print(env.get_attr('balance'))
        net_worth.extend(env.get_attr('net_worth'))
        # total_shares_sold.extend(env.get_attr('total_shares_sold'))
        # shares_held.extend(env.get_attr('shares_held'))

        num_shares_sold.extend(env.get_attr('num_shares_sold'))
        shares_held.extend(env.get_attr('num_shares'))
    
    log.writelines(output)
    log.close()
    
    # print(balance)
    x =  [l for l in range(len(balance))]
    figure, axis = plt.subplots(2, 2)
    axis[0, 0].plot(x, balance)
    axis[0, 0].set_title("balance")
    
    axis[0, 1].plot(x, shares_held)
    axis[0, 1].set_title("shares_held")
    
    axis[1, 0].plot(x, net_worth)
    axis[1, 0].set_title("net_worth")
    
    # axis[1, 1].plot(x, total_shares_sold)
    # axis[1, 1].set_title("total_shares_sold")

    axis[1, 1].plot(x, num_shares_sold)
    axis[1, 1].set_title("num_shares_sold")

    figure.set_figwidth(16)
    figure.set_figheight(9)

    plt.savefig('./plots/log57plot.png')
    plt.show()