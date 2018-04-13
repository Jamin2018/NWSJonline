# -*- coding: utf-8 -*-
import os
import pickle
import pandas as pd
import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import PyDataFun




def draw_day_order_refund(df,sku_name = None):
    '''
    订单-退款-实际
    :param df:
    :param sku_name:
    :return:
    '''
    py.init_notebook_mode(connected=True)
    trace1 = go.Scatter(
        x= df.index,
        y=df[u'订单金额'],
        mode='lines+markers',
        name='订单金额',
        line=dict(
            shape='spline'
        )
    )

    trace2 = go.Scatter(
        x= df.index,
        y=df[u'退款金额'],
        mode='lines+markers',
        name='退款金额',
        line=dict(
            shape='spline'
        )
    )

    trace3 = go.Scatter(
        x= df.index,
        y=df[u'实际订单金额'],
        mode='lines+markers',
        name='实际订单金额',
        line=dict(
            shape='spline'
        )
    )
    sku_name = sku_name.encode('utf-8')
    title = sku_name+ '系列订单-退款'
    layout = dict(title = title,
                  xaxis = dict(title = '时间'),
                  yaxis = dict(title = '美元'),
                  )
    data = [trace1, trace2,trace3]
    fig = dict(data=data, layout=layout)

    filename = os.getcwd() + r'/templates/line_chart_html/order_refund_' + sku_name
    py.plot(fig, filename=filename)


def dict_line_day_sku_list():
    '''
    为绘制每日订单数提供数据
    :return:
    '''
    with open(os.getcwd()+'/media/data/data.pkl', 'rb') as f:
        data = f.read()
        data_dict = pickle.loads(data)
        sku_useful_info_dict = data_dict['sku_useful_info_dict']
        sku_name_list_sort = data_dict['sku_name_list_sort']

    sku_list = []
    for sku_name, v in sku_useful_info_dict.items():
        data = v['quantity-purchased']
        # DataFrame存入字典后取出变成series，故需要转回DataFrame，顺便设置列名
        data.name = sku_name
        data = data.to_frame(name=sku_name)
        sku_list.append(data)
        # 合并数据
    data = pd.concat(sku_list, axis=1)
    _ = data.fillna(0, inplace=True)
    # 绘图
    dic = {'sku_name_list_sort':sku_name_list_sort,'data':data}
    return dic

def draw_line_day_sku_list(dic):
    '''
    每日订单数
    :param dic:
    :return:
    '''
    sku_name_list_sort = dic['sku_name_list_sort']
    df = dic['data']
    data = []
    for i in sku_name_list_sort[:8]:
        line = go.Scatter(
            x=df.index,
            y=df[u'%s' % i],
            mode='lines+markers',
            name=i,
            line=dict(
                shape='spline'
            )
        )
        data.append(line)

    layout = dict(title = '每日订单数',
                  xaxis = dict(title = '日期'),
                  yaxis = dict(title = '个数'),
                  )
    fig = dict(data=data, layout=layout)

    filename = os.getcwd() + u'/templates/index_chart_html/每日订单数'
    py.plot(fig, filename=filename)



def dict_bar_sku_count():
    # 解析数据
    with open(os.getcwd()+'/media/data/data.pkl', 'rb') as f:
        data = f.read()
        data_dict = pickle.loads(data)
        sku_useful_info_dict = data_dict['sku_useful_info_dict']
        sku_name_list_sort = data_dict['sku_name_list_sort']

    sku_list = []
    for sku_name, v in sku_useful_info_dict.items():
        data = v['quantity-purchased']
        # DataFrame存入字典后取出变成series，故需要转回DataFrame，顺便设置列名
        data.name = sku_name
        data = data.to_frame(name=sku_name)
        sku_list.append(data)
        # 合并数据
    data = pd.concat(sku_list, axis=1)
    data = data.T.sum(axis = 1)
    # _ = data.fillna(0, inplace=True)
    # 绘图
    dic = {'sku_name_list_sort':sku_name_list_sort,'data':data}
    return dic

def draw_bar_sku_count(dic):
    sku_name_list_sort = dic['sku_name_list_sort']
    Sr = dic['data']

    df = Sr.to_frame(name='count')
    df =  df.loc[sku_name_list_sort[:5]]


    # 设置color颜色集合
    color_list = ['rgba(#c9302c)','rgba(#449d44)','rgba(#31b0d5)','rgba(#ec971f)','rgba(#31b0d5)','rgba(#fdff5c)','rgba(#ec91ff)','rgba(#b9fff2)','rgba(#dcb2f2)','rgba(#8c8dda)']
    print color_list[:5]
    data = [go.Bar(
        x = df.index,
        y = df['count'],
        marker = dict(
            color = ['rgba(222,45,38,0.8)','rgba(0,255,127,0.8)','rgba(222,45,38,0.8)','rgba(#ec971f)','rgba(#31b0d5)']
        )
    )]


    layout = dict(title = 'SKU系列前五订单数',
                  xaxis = dict(title = '系列名'),
                  yaxis = dict(title = '个数'),
                  )
    fig = dict(data=data, layout=layout)

    filename = os.getcwd() + u'/templates/index_chart_html/SKU系列前五订单数'
    py.plot(fig,filename = filename)




if __name__ == '__main__':
    pass
    # df = test()
    # draw_day_order_refund(df)
    # print df_day_sku_list()