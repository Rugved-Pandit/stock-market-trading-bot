import gym
from gym.spaces import Box
import numpy as np
import pandas_ta


INITIAL_ACCOUNT_BALANCE = 10000

class EnvEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, df, render_mode=None, size=5):
        
        self.df = df
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.num_shares = 0
        self.current_step = 20
        self.num_shares_sold = 0
        self.rsi = pandas_ta.rsi(df['close'], length=14)

        self.isTraining = True

        #balance, close, n.shares, macd, rsi
        #balance, close, n.shares, net_worth, rsi
        self.observation_space = Box(-np.inf, np.inf, shape=(5,))

        # buy - hold - sell
        self.action_space = Box(-1, 1, shape=(1,))


    def _get_obs(self):
        obs = np.array([
            self.balance,
            self.df.loc[self.current_step, 'close'],
            self.num_shares,
            self.net_worth,
            self.rsi[self.current_step]
            ])

        return obs


    def step(self, action):
        self.current_step +=1
        # print(self.current_step)

        if self.isTraining:
            if self.current_step > 555555:
                self.current_step = 20
        else:
            if self.current_step > len(self.df.loc[:, 'open'].values) -10:
                self.current_step = 555600

        old_net_worth = self.net_worth

        current_price = self.df.loc[self.current_step-1, "close"]
        
        #buy
        if action < -0.33:
            percentage_buy = abs(action)
            if current_price ==0:
                num_buy_possible = 0
            else:
                num_buy_possible = int(self.balance / current_price)
            num_buying = int(num_buy_possible * percentage_buy)
            self.num_shares += num_buying
            self.balance -= num_buying*current_price
        
        #sell
        elif action > 0.33:
            percentage_sell = action
            num_selling = int(self.num_shares * percentage_sell)
            self.num_shares -= num_selling
            self.balance += num_selling*current_price
            self.num_shares_sold +=1
        
        self.net_worth = self.balance + self.num_shares * current_price
        
        terminated = self.net_worth <=0

        reward = self.net_worth - old_net_worth
        
        observation = self._get_obs()

        return observation, reward, terminated, {}

    def reset(self):
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.num_shares = 0
        self.num_transactions = 0

        self.current_step = 555600

        observation = self._get_obs()

        self.isTraining = False

        return observation


    def render(self,  mode='human', close=False):
        output = []
        output.append('Step: ' + str(self.current_step) + '\n')
        output.append('Balance: ' + str(self.balance) + '\n')
        output.append('Shares held: ' + str(self.num_shares) + '\n')
        output.append('Net worth: ' + str(self.net_worth) + '\n')
        output.append('Profit: ' + str(self.net_worth - INITIAL_ACCOUNT_BALANCE) + '\n')
        output.append('\n')
        return output