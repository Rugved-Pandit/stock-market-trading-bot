import matplotlib.pyplot as plt

with open('./logs/log64training-rewards.txt', 'r') as log:
    r = log.readlines()
    r =  [float(i[:-1]) for i in r]
    # x =  [l for l in range(len(r))]
    x =  [l for l in range(10000)]
    # print(r)
    plt.plot(x, r[:10000])
    plt.figure(figsize=(16,9))
    # plt.savefig('./plots/log64training-rewards-plot.png')
    plt.show()