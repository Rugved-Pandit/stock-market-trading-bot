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
import datetime
from env.envenv import EnvEnv
import yfinance as yf
import time

# from selen import run_selenium
# from buy_sell import run_selenium
import json
# My code goes here

global old_shares_held
old_shares_held = 0
old_shares_sold = 0
flag=True
parameters_main = {'buy':False, 'sell':False, 'hold':False, 'qty':0}

with open('./logs/test_15-02-2023.txt', 'w') as log:
    output = []
    balance = []
    net_worth = []
    total_shares_sold = []
    shares_held = []

    num_shares_sold = []
    rewards_list = []
    actions_list = []

    prev_val = 0
    counter = 30
    while counter:
        df = yf.download( tickers="ADANIPORTS.NS", period="1d", interval="1m", ignore_tz=False, group_by='ticker', auto_adjust=True, repair=False, prepost=True, threads=True, proxy=None)
        if len(df)>prev_val:
            prev_val = len(df)
            df.to_csv('./data/ADANIPORTS-28-03-2023.csv')
            dataa = pd.read_csv('./data/ADANIPORTS-28-03-2023.csv')
            dataa.rename(
                columns={"Datetime": "datetime", "Open": "open", "High": "high","Low":"low","Close":"close"},
                inplace=True)


                # for i in range(10):
            model = PPO.load('./save/model76')
            env = dummy_vec_env.DummyVecEnv([lambda: EnvEnv(dataa)])
            obs = env.reset()
            # for i in range(374-41):
            # print(obs)
            action, _states = model.predict(obs)
            obs, rewards, done, info = env.step(action)
            renderLog = env.render()
            output = renderLog
            balance = env.get_attr('balance')

            # print(balance)
            # print(type(balance[0]))
            # update balance from selenium
            with open('./BALANCE.txt', 'w') as bal:
                bal.writelines(str(balance[0]))
                bal.close()
            net_worth = env.get_attr('net_worth')
            num_shares_sold = env.get_attr('num_shares_sold')
            # shares_held = env.get_attr('num_shares')
            shares_held.extend(env.get_attr('num_shares'))
            print("Env is running")
            if flag:
                # run_selenium()
                flag=False
            # if old_shares_held==0:
            old_shares_held = shares_held
            # if shares_held!=old_shares_held:
                # run_selenium(shares_held, num_shares_sold)
            if shares_held>old_shares_held:
                quantity = shares_held - old_shares_held
                parameters_main = {'buy':1, 'sell':0, 'hold':0, 'qty':quantity}
                
                with open('./parameters.json', 'w') as param:
                    json_object = json.dumps(parameters_main, param)
                    param.close()
            
            elif shares_held<old_shares_held:
                quantity = old_shares_held - shares_held
                parameters_main = {'buy':0, 'sell':1, 'hold':0, 'qty':quantity}
                
                with open('./parameters.json', 'w') as param:
                    json_object = json.dumps(parameters_main, param)
                    param.close()

            
            elif shares_held==old_shares_held:
                parameters_main = {'buy':0, 'sell':0, 'hold':1, 'qty':0}
                
                with open('./parameters.json', 'w') as param:
                    json_object = json.dumps(parameters_main, param)
                    param.close()

            else:
                pass
            print(output)
            # call selenium script when there is change in the value
            # print(balance)
            # print(net_worth)
            # print(num_shares_sold)
            # print(shares_held)
            # output.extend(renderLog)
            # balance.extend(env.get_attr('balance'))
            # # print(env.get_attr('balance'))
            # net_worth.extend(env.get_attr('net_worth'))
            # # total_shares_sold.extend(env.get_attr('total_shares_sold'))
            # # shares_held.extend(env.get_attr('shares_held'))

            # num_shares_sold.extend(env.get_attr('num_shares_sold'))
            # shares_held.extend(env.get_attr('num_shares'))

            # rewards_list.append(str(rewards[0]) + '\n')
            # actions_list.append(str(action[0][0]) + '\n')
            counter=counter-1
            time.sleep(60)
    log.writelines(output)
    log.close()

with open('./logs/rewards_15-02-2023.txt', 'w') as log:
    log.writelines(rewards_list)
    log.close()

with open('./logs/actions_15-02-2023.txt', 'w') as log:
    log.writelines(actions_list)
    log.close()

    # df.to_csv('./INFY.csv')


# date_str = '2023-02-06 09:15:00'
# datetime_object = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
# print(datetime_object)

# df = pd.read_csv('./data/TCS-Today.csv')

# print(df.loc[df['Datetime']=='2023-02-06 09:15:00+05:30'])

# env = dummy_vec_env.DummyVecEnv([lambda: EnvEnv(df.loc[df['Datetime']== f'{str(datetime_object)}+05:30'])])


    



# model = PPO("MlpPolicy", env, verbose=1, seed=777)

# model.learn(total_timesteps=555555) #2021-02-04 13:07:00+05:30
# model.learn(total_timesteps=50) #2021-02-04 13:07:00+05:30

# model.save('./save/model76')

