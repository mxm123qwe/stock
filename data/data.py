# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:18:04 2023

@author: mxm18
"""
import tushare as ts
import pandas as pd
# 设置 tushare 的 token
ts.set_token('e7d5fc2af55a0f46a41f28ef9b81468b83c55a30e64fecd8360fe1ad')
pro = ts.pro_api()
#指定下载股票的日期范围
start_date = '2018-01-01'
end_date = '2023-06-20'
#使用ts获取数据
#将时间范围作为参数传入
zgpa = ts.get_k_data('399001',
                    start_date, end_date)
# 保存数据为 CSV 文件
#desktop_path = os.path.expanduser("~/Desktop")  # 获取桌面路径
#file_path = os.path.join(desktop_path, 'stock_data.csv')  # 拼接文件路径
#data.to_csv(file_path, index=False)
# 保存数据为 CSV 文件
file_path = 'C:/Users/mxm18/Desktop/量化/data.csv'  # 修改为你想要保存的路径和文件名
zgpa.to_csv(file_path, index=False)
#zgpa.to_csv('stock_data.csv', index=False) 
# 从 CSV 文件中读取数据
zgpa = pd.read_csv('C:/Users/mxm18/Desktop/量化/data.csv')
# 打印前几行数据
print(zgpa.head(5))
