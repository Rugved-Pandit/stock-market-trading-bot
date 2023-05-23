import gym
import numpy as np
import torch
from envenv import EnvEnv
from ppo_torch import Agent
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from stockstats import StockDataFrame as Sdf
import time
import json

global old_shares_held
old_shares_held = 0
old_shares_sold = 0
flag=True
parameters_main = {'buy':False, 'sell':False, 'hold':False, 'qty':0}


tech_indicator_list = ['macd',
 'boll_ub',
 'boll_lb',
 'rsi_30',
 'cci_30',
 'dx_30',
 'close_30_sma',
 'close_60_sma']

def add_technical_indicator(data):
    """
    calculate technical indicators
    use stockstats package to add technical inidactors
    :param data: (df) pandas dataframe
    :return: (df) pandas dataframe
    """
    df = data.copy()
    df = df.sort_values(by=["tic", "date"])
    stock = Sdf.retype(df.copy())
    unique_ticker = stock.tic.unique()

    for indicator in tech_indicator_list:
        indicator_df = pd.DataFrame()
        for i in range(len(unique_ticker)):
#             print("Number: " + str(i))
            try:
                temp_indicator = stock[stock.tic == unique_ticker[i]][indicator]
                temp_indicator = pd.DataFrame(temp_indicator)
                temp_indicator["tic"] = unique_ticker[i]
                temp_indicator["date"] = df[df.tic == unique_ticker[i]][
                    "date"
                ].to_list()
                indicator_df = indicator_df.append(
                    temp_indicator, ignore_index=True
                )
                # print(str(i))
            except Exception as e:
                print(e)
        df = df.merge(
            indicator_df[["tic", "date", indicator]], on=["tic", "date"], how="left"
        )
    df = df.sort_values(by=["date", "tic"])
    return df

# df = pd.read_csv('C:/Users/Rugved/GitHub/stock-market-trading-bot/freecodecamp-test/ADANIPORTS-TA.csv')
df = pd.read_csv('./INFY_historical.csv')
env = EnvEnv(df)
# N = 20
batch_size = 5
n_epochs = 4
alpha = 0.0003
model = Agent(n_actions=env.action_space.n, batch_size=batch_size,
                  alpha=alpha, n_epochs=n_epochs,
                  input_dims=env.observation_space.shape)
model.load_models()

obs = env.reset()

with open('./logs/log152.txt', 'w') as log:
    output = []
    balance = []
    net_worth = []
    net_worth2 = []
    total_shares_sold = []
    shares_held = []

    num_shares_sold = []
    rewards_list = []
    actions_list = []
    n_steps=0

    
    savings = 0
    savings_list = []

    # for i in range(10):
    env.current_step = 555669
    # for i in range(int((650000-555600))):
    counter = 375
    while counter:
        df = yf.download( tickers="INFY.NS", period="1d", interval="1m", ignore_tz=False, group_by='ticker', auto_adjust=True, repair=False, prepost=True, threads=True, proxy=None)
       
        tic = ['INFY']*(df.shape[0])
        df['tic'] = tic
        df.reset_index(inplace=True)
        print(df.columns)
        df.rename(columns={"Datetime": "date", "Open": "open", "High": "high","Low":"low","Close":"close"},
                inplace=True)
        df = add_technical_indicator(df)
        env.current_price = float(df['close'].tail(1))
        df = df.tail(61)
        ti_df = df.head(60)
        pred = df.tail(1)

        # if len(df)>prev_val:
        #     prev_val = len(df)
        #     df.to_csv('./data/ADANIPORTS-28-03-2023.csv')
        #     dataa = pd.read_csv('./data/ADANIPORTS-28-03-2023.csv')
        #     dataa.rename(
        #         columns={"Datetime": "datetime", "Open": "open", "High": "high","Low":"low","Close":"close"},
        #         inplace=True)
        
        obs = np.array([env.balance, float(df['close'].tail(1)), env.num_shares, float(df['macd'].tail(1)), float(df['boll_ub'].tail(1)), float(df['boll_lb'].tail(1)), float(df['rsi_30'].tail(1)), float(df['cci_30'].tail(1)), float(df['dx_30'].tail(1)),float(df['close_30_sma'].tail(1)), float(df['close_60_sma'].tail(1))])
        action, prob, val = model.choose_action(obs)
        obs, rewards, done, info = env.step(action)
        n_steps += 1
        renderLog = env.render()

        output.extend(renderLog)
        balance.append(env.__getattribute__('balance'))
        with open('./BALANCE.txt', 'w') as bal:
                bal.writelines(str(balance[0]))
                bal.close()
        # print(env.__getattribute__('balance'))
        net_worth.append(env.__getattribute__('net_worth'))
        net_worth2.append(str(env.__getattribute__('net_worth'))+'\n')
        # total_shares_sold.extend(env.__getattribute__('total_shares_sold'))
        # shares_held.extend(env.__getattribute__('shares_held'))

        num_shares_sold.append(env.__getattribute__('num_shares_sold'))
        shares_held.append(env.__getattribute__('num_shares'))

        rewards_list.append(str(rewards) + '\n')
        actions_list.append(str(action) + '\n')

        if env.net_worth > 102000:
                    if env.num_shares >1:
                        print('!SAVING!')
                        env.num_shares -= 1
                        # env.net_worth = env.current_price
                        # env.balance += env.current_price
                        savings += env.current_price
        savings_list.append(str(savings) + '\n')
        if flag:
            old_shares_held = shares_held[-1]
            flag=False
        else:
            old_shares_held = shares_held[-2]
        # print("old",old_shares_held)
        # print("new",shares_held)
            # if shares_held!=old_shares_held:
                # run_selenium(shares_held, num_shares_sold)
        if int(shares_held[-1])>int(old_shares_held):
            quantity = shares_held[-1] - old_shares_held
            parameters_main = {'buy':1, 'sell':0, 'hold':0, 'qty':quantity}
            # print("in buy ")
            with open('./parameters.json', 'w') as param:
                json_object = json.dump(parameters_main, param)
                param.close()
        
        elif shares_held[-1]<old_shares_held:
            quantity = old_shares_held - shares_held[-1]
            parameters_main = {'buy':0, 'sell':1, 'hold':0, 'qty':quantity}
            
            with open('./parameters.json', 'w') as param:
                json_object = json.dump(parameters_main, param)
                param.close()

        
        elif shares_held[-1]==old_shares_held:
            parameters_main = {'buy':0, 'sell':0, 'hold':1, 'qty':0}
            
            with open('./parameters.json', 'w') as param:
                json_object = json.dump(parameters_main, param)
                param.close()

        else:
            pass
        print(output)
            
        
        counter = counter - 1
        log.writelines(output)
        time.sleep(60)                
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

    plt.savefig('./plots/log152plot.png')
    plt.show()

with open('./logs/log152rewards.txt', 'w') as log:
    log.writelines(rewards_list)
    log.close()

with open('./logs/log152actions.txt', 'w') as log:
    log.writelines(actions_list)
    log.close()

with open('./logs/log152savings.txt', 'w') as log:
    log.writelines(savings_list)
    log.close()

with open('./logs/log152networth.txt', 'w') as log:
    log.writelines(net_worth2)
    log.close()

print('savings ', savings)