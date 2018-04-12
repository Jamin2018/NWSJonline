# -*- coding: utf-8 -*-
import os
import random
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # 导入绘图库
import pickle


def get_df(filename, usecols = None):
    '''
    获得有用的df的数据列
    '''
    if filename[-3:] == 'csv' :
        df = pd.read_csv(filename, usecols = usecols)
    elif filename[-4:] == 'xlsx':
        df = pd.read_excel(filename, usecols=usecols)
    return (df)

def get_sku_name_list(df):
    '''
    获得sku名字列表
    '''
    df = df['sku'].dropna()
    r = r'(.*?)-'
    sku_name_set = set()
    for i in df.values:
        a = re.match(r, i).group(1)
        sku_name_set.add(a)
    return sku_name_set

def get_orderly_sku_list(sku_info_dict, transaction_type = 'Order', reverse=True , product_cost_weight_path = None):
    '''
    获得有序列表名
    '''
    sku_count_dict = {}
    for sku_name,sku_info in sku_info_dict.items():
        sku_useful_info = get_sku_useful_info(sku_name, sku_info, transaction_type = transaction_type,product_cost_weight_path= product_cost_weight_path)  # 获得订单单个有用信息，根据需求,处理后的sku信息
        sku_count = sku_useful_info['quantity-purchased'].sum(axis=0)
        sku_count_dict[sku_name]=sku_count

    sku_name_dict_sort = sorted(sku_count_dict.items(), key=lambda x: x[1], reverse=reverse)
    lit = []
    for sku_name in sku_name_dict_sort:
        lit.append(sku_name[0])
    return lit


def get_sku_info_dict(df,sku_name_list):
    '''
     获得所有每个系列的sku的信息字典集合
    '''
    dic = {}
    for i in sku_name_list:
        r = r'(%s)-' % i
        # print(df_csv['sku'].index)
        data = df[df['sku'].str.contains(r, na=True)]  # 分别筛选各个系列的详细数据
        dic[i] = data
    return dic


def get_sku_info(sku_name,sku_info_dict):
    '''
    通过当个sku名获得该sku信息集合
    '''
    sku_info = sku_info_dict[sku_name]
    return sku_info


def get_sku_useful_info(sku_name,sku_info,exchange_rate = 0.1589,transaction_type ='Order', product_cost_weight_path= None):
    '''
    获得单个有用shu数据，根据需求,处理后的sku信息
    '''
    product_cost_weight = get_df(product_cost_weight_path)
    df_product_cost_weight = product_cost_weight[product_cost_weight['style'] == sku_name]
    sku_useful_info = sku_info[sku_info['transaction-type'] == transaction_type ]
    # 处理时间数据，生成新的CSV数据表
    sku_useful_info['posted-date'] = pd.Series(pd.to_datetime(sku_useful_info['posted-date'])).dt.date
    sku_useful_info = sku_useful_info.groupby('posted-date').sum()
    price = df_product_cost_weight.iat[0,1]
    weight = df_product_cost_weight.iat[0,2]
    sku_useful_info['product_cost_weight'] = sku_useful_info['quantity-purchased'].apply(lambda x : -x * price * weight * exchange_rate)
    return (sku_useful_info)


def get_sku_useful_info_dict(sku_name_list,sku_info_dict,product_cost_weight_path= None):
    '''
    传入一个想查询的列表名，获得该列表的信息字典
    '''
    sku_dict = {}
    for sku_name in sku_name_list:
        sku_info = get_sku_info(sku_name, sku_info_dict)  # 获得单个sku信息
        sku_useful_info = get_sku_useful_info(sku_name, sku_info,product_cost_weight_path = product_cost_weight_path)  # 获得单个有用信息，根据需求,处理后的sku信息
        sku_dict[sku_name] = sku_useful_info
    return sku_dict


