import gym
import json
import datetime as dt
import numpy as np
import torch

from stable_baselines3 import PPO, A2C, DDPG, DQN, SAC, TD3
from stable_baselines3.common.vec_env import dummy_vec_env
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise

# from stabl .common.policies import MlpPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import PPO2

from env.StockTradingEnv import StockTradingEnv

import pandas as pd
import matplotlib.pyplot as plt

from env.envenvenv import EnvEnvEnv

# df = pd.read_csv('./data/ADANIPORTS-TA.csv')
df = pd.read_csv('./data/ADANIPORTS.csv')
# df = df.sort_values('Date')

# The algorithms require a vectorized environment to run
# env = dummy_vec_env.DummyVecEnv([lambda: StockTradingEnv(df)])
env = dummy_vec_env.DummyVecEnv([lambda: EnvEnvEnv(df)])
# env = EnvEnv(df)

# # The noise objects for TD3
# n_actions = env.action_space.shape[-1]
# action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
# model = TD3("MlpPolicy", env, action_noise=action_noise, verbose=1)

# model = SAC("MlpPolicy", env, verbose=1)

# Custom actor (pi) and value function (vf) networks of two layers of size 32 each with Relu activation function
# policy_kwargs = dict(activation_fn=torch.nn.ReLU, net_arch=[dict(pi=[64, 32], vf=[64, 32])])
# Create the agent
# model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1)

model = PPO("MlpPolicy", env, verbose=1, seed=69)

# model.learn(total_timesteps=555555) #2021-02-04 13:07:00+05:30
# model.learn(total_timesteps=50) #2021-02-04 13:07:00+05:30

# model.learn(total_timesteps=555555)

# model.save('./save/model141')
model = PPO.load('./save/model76')

obs = env.reset()

# print('obs')
# print(obs)


with open('./logs/log141.txt', 'w') as log:
    output = []
    balance = []
    net_worth = []
    total_shares_sold = []
    shares_held = []

    num_shares_sold = []
    rewards_list = []
    actions_list = []

    savings = 0
    savings_list = []

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

        rewards_list.append(str(rewards[0]) + '\n')
        actions_list.append(str(action[0][0]) + '\n')

        # if env.get_attr('net_worth')[0] > 102000:  
        #             if env.get_attr('num_shares')[0] >1:
        #                 print('!SAVING!')
        #                 env.num_shares -= 1
        #                 # env.net_worth = env.current_price
        #                 # env.balance += env.current_price
        #                 # env.balance-=env.current_price
        #                 savings += env.current_price
        #                 savings_list.append(savings)

    
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

    plt.savefig('./plots/log141plot.png')
    plt.show()

env.reset()

with open('./logs/log141rewards.txt', 'w') as log:
    log.writelines(rewards_list)
    log.close()

with open('./logs/log141actions.txt', 'w') as log:
    log.writelines(actions_list)
    log.close()

# with open('./logs/log141savings.txt', 'w') as log:
#     log.writelines(savings_list)
#     log.close()