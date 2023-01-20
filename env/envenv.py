import gym
from gym.spaces import Box, Discrete
import numpy as np
import pandas_ta
import matplotlib.pyplot as plt
import random


INITIAL_ACCOUNT_BALANCE = 100000

class EnvEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, df, render_mode=None, size=5):
        
        self.df = df
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.num_shares = 0
        self.current_step = 40
        self.num_shares_sold = 0
        self.transaction_cost = 0
        self.total_transaction_cost = 0

        self.exploration_rate = 1
        self.exploration_rate_min = 0.01
        self.exploration_rate_decay = 0.001

        self.training_output = []
        self.training_rewards = []
        self.training_steps = []
        self.training_actions = []

        #rsi
        self.rsi = pandas_ta.rsi(df['close'], length=14)

        #macd
        ShortEMA = self.df.close.ewm(span=12, adjust=False).mean()
        # Calculate the long term exponential moving average (EMA)
        LongEMA = self.df.close.ewm(span=26, adjust=False).mean()
        # Calculate the MACD line
        self.MACD = ShortEMA - LongEMA
        # Calculate the signal line
        self.signal = self.MACD.ewm(span=9, adjust=False).mean()

        self.isTraining = True

        #balance, close, n.shares, macd, rsi
        #balance, close, n.shares, net_worth, rsi
        #balance, close, n.shares, net_worth, rsi, macd, signal
        #balance, close, n.shares, rsi, macd, signal
        self.observation_space = Box(-np.inf, np.inf, shape=(6,))

        # buy - hold - sell
        self.action_space = Box(-1, 1, shape=(1,))
        # self.action_space = Discrete(3)


    def _get_obs(self):
        obs = np.array([
            self.balance,
            self.df.loc[self.current_step, 'close'],
            self.num_shares,
            # self.net_worth,
            self.rsi[self.current_step],
            self.MACD[self.current_step],
            self.signal[self.current_step],
            ])

        return obs

    #DISCRETE ACTION
    def step_discrete(self, action):
        self.current_step +=1
        # print(self.current_step)

        if self.isTraining:
            if self.current_step > 555555:
                self.current_step = 40
        else:
            if self.current_step > len(self.df.loc[:, 'open'].values) -10:
                self.current_step = 555600

        old_net_worth = self.net_worth

        current_price = self.df.loc[self.current_step-1, "close"]
        
        self.transaction_cost = 0

        #buy
        if action ==0:
            if current_price ==0:
                is_buy_possible = False
            else:
                is_buy_possible = ((self.balance-20) - current_price) >0

            if is_buy_possible:
                self.transaction_cost = min(20, current_price*0.03)
                
                self.num_shares += 1
                self.balance -= current_price
        
        #sell
        elif action ==2 and self.num_shares>0 :
            self.transaction_cost = min(20, current_price*0.03)
            self.num_shares_sold +=1

            self.num_shares -= 1
            self.balance += current_price
        
        #NO TRANSACTION COST
        self.transaction_cost = 0
        
        self.balance -= self.transaction_cost
        self.total_transaction_cost += self.transaction_cost

        self.net_worth = self.balance + self.num_shares * current_price
        
        terminated = self.net_worth <=0

        reward = self.net_worth - old_net_worth
        # reward = 1 if ((self.net_worth - old_net_worth) > 0 ) else -1
        # if self.net_worth - old_net_worth >1:
        #     reward = math.log(self.net_worth - old_net_worth)
        # elif self.net_worth - old_net_worth <-1:
        #     reward = -math.log(old_net_worth - self.net_worth)
        # else:
        #     reward = old_net_worth - self.net_worth
        # reward = 1/(1 + np.exp(old_net_worth - self.net_worth))
        # reward = self.net_worth-INITIAL_ACCOUNT_BALANCE
        
        observation = self._get_obs()

        return observation, reward, terminated, {}

    #CONTINUOUS ACTION
    def step(self, action):
        action = action[0]
        self.current_step +=1
        # print(self.current_step)

        # if self.isTraining:
        #     if self.current_step > 555555:
        #         self.current_step = 40
        #         print('training')
        # else:
        #     if self.current_step > len(self.df.loc[:, 'open'].values) -10:
        #         self.current_step = 555600

        old_net_worth = self.net_worth

        current_price = self.df.loc[self.current_step-1, "close"]
        
        # print(self.current_step)
        # print(self.df.loc[self.current_step-1, "date"])
        
        self.transaction_cost = 0

        # # EXPLORATION EXPLOITATION
        # exploration_rate_threshold = random.uniform(0, 1)
        # if exploration_rate_threshold > self.exploration_rate:
        #     action = random.uniform(-1, 1)
        
        # # Exploration rate decay
        # self.exploration_rate = self.exploration_rate_min + (1 - self.exploration_rate_min) * np.exp(-self.exploration_rate_decay * self.current_step / 100)

        #buy
        if action < -0.33:
            percentage_buy = abs(action)
            if current_price ==0:
                num_buy_possible = 0
            else:
                num_buy_possible = int((self.balance-20) / current_price)
            num_buying = int(num_buy_possible * percentage_buy)

            if num_buying >0:
                self.transaction_cost = min(20, num_buying*current_price*0.03)
                
            self.num_shares += num_buying
            self.balance -= num_buying*current_price
        
        #sell
        elif action > 0.33:
            percentage_sell = action
            num_selling = int(self.num_shares * percentage_sell)
            if num_selling >0:
                self.transaction_cost = min(20, num_selling*current_price*0.03)
                self.num_shares_sold +=num_selling

            self.num_shares -= num_selling
            self.balance += num_selling*current_price
        
        #TRANSACTION COST
        # self.balance -= self.transaction_cost

        self.total_transaction_cost += self.transaction_cost

        self.net_worth = self.balance + self.num_shares * current_price
        
        terminated = self.net_worth <=0

        # reward = self.net_worth - old_net_worth - self.transaction_cost
        reward = self.net_worth - old_net_worth
        
        observation = self._get_obs()

        #trying logging
        self.training_output.append('Step: ' + str(self.current_step) + '\n')
        self.training_output.append('Action: ' + str(action) + '\n')
        self.training_output.append('Balance: ' + str(self.balance) + '\n')
        self.training_output.append('Shares held: ' + str(self.num_shares) + '\n')
        self.training_output.append('num_shares_sold: ' + str(self.num_shares_sold) + '\n')
        self.training_output.append('total_transaction_cost: ' + str(self.total_transaction_cost) + '\n')
        self.training_output.append('Net worth: ' + str(self.net_worth) + '\n')
        self.training_output.append('Profit: ' + str(self.net_worth - INITIAL_ACCOUNT_BALANCE) + '\n')
        self.training_output.append('\n')

        self.training_rewards.append(str(reward)+'\n')
        self.training_steps.append(str(self.current_step)+'\n')
        self.training_actions.append(str(action) + '\n')

        return observation, reward, terminated, {}

    def reset(self):
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.num_shares = 0
        self.transaction_cost = 0
        self.total_transaction_cost = 0
        self.num_shares_sold = 0

        # self.current_step = 555600

        observation = self._get_obs()

        # self.isTraining = False

        with open('./logs/log76training.txt', 'w') as log:
            log.writelines(self.training_output)
            log.close()
        
        with open('./logs/log76training-rewards.txt', 'w') as log:
            log.writelines(self.training_rewards)
            log.close()

        with open('./logs/log76training-actions.txt', 'w') as log:
            log.writelines(self.training_actions)
            log.close()

        return observation


    def render(self,  mode='human', close=False):
        output = []
        output.append('Step: ' + str(self.current_step) + '\n')
        output.append('Balance: ' + str(self.balance) + '\n')
        output.append('Shares held: ' + str(self.num_shares) + '\n')
        output.append('num_shares_sold: ' + str(self.num_shares_sold) + '\n')
        output.append('total_transaction_cost: ' + str(self.total_transaction_cost) + '\n')
        output.append('Net worth: ' + str(self.net_worth) + '\n')
        output.append('Profit: ' + str(self.net_worth - INITIAL_ACCOUNT_BALANCE) + '\n')
        output.append('\n')
        return output