def draw_day_sku_list(sku_useful_info_dict):
    '''
    传入想查询的信息字典，经过处理，获得关系图
    '''
    sku_list = []
    for sku_name, v in sku_useful_info_dict.items():
        data = v['quantity-purchased']
        # DataFrame存入字典后取出变成series，故需要转回DataFrame，顺便设置列名
        data.name = sku_name
        data  = data.to_frame(name=sku_name)
        sku_list.append(data)
    # 合并数据
    data = pd.concat(sku_list, axis=1)
    _ = data.fillna(0, inplace=True)
    # 绘图

    path = os.getcwd()
    filepath = path + r'/static/imgs/datas/'
    drawing(data,title=u'每日订单数',to_imgpath = filepath)
    return (data)


def draw_day_profits_list(sku_useful_info_dict):
    '''
    获得每日利润图
    '''
    sku_list = []
    for sku_name, v in sku_useful_info_dict.items():
        # 价格合并到一起
        amount= v[[ 'price-amount', 'item-related-fee-amount','product_cost_weight']].apply(lambda x: x.sum(), axis=1)
        #     # DataFrame存入字典后取出变成series，故需要转回DataFrame，顺便设置列名
        amount.name = sku_name
        data = amount.to_frame(name=sku_name)
        sku_list.append(data)
    # 合并数据
    data = pd.concat(sku_list, axis=1)
    _ = data.fillna(0, inplace=True)
    # 绘图
    path = os.getcwd()
    filepath = path + r'/static/imgs/datas/'
    drawing(data, title=u'每日利润',to_imgpath=filepath)
    return (data)


def draw_day_profit_price(sku_name,sku_info_dict,subplots=True, product_cost_weight_path = None):
    '''
    获得单系列每日平均售价和每日利润的关系图
    '''
    sku_info = get_sku_info(sku_name,sku_info_dict)   # 获得单个sku信息
    sku_useful_info = get_sku_useful_info(sku_name,sku_info, product_cost_weight_path = product_cost_weight_path)     # 获得单个有用信息，根据需求,处理后的sku信息
    # 获得每日利润数据
    profit_day = sku_useful_info[[ 'price-amount', 'item-related-fee-amount','product_cost_weight']].apply(lambda x: x.sum(), axis=1)
    # 获得每日均价数据
    average_price = sku_useful_info['price-amount'] / sku_useful_info['quantity-purchased']
    # Series --> DataFrame
    average_price,profit_day = average_price.to_frame(name=u'每日均价'),profit_day.to_frame(name=u'每日利润')
    data = pd.concat([average_price,profit_day], axis=1)

    path = os.getcwd()
    filepath = path + r'/static/imgs/chart/'
    drawing(data, to_imgpath = filepath, title=u'%s系列每日均价-利润对比图' % sku_name, subplots=subplots,ylabel = u'美元', fontsize=14, rot = 30)


def draw_day_order_refund(sku_name,sku_info_dict,product_cost_weight_path = None):
    sku_info = get_sku_info(sku_name, sku_info_dict)  # 获得单个sku信息
    sku_useful_info = get_sku_useful_info(sku_name, sku_info, transaction_type='Order', product_cost_weight_path = product_cost_weight_path)  # 获得订单单个有用信息，根据需求,处理后的sku信息
    refund_sku_useful_info = get_sku_useful_info(sku_name, sku_info, transaction_type='Refund', product_cost_weight_path = product_cost_weight_path)  # 获得退款单个有用信息，根据需求,处理后的sku信息
    order_price_day = sku_useful_info['price-amount']
    refund_price_day = refund_sku_useful_info['price-amount']
    order_profit_day, refund_profit_day = order_price_day.to_frame(name=u'订单金额'), refund_price_day.to_frame(name=u'退款金额')
    df_price_spread = pd.concat([order_profit_day, refund_profit_day],axis=1)
    _ = df_price_spread.fillna(0, inplace=True)
    df_price_spread[u'实际订单金额'] = df_price_spread.sum(axis=1)
    df_price_spread[u'退款金额'] = -df_price_spread[u'退款金额']

    path = os.getcwd()
    filepath = path + r'/static/imgs/chart/'
    drawing(df_price_spread, to_imgpath = filepath, title=u'%s订单-退款关系图' % sku_name, fontsize=14, rot = 30)


