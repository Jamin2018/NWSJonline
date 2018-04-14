# -*- coding: utf-8 -*-
import os
import pandas as pd
import re


import os
import pickle
import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import PyDataFun
import random


df = pd.read_csv('0211-0225bak.csv')

print df['settlement-start-date'].to_frame().iloc[0,0]



        # print '---' * 100
    # print i[1]


# dic = {}
# for i in sku_name_set:
#     r = r'(%s)-' % i
#     # print(df_csv['sku'].index)
#     data = df[df['sku'].str.contains(r, na=True)]  # 分别筛选各个系列的详细数据
#     dic[i] = data
#
# # print data.columns
# df = data.groupby('order-id').sum()
# print df[df['quantity-purchased']==1].head(5)