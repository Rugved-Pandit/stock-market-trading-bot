import matplotlib.pyplot as plt

with open('./logs/log64training-rewards.txt', 'r') as log:
    r = log.readlines()
    r =  [float(i[:-1]) for i in r]
    x =  [l for l in range(len(r))]
    # print(r)
    plt.plot(x, r)
    plt.figure(figsize=(16,9))
    plt.savefig('./plots/log64training-rewards-plot.png')
    plt.show()