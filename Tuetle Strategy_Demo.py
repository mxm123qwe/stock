# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:29:31 2023

@author: mxm18
"""
import matplotlib
#import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#zgpa.to_csv('stock_data.csv', index=False) 
# 从 CSV 文件中读取数据
#zgpa = pd.read_csv('C:/Users/mxm18/Desktop/量化/data.csv')
# 读取 CSV 文件
file_path = 'C:/Users/mxm18/Desktop/股票-趋势类-海龟交易-海龟策略（附书籍）/data/data.csv'  # 修改为你要读取的文件路径
zgpa = pd.read_csv(file_path)
#检查是否下载成功
zgpa.head(5)
#创建一个名为turtle的数据表，使用原始数据表的日期序号
turtle = pd.DataFrame(index = zgpa.index)
#设置唐奇安通道的上沿为前5天股价的最高点
turtle['high'] = zgpa['close'].shift(1).rolling(5).max()
#设置唐奇安通道的下沿为过去5天的最低点
turtle['low'] = zgpa['close'].shift(1).rolling(5).min()
#当股价突破上沿时，发出买入信号
turtle['buy'] = zgpa['close'] > turtle['high']
#当股价突破下沿时，发出卖出信号
turtle['sell'] = zgpa['close'] < turtle['low']
#检查信号创建情况
turtle.tail()
#初始的订单状态为0
turtle['orders']=0
#初始的仓位为0
position = 0
#设置循环，遍历turtle数据表
for k in range(len(turtle)):
    #当买入信号为True且仓位为0时下单买入1手
    if turtle.buy[k] and position ==0:
        #修改对应的orders值为1
        turtle.orders.values[k] = 1
        #仓位也增加1手
        position = 1
    #而当卖出信号为True且有持仓时买出1手
    elif turtle.sell[k] and position > 0:
        #orders的值修改为-1
        turtle.orders.values[k] = -1
        #仓位相应清零
        position = 0
#检查是否成功
turtle.tail(15)
#创建10*5的画布
plt.figure(figsize=(10,5))
#绘制股价的折线图
plt.plot(zgpa['close'],lw=2)
#绘制唐奇安通道上沿
plt.plot(turtle['high'],lw=2, ls='--',c='r')
#绘制唐奇安通道下沿
plt.plot(turtle['low'],lw=2,ls='--',c='g')
#标出买入订单，用正三角标记
plt.scatter(turtle.loc[turtle.orders==1].index,
           zgpa['close'][turtle.orders==1],
           marker='^',s=80,color='r',label='Buy')
#标出卖出订单，用倒三角标记
plt.scatter(turtle.loc[turtle.orders==-1].index,
           zgpa['close'][turtle.orders==-1],
           marker='v',s=80,color='g',label='Sell')
#添加网格、图注并显示
plt.legend()
plt.xticks([0,12,24,36,48])
plt.grid()
plt.show()
print('============Test===============')
# 新建一个positions表，序号和strategy数据表保持一致
#再次给小瓦2万块初始资金
initial_cash = 20000
#创建新的数据表，序号和turtle数据表一致
positions = pd.DataFrame(index=turtle.index).fillna(0.0)
#每次交易为1手，即100股，仓位即买单和卖单的累积加和
positions['stock'] = 100 * turtle['orders'].cumsum()
#创建投资组合数据表
portfolio = positions.multiply(zgpa['close'], axis=0)
#持仓市值为持仓股票数乘以股价
portfolio['holding_values'] = (positions.multiply(zgpa['close'], axis=0))
#计算出仓位的变化
#剩余的现金是初始资金减去仓位变化产生的现金流累计加和
portfolio['cash'] = initial_cash - (positions.diff().multiply(zgpa['close'], axis=0)).cumsum()
#总资产即为持仓股票市值加剩余现金
portfolio['total'] = portfolio['cash'] + portfolio['holding_values']
portfolio.tail(13)
plt.figure(figsize=(10,5))
plt.plot(portfolio['total'])
plt.plot(portfolio['holding_values'],'--')
plt.grid()
plt.legend()
plt.xticks([0,12,24,36,48])
plt.show()