def drawing(df, to_imgpath = None, kind = 'line', title=u'数据分析', color = None, figsize = (10,10), linewidth = 1.5, alpha = 0.8,
            subplots=False, ylabel = u'', grid = True, fontsize = 15, legend=True , rot = 0):
    '''
    将数据在图上绘制（title命名不要加“/”等特殊字符）
    :param csv:
    :return:
    '''
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    # matplotlib.rc('font', **{'family': 'SimHei'})
    # 自定义颜色
    # if type(csv) == list:
    #     plt.plot(csv[u'YSW5402系列'], 'g-', csv[u'YSW1623系列'], 'r-')
    df.plot(kind = kind , subplots=subplots,color = color,linewidth = linewidth , linestyle = '-' , title = title, alpha = alpha,rot=rot,
            figsize = figsize,fontsize = fontsize,grid=grid,legend=legend,)

    # 自动化最佳比例
    if kind != 'bar':
        plt.autoscale(tight=True)
    plt.xlabel(u'2018/2/12 - 2018/2/26')
    plt.ylabel(ylabel)
    # 设置y轴范围
    # plt.ylim(0,150)
    plt.savefig(to_imgpath+'%s.jpg' % title)
    plt.show()


def draw_bar(df, to_imgpath = None,section = 5, kind = 'line', title=u'数据分析', color = None, figsize = (10,10), linewidth = 1.5,
             alpha = 0.8, subplots=False, ylabel = u'', grid = True, legend=True, rot = 0):
    '''
    将数据在图上绘制（title命名不要加“/”等特殊字符）
    :param csv:
    :return:
    '''
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False

    # matplotlib.rc('font', **{'family': 'SimHei'})
    # 自定义颜色
    # if type(csv) == list:
    #     plt.plot(csv[u'YSW5402系列'], 'g-', csv[u'YSW1623系列'], 'r-')
    df.plot(kind = kind , subplots=subplots,linewidth = linewidth , linestyle = '-' , title = title, alpha = alpha,rot=rot,
            figsize = figsize,fontsize = 7,grid=grid,legend=legend)
    # 标注坐标
    x = [x for x in range(section)]
    y = [int(y[0]) for y in df.values]

    # 添加柱状图值
    for x,y in zip(x,y):
        plt.text(x,y,y,color="black",ha='center',va='bottom')

    plt.xlabel(u'2018/2/12 - 2018/2/26')
    plt.ylabel(ylabel)
    plt.savefig(to_imgpath+'%s.jpg' % title)
    plt.show()

if __name__ == '__main__':
    file = '0211-0225bak.csv'
    df_csv = get_df(file,usecols =[6,7, 17, 21, 22, 24, 26])  # 获得有用数据
    sku_name_list = get_sku_name_list(df_csv)  # 获得列表名
    sku_info_dict = get_sku_info_dict(df_csv,sku_name_list) # 根据列名获取相关字典信息
    sku_name_list_sort = get_orderly_sku_list(sku_info_dict, transaction_type = 'Order',reverse=True)

    sku_name = sku_name_list_sort[0]
    sku_info = get_sku_info(sku_name,sku_info_dict)   # 获得单个sku信息
    sku_useful_info = get_sku_useful_info(sku_name,sku_info,transaction_type = 'Order')     # 获得订单单个有用信息，根据需求,处理后的sku信息
    refund_sku_useful_info = get_sku_useful_info(sku_name,sku_info,transaction_type = 'Refund')     # 获得退款单个有用信息，根据需求,处理后的sku信息
    print(sku_useful_info.head(5))
    sku_useful_info_dict = get_sku_useful_info_dict(sku_name_list_sort[:5], sku_info_dict)  # 获得选择的sku字典信息
    draw_day_sku_list(sku_useful_info_dict)
    draw_day_profits_list(sku_useful_info_dict)
    draw_day_profit_price(sku_name,sku_info_dict)
    draw_day_order_refund(sku_name,sku_info_dict)