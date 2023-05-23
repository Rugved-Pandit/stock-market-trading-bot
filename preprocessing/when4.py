import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 

plt.rcParams.update({'font.size': 20})

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




dates = df['date'][555669:555669+len(r)].tolist()


# for i in range(len(dates)):
#     dates[i] = dates[i][:10]




# for i in range(len(dates)):
#     dates[i] = dates[i][:10]



fig = plt.figure()
plt.tight_layout()
fig.set_size_inches(15,19)
plt.subplots_adjust(left=0.08, right=0.92, bottom=0.08, top=0.92)
gs = fig.add_gridspec(1, 2)

aa = fig.add_subplot(gs[0, 0:])
fmt_dates = mdates.DayLocator(interval=25000)

aa.xaxis.set_major_locator(fmt_dates)
plt.grid()
aa.plot(dates, r2, label="Net Worth")
aa.plot(dates, r3, label="Total Return")
aa.plot(dates, r,label="Saving")
# aa.plot(df['date'][1:100000], df['net worth cumsum'][1:100000], label="cum net worth")
aa.set_title("Cumulative Return in (Rs.)")
plt.legend()
plt.show()