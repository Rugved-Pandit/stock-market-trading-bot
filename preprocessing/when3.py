import matplotlib.pyplot as plt
import pandas as pd

with open('./logs/log151savings.txt', 'r') as log:
# with open('./logs/log67rewards.txt', 'r') as log:
# with open('./logs/log66actions.txt', 'r') as log:
    r = log.readlines()
    r =  [float(i[:-1])/100000 for i in r]
    x =  [l for l in range(len(r))]
    # print(r)

with open('./logs/log151networth.txt', 'r') as log:
# with open('./logs/log67rewards.txt', 'r') as log:
# with open('./logs/log66actions.txt', 'r') as log:
    r2 = log.readlines()
    r2 =  [float(i[:-1])/100000 for i in r2]
    # x =  [l for l in range(len(r2))]
    # print(r)

r3=[]
for i in range(len(r)):
    r3.append(r[i]+r2[i])

###
df = pd.read_csv('./data/ADANIPORTS.csv')

y = df['close'][555669:555669+len(r)]
y =  [l/567.7 for l in y]
# y =  [l/1280 for l in y]
# plt.xkcd()
# plt.figure(figsize=(16,9))
# plt.plot(x,y)
# # plt.savefig('./close-plots/ADANIGREEN.png')
# plt.xlabel('timesteps')
# plt.ylabel('Rs')
# plt.title('Closing price of ADANIPORTS')


plt.plot(x, r2)
plt.plot(x, r3)
plt.plot(x, r)
# plt.plot(x, y)
plt.figure(figsize=(16,9))
# plt.savefig('./plots/plot151.png')
plt.show()