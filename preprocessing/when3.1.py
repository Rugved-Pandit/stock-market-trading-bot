import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
from datetime import datetime

with open('./logs/log151savings.txt', 'r') as log:
    r = log.readlines()
    r =  [float(i[:-1])/100000 for i in r]
    x =  [l for l in range(len(r))]
    # print(r)

with open('./logs/log151networth.txt', 'r') as log:
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

fig = plt.figure()
plt.tight_layout()
fig.set_size_inches(15,19)
plt.subplots_adjust(left=0.08, right=0.92, bottom=0.08, top=0.92)
gs = fig.add_gridspec(1, 2)

aa = fig.add_subplot(gs[0, 0:])
fmt_dates = mdates.DayLocator(interval=25000)

print(fmt_dates)
# exit()

aa.xaxis.set_major_locator(fmt_dates)
plt.grid()
# aa.plot(dates, r2, label="Total Return")
# aa.plot(dates, r3, label="Net Worth")
# aa.plot(dates, r,label="Saving")
# aa.plot(df['date'][1:100000], df['net worth cumsum'][1:100000], label="cum net worth")

d = []
for i in range(len(y)):
    d.append('6-9-69')
aa.plot(d, r2, label="Total Return")

aa.set_title("Cumulative Return in (Rs.)")
plt.legend()
# plt.show()




#############
dates = [l[:10] for l in dates]
origin = dates
# a = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S %z') for d in origin]
a = [datetime.strptime(d, '%Y-%m-%d') for d in origin]
  
# b = ['35.764299', '20.3008', '36.94704']
  
x = matplotlib.dates.date2num(a)
formatter = matplotlib.dates.DateFormatter('%d:%m:%Y')
  
figure = plt.figure()
axes = figure.add_subplot(1, 1, 1)
  
axes.xaxis.set_major_formatter(formatter)
plt.setp(axes.get_xticklabels(), rotation = 15)
  
axes.plot(x, y)
plt.show()