import matplotlib.pyplot as plt
import pandas as pd

with open('./logs/log69training-rewards.txt', 'r') as log:
    r = log.readlines()
    r =  [float(i[:-1]) for i in r]
    # x =  [l for l in range(len(r))]
    x =  [l for l in range(10000)]
    # print(r)
    plt.plot(x, r[:10000])
    plt.figure(figsize=(16,9))
    # plt.savefig('./plots/log64training-rewards-plot.png')
    plt.show()

# with open('./logs/log67actions.txt', 'r') as log:
#     a = log.readlines()
#     a =  [float(i[:-1]) for i in a]
#     # x =  [l for l in range(len(a))]
#     df = pd.read_csv('./data/YESBANK.csv')

#     y = df['close'][557097:651497]
#     x =  [l for l in range(len(y))]
#     # plt.xkcd()
#     plt.figure(figsize=(16,9))
#     plt.plot(x,y)
#     # plt.savefig('./close-plots/ADANIGREEN.png')
#     plt.xlabel('timesteps')
#     plt.ylabel('Rs')
#     # plt.title('Closing price of ADANIPORTS')
    
#     col =[]
  
#     for i in range(0, len(x)):
#         if a[i]<-0.33:
#             col.append('red')  
#         elif a[i]>0.33:
#             col.append('green')
#         else:
#             col.append('yellow')
    
#     # for i in range(len(x)):
#     #     # plotting the corresponding x with y and respective color
#     #     plt.scatter(x[i], y[i], c = col[i], s = 10, linewidth = 0)

#     plt.scatter(x, y, c = col, alpha=0.5)
#     # plt.legend(['close price', 'red', 'yellow', 'green'])
#     plt.title('red: buy, yellow: hold, red: sell')
#     plt.show()