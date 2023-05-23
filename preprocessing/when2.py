import matplotlib.pyplot as plt
import pandas as pd

# with open('./logs/log132training-rewards.txt', 'r') as log:
# # with open('./logs/log67rewards.txt', 'r') as log:
# # with open('./logs/log66actions.txt', 'r') as log:
#     r = log.readlines()
#     r =  [float(i[:-1]) for i in r]
#     x =  [l for l in range(len(r))]
#     # print(r)
#     plt.plot(x, r)
#     plt.figure(figsize=(16,9))
#     # plt.savefig('./plots/log64training-rewards-plot.png')
#     plt.show()

with open('./logs/log132actions.txt', 'r') as log:
    a = log.readlines()
    a =  [float(i[:-1]) for i in a]
    # x =  [l for l in range(len(a))]
    df = pd.read_csv('./data/INFY.csv')

    y = df['close'][555669:(650000-555600 + 555669)]
    x =  [l for l in range(len(y))]
    # plt.xkcd()
    plt.figure(figsize=(16,9))
    plt.plot(x,y)
    # plt.savefig('./close-plots/ADANIGREEN.png')
    plt.xlabel('timesteps')
    plt.ylabel('Rs')
    # plt.title('Closing price of ADANIPORTS')
    
    col =[]
  
    for i in range(0, len(x)):
        print(a)
        if a[i]<10:
            col.append('red')  
        elif a[i]>10:
            col.append('green')
        else:
            col.append('yellow')
    
    # for i in range(len(x)):
    #     # plotting the corresponding x with y and respective color
    #     plt.scatter(x[i], y[i], c = col[i], s = 10, linewidth = 0)

    plt.scatter(x, y, c = col, alpha=0.5)
    plt.show()