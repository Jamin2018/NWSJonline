# -*- coding: utf-8 -*-
import os
import pandas as pd
import pickle
import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import PyDataFun

with open('data.pkl','rb') as f:
    data = f.read()
    data_dict = pickle.loads(data)
    data_dict = data_dict['sku_info_dict']

product_cost_weight_path = 'product_cost_weight-sample.xlsx'
df = PyDataFun.draw_day_profit_price('YSW5402', data_dict, product_cost_weight_path = product_cost_weight_path)
print df


py.init_notebook_mode(connected=True)

trace1 = go.Scatter(
    x= df.index,
    y=df[u'每日利润'],
    mode='lines+markers',
    name='每日利润',
    line=dict(
        shape='spline'
    )
)

trace2 = go.Scatter(
    x= df.index,
    y=df[u'每日均价'],
    mode='lines',
    name='每日均价',
    line=dict(
        shape='spline'
    )
)


layout = dict(title = 'title',
              xaxis = dict(title = '每日'),
              yaxis = dict(title = '美元'),
              )
data = [trace1, trace2,]

fig = dict(data=data, layout=layout)
py.plot(fig, filename='2')