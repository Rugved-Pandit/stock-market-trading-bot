import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np

MAX_ACCOUNT_BALANCE = 2147483647
MAX_NUM_SHARES = 2147483647
MAX_SHARE_PRICE = 10000
MAX_OPEN_POSITIONS = 5
# MAX_STEPS = 20000
MAX_STEPS = 2147483647

INITIAL_ACCOUNT_BALANCE = 10000


class StockTradingEnv(gym.Env):
    """A stock trading environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(StockTradingEnv, self).__init__()

        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)

        # Actions of the format Buy x%, Sell x%, Hold, etc.
        # self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]))

        # Prices contains the OHCL values for the last five prices
        # self.observation_space = spaces.Box(low=0, high=1, shape=(6, 6), dtype=np.float16)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6, 6)) #balance, close, n.shares, macd, rsi

        self.current_step = 0

        self.profit = 0

    def _next_observation(self):
        # Get the stock data points for the last 5 days and scale to between 0-1
        # frame = np.array([
        #     self.df.loc[self.current_step: self.current_step +
        #                 5, 'open'].values / MAX_SHARE_PRICE,
        #     self.df.loc[self.current_step: self.current_step +
        #                 5, 'high'].values / MAX_SHARE_PRICE,
        #     self.df.loc[self.current_step: self.current_step +
        #                 5, 'low'].values / MAX_SHARE_PRICE,
        #     self.df.loc[self.current_step: self.current_step +
        #                 5, 'close'].values / MAX_SHARE_PRICE,
        #     self.df.loc[self.current_step: self.current_step +
        #                 5, 'volume'].values / MAX_NUM_SHARES,
        # ])

        frame = np.array([
            self.df.loc[self.current_step: self.current_step +
                        5, 'open'].values,
            self.df.loc[self.current_step: self.current_step +
                        5, 'high'].values,
            self.df.loc[self.current_step: self.current_step +
                        5, 'low'].values,
            self.df.loc[self.current_step: self.current_step +
                        5, 'close'].values,
            self.df.loc[self.current_step: self.current_step +
                        5, 'volume'].values,
        ])

        # Append additional data and scale each value to between 0-1
        # obs = np.append(frame, [[
        #     self.balance / MAX_ACCOUNT_BALANCE,
        #     self.max_net_worth / MAX_ACCOUNT_BALANCE,
        #     self.shares_held / MAX_NUM_SHARES,
        #     self.cost_basis / MAX_SHARE_PRICE,
        #     self.total_shares_sold / MAX_NUM_SHARES,
        #     self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),
        # ]], axis=0)

        obs = np.append(frame, [[
            self.balance,
            self.max_net_worth,
            self.shares_held,
            self.cost_basis,
            self.total_shares_sold,
            self.total_sales_value,
        ]], axis=0)

        return obs

    def _take_action(self, action):
        # Set the current price to a random price within the time step
        # current_price = random.uniform(
        #     self.df.loc[self.current_step, "open"], self.df.loc[self.current_step, "close"])
        
        current_price = self.df.loc[self.current_step, "close"]
        if current_price == 0:
            current_price = self.df.loc[self.current_step-1, "close"]

        action_type = action[0]
        amount = action[1]

        if action_type < 1:
            # Buy amount % of balance in shares

            #transaction cost
            # print("\n\nBALANCE " + str(self.balance))
            # self.balance -= 10

            total_possible = int(self.balance / current_price)
            shares_bought = int(total_possible * amount)
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price

            self.balance -= additional_cost
            self.cost_basis = (
                prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held += shares_bought

        elif action_type < 2:
            # Sell amount % of shares held

            #transaction cost
            # self.balance -= 10

            shares_sold = int(self.shares_held * amount)
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

        self.net_worth = self.balance + self.shares_held * current_price

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        if self.shares_held == 0:
            self.cost_basis = 0

    def step(self, action):
        # print(self.balance)
        # Execute one time step within the environment
        print(self.current_step)
        old_net_worth = self.net_worth
        self._take_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:, 'open'].values) - 6:
            self.current_step = 0

        delay_modifier = (self.current_step / MAX_STEPS)

        # reward = self.balance * delay_modifier

        # profit = self.net_worth - INITIAL_ACCOUNT_BALANCE
        reward = self.net_worth - old_net_worth
        # print(reward)

        done = self.net_worth <= 0

        obs = self._next_observation()

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        # Set the current step to a random point within the data frame
        # self.current_step = random.randint(
        #     0, len(self.df.loc[:, 'Open'].values) - 6)

        self.current_step = 555600  

        return self._next_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        self.profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

        # print(f'Step: {self.current_step}')
        # print(f'Balance: {self.balance}')
        # print(
        #     f'Shares held: {self.shares_held} (Total sold: {self.total_shares_sold})')
        # print(
        #     f'Avg cost for held shares: {self.cost_basis} (Total sales value: {self.total_sales_value})')
        # print(
        #     f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
        # print(f'Profit: {self.profit}')
        # print()
        
        output = []
        output.append('Step: ' + str(self.current_step) + '\n')
        output.append('Balance: ' + str(self.balance) + '\n')
        output.append('Shares held: ' + str(self.shares_held) + ' Total sold: ' + str(self.total_shares_sold) + '\n')
        output.append('Avg cost for held shares: ' + str(self.cost_basis) + ' Total sales value: ' + str(self.total_sales_value) + '\n')
        output.append('Net worth: ' + str(self.net_worth) + ' Max net worth: ' + str(self.max_net_worth) + '\n')
        output.append('Profit: ' + str(self.profit) + '\n')
        output.append('\n')
        return output
