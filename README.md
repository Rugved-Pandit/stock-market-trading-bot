# Intraday Stock Market Trading Bot

<!-- In this study, Reinforcement Learning (RL) techniques are used to develop trading strategies for the stock market. Conventional trading strategies rely on human intuition and the examination of historical data to make forecasts, whereas RL agents can automatically learn the best trading strategies through market interaction. The Proximal Policy Gradient (PPO) agent is used in this paper to produce trading policies using real-world stock market data. The tests covered in the paper are conducted on the notoriously turbulent Indian intraday market. The findings of this study can be helpful to financial institutions, RL researchers, and those interested in the use of RL approaches for stock trading. -->

This repository houses implementation of a trading bot that leverages reinforcement learning techniques to make informed sequences of good decisions in an intraday stock trading environment. Conventional trading strategies rely on human intuition and the examination of historical data to make forecasts, whereas RL agents can automatically learn the best trading strategies through market interaction. The Proximal Policy Gradient (PPO) agent is employed to produce trading policies using real-world stock market data. 
 
 ## Our Goal: 
Given the current closing price of the stock in the market, calculate all the necessary parameters related to the stock. Determine and execute the best possible action based on the calculated parameters. The action is to buy or sell a certain number of stocks, or to hold the already owned stocks.

![image](https://drive.google.com/uc?export=view&id=1HncIxAdTvKeS-ymvzjH9JntDJXL5N7mC)

## How we did it! 
 * A type of machine learning called Reinforcement Learning allows an agent to pick up new skills by interacting with its surroundings and getting feedback in the form of rewards or penalties.  
 * A well-liked approach for describing decision-making issues in reinforcement learning is the Markov Decision Process (MDP). The probabilities of changing from one state to another and the incentives connected to each state-action pair are defined by an MDP, which is made up of a set of states, actions, and rewards. The Markov property, which asserts that the decision of transitioning to the next state depends only on the present state and action and not on the history of prior states and actions, is the fundamental premise behind MDPs.

## The parameters for the agent in MDP

* State (s) = A vector that includes
the current stock price, technical indicators for the stock, total balance, the
current total net worth (sum of balance and price of owned stocks), savings.

* Action (a) = A vector of actions.
The permitted actions for a stock are buying, holding and selling. The action
space is defined as a set of Discrete numbers ranging from 0 to 20. The
divergence point is at the value of 10, the numbers preceding it define sell
and the degree of sell
and the numbers exceeding it define buy and the degree
of buy. 

* Reward (r) =The direct reward given
to the model, gauged on the quality of action. Defined in our case as
               
   ## $r = n_t - n_{t-1} + \frac{n_t - b}{b} * 10$


   Where, r: reward, : net worth at time t, b: initial balance
   The novel reward function has two terms, first is the difference in net worth now and a step prior. This tells the model how it is performing each step. Second is the profit term. This keeps a long term track of how much profit was made since beginning. The reason for using two terms is that the first term is shallow, it only tracks the difference between last step and now, but it is necessary to learn about immediate actions, and the second term helps the model look deeper and generate higher overall profit.
   
* Market Liquidity: Allows for quick execution of orders at the close price. It is anticipated that the reinforcement trading agent won't have an impact on the stock market.
* Positive Balance: A negative balance should not be produced by the permitted acts.

## Environment description

An environment was meticulously constructed to imitate real-world trading before training a deep reinforcement trading agent, enabling the agent to interact with and learn from its surroundings. In order to trade effectively, a variety of facts must be considered, including historical stock prices, current share prices, technical indicators, etc. 
The environment utilized for training the agents comprises several financial technical indicators which are calculated using historical stock prices. The technical indicators used are: 
* MACD
* Bollinger Bands
* RSI
* CCI
* Directional Movement Index
* SMA 

## Agent Training

Continuous learning methodology was utilized to train the agents over historical stock data for which technical indicators were added. The way the agent learnt in the environment is depicted below: 

![image](https://drive.google.com/uc?export=view&id=1GnIky4XtkFTblo30DQbTSUSIbYIyaeXQ)

<!-- <a href="https://drive.google.com/uc?export=view&id=1GnIky4XtkFTblo30DQbTSUSIbYIyaeXQ"><img src="https://drive.google.com/uc?export=view&id=1GnIky4XtkFTblo30DQbTSUSIbYIyaeXQ" style="width: 650px; max-width: 100%; height: auto" title="Stock Training Process" /> -->

Whilst performing the training process it was observed that the agent would often get stuck in local minima and as a result would lead to stagnation. This adversely affects trading performance and the ability of the agent to learn effectively. The solution to the stagnation problem is two-fold, the first step being to add random steps to increase exploration. Manually increasing exploration of the model ensures the model does not stagnate and learns more. This was employed by adding random steps at a rate of 5% per step taken during training. The second way to combat the stagnation problem was to reset the environment every 100,000 steps, which includes resetting the current balance, net worth and shares held. These two methods acting together ensured the agent constantly kept learning.

## Novel tactic of savings

* A novel tactic was employed to save the profits made by the model. After a certain threshold of profit was reached, the agent was forced to sell a stock and store the profit from that action in the “savings” variable. 
* The agent could trade with whatever it had left after the subtraction operation and could not access the capital in the savings section. This promoted a way to safeguard profits from time to time and ensured consistent profits. 


## Observations and Results

The models created were tested with different environments and on different stocks in the Indian Stock Market. 

![image](https://drive.google.com/uc?export=view&id=10PtukdCYJgu6bl4iXnlFHXMd-yre2Sep)

The figure above tracks the movement of net worth, total return and savings over the course of February 2021 till February 2022 for the INFY stock. The total return is calculated by adding up the net worth and saving variables as mentioned in the methodology. The total result sees a consistent growth over the months returning a final cumulative return of 30.61%. The initial invested amount was 100,000 INR, after performing the backtesting trades for a year the final observed values for net worth and savings were 89,396 and 40,977 respectively, leading to a total return of 130,613 INR. 





