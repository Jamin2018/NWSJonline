# -*- coding: utf-8 -*-
import os
import pandas as pd
import plotly.offline as off
import re
from sqlalchemy import create_engine

off.init_notebook_mode(connected=False)

df = pd.read_csv('0211-0225bak.csv',usecols=[1, 2, 6, 7, 17, 21, 22, 24, 26,32])


df_sku = df['sku'].dropna()
r = r'(.*?)-'
sku_name_set = set()
for i in df_sku.values:
    a = re.match(r, i).group(1)
    sku_name_set.add(a)
dic = {}
for i in sku_name_set:
    r = r'(%s)-' % i
    # print(df_csv['sku'].index)
    m = df['sku'].fillna('0')
    dfs = df[(m.str.contains(r, na=True)) & (df['transaction-type'] == 'Order')]  # 分别筛选各个系列的详细数据
    for i in dfs.groupby('order-id'):
        i[1]['quantity-purchased'] = i[1]['quantity-purchased'].sum()
        i[1]['price-amount'] = i[1]['price-amount'].sum()
        i[1]['item-related-fee-amount'] = i[1]['item-related-fee-amount'].sum()
        i[1]['promotion-amount'] = i[1]['promotion-amount'].sum()
        m = i[1].drop_duplicates()
        if m.shape[0] > 1:
            print m
        # dic[i] = i[1]
    # k = dfs['quantity-purchased'].groupby(dfs['posted-date'])
    # print i,':',k.sum()



# print i.shape[0]
# print df[(df.index == '111-3543110-8044230')]