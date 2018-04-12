# -*- coding: utf-8 -*-
import os
import random
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # 导入绘图库


def get_csv(filepath):
    '''
    读取目标文件
    :param filename:目标文件
    :return:
    '''
    df = pd.read_csv(filepath)
    return df


def add_weight_freight_df(df):
    '''
    添加重量和运费
    :param df:
    :return:
    '''
    df['weight'] = round(random.uniform(0.6, 1), 2)
    df['freight'] = -10.36
    return df
    # 生成随机重量的


def get_sku_quantity_purchased_all(df, transaction_type = 'Order'):
    '''
    获得单系列的总计字典
    :param df:
    :param transaction_type:订单类型
    :param ascending: ascending = True升序, ascending = False降序
    :return:
    '''
    df = get_transaction_type_info(df, transaction_type)
    df = df[['sku','quantity-purchased']].groupby('sku').sum()
    # df = df.sort_values('quantity-purchased',ascending=ascending)

    # df_sku_name = df['sku'].dropna().drop_duplicates()
    # re正则匹配系列名,获得系列名的列表
    r = r'(.*?)-'
    sku_name_set = set()
    for i in df.index:
        a = re.match(r, i).group(1)
        sku_name_set.add(a)
    sku_name_list = list(sku_name_set)

    sku_quantity_purchased_all_dict = {}
    for sku_name in sku_name_list:
        # 模糊匹配
        r = r'%s' % sku_name
        data = df[df.index.str.contains(r, na=True)]  # 分别筛选各个系列的详细数据
        sku_quantity_purchased_all_dict[sku_name] = data.sum()[0]

    return sku_quantity_purchased_all_dict


def get_sku_name_list(df,transaction_type = 'Order',reverse=True):
    '''
    获得系列名订单量排名的列表
    :param df:
    :param transaction_type:
    :param reverse:
    :return:
    '''
    sku_quantity_purchased_all_dict = get_sku_quantity_purchased_all(df, transaction_type)
    # 根据'quantity-purchased'总数排序
    sku_name_dict_sort = sorted(sku_quantity_purchased_all_dict.items(), key=lambda x: x[1], reverse=reverse)
    lit = []
    for sku_name in sku_name_dict_sort:
        lit.append(sku_name[0])
    return lit


def get_transaction_type_info(df, transaction_type):
    '''
    获得想要的Order,Refund等订单信息
    :param df:
    :param transaction_type:
    :return:
    '''
    df = df[df['transaction-type'] == transaction_type]
    return df


######   这是一开始写的函数，发现很多代码重复，一开始思路就不正确，应该先总体清洗出有用的数据返回，再进行处理 #####@
# def get_day_order(csv):
#     '''
#     清洗日期格式，并累加同一天的销售数量
#     :param csv:
#     :return:
#     '''
#     csv_order = csv[csv['transaction-type'] == 'Order']
#     csv_day_order = csv_order[['posted-date', 'quantity-purchased']]
#     # 处理缺失值
#     csv_day_order = csv_day_order.dropna()
#
#     # 处理时间数据，生成新的CSV数据表
#     # T = pd.DataFrame([i[:10] for i in csv_day_order['posted-date']], index= csv_day_order.index)
#     # 第二种更快的，处理时间数据，生成新的CSV数据表
#     t = pd.Series(pd.to_datetime(csv_day_order['posted-date'],))
#     # 第一种
#     # csv_day_order['posted-date'] = T
#     # 第二种
#     csv_day_order['posted-date'] = t.dt.date
#
#     csv_day_order.rename(columns={'quantity-purchased': u'订单量', 'posted-date': u'时间'}, inplace=True)
#     # 将同一天的销售量累加
#     csv_day_order = csv_day_order.groupby(u'时间').sum()
#
#     drawing(csv_day_order,title=u'每日订单量',color='red')
#     return csv_day_order


# def get_day_sku(csv,sku_name):
#     '''
#     获得单独的sku系列每日订单量数据
#     :param csv:
#     :param sku_name:
#     :return:
#     '''
#     csv_sku = csv[csv['transaction-type'] == 'Order']
#     csv_day_sku = csv_sku[['posted-date', 'sku','quantity-purchased']]
#     # 处理缺失值
#     csv_day_sku = csv_day_sku.dropna()
#     # 处理时间数据，生成新的CSV数据表
#     t = pd.Series(pd.to_datetime(csv_day_sku['posted-date'], ))
#     csv_day_sku['posted-date'] = t.dt.date
#     # 使用模糊分别匹配sku
#     r = r'%s' % sku_name
#     data = csv_day_sku['sku']
#     data = data[data.str.contains(r,na = True)]
#     csv_day_sku['nid'] = data
#     csv_day_sku = csv_day_sku.dropna()
#
#     # 修改列名字
#     csv_day_sku.rename(columns={'quantity-purchased':sku_name,'posted-date':u'时间'}, inplace=True)
#     # 求和
#     csv_day_sku = csv_day_sku[[u'时间',sku_name]].groupby(u'时间').sum()
#     # 调用绘图函数
#     drawing(csv_day_sku,title=u'%s系列每日订单量'%sku_name)
#     return (csv_day_sku)
#
# def get_day_sku_all(csv,sku_name_list):
#     '''
#     传入总CSV，整合sku系列订单量
#     :param csv: 总数据
#     :param sku_name_list:sku系列名，列表
#     :return:
#     '''
#     csv_sku = csv[csv['transaction-type'] == 'Order']
#     csv_sku_all = csv_sku[['posted-date', 'sku','quantity-purchased']]
#     # 去重
#     # csv_day_sku = csv_day_sku.drop_duplicates()
#     # 处理缺失值
#     csv_sku_all = csv_sku_all.dropna()
#     # 处理时间数据，生成新的CSV数据表
#     t = pd.Series(pd.to_datetime(csv_sku_all['posted-date'], ))
#     csv_sku_all['posted-date'] = t.dt.date
#
#     sku_list = []
#     for sku_name in sku_name_list:
#         csv_day_sku = csv_sku_all
#         # 使用模糊分别匹配sku
#         r = r'%s' % sku_name
#         data = csv_day_sku['sku']
#         data = data[data.str.contains(r,na = True)]
#         csv_day_sku['nid'] = data
#         csv_day_sku = csv_day_sku.dropna()
#         # 修改列名字
#         csv_day_sku.rename(columns={'quantity-purchased':sku_name,'posted-date':u'时间'}, inplace=True)
#         # 求和
#         csv_day_sku = csv_day_sku[[u'时间',sku_name]].groupby(u'时间').sum()
#         sku_list.append(csv_day_sku)
#
#     # 合并数据
#     res = pd.concat(sku_list, axis=1)
#     drawing(res,title=u'每日销售走势图')
#     return (res)


def get_sku_info_dict(df,transaction_type,sku_name_list,):
    '''
    获得sku信息字典
    :param df:
    :param sku_name:
    :return:
    '''
    df_order_info = get_transaction_type_info(df, transaction_type)
    sku_info_all = df_order_info[['posted-date', 'quantity-purchased', 'price-amount', 'item-related-fee-amount', 'sku']]
    # 将缺失值填充
    _ = sku_info_all.fillna(0, inplace=True)

    sku_info_dict = {}

    for sku_name in sku_name_list:
        sku_info = sku_info_all
        # 模糊匹配
        r = r'%s' % sku_name
        data = sku_info['sku']
        data = data[data.str.contains(r, na=True)]
        # 标记要找的数据
        sku_info['nid'] = data
        # 将没筛选到的数据排除
        sku_info = sku_info.dropna()
        # r = r'%s' % sku_name
        # sku_info = sku_info[sku_info['sku'].str.contains(r, na=True)]
        # 价格合并到一起
        amount= sku_info[[ 'price-amount', 'item-related-fee-amount']].apply(lambda x: x.sum(), axis=1)
        sku_info['sum'] = amount
        # 处理时间数据，生成新的CSV数据表
        t = pd.Series(pd.to_datetime(sku_info['posted-date']))
        sku_info['posted-date'] = t.dt.date
        # 根据最新时间数据，得到其他费用总和
        sku_info = sku_info.groupby('posted-date').sum()
        sku_info = add_weight_freight_df(sku_info)
        sku_info_dict['%s'% sku_name] = sku_info
        # print(sku_info.head(4))
    return sku_info_dict


def get_diagram_day_sku_list(sku_info_dict,sku_name_list):
    '''
    传入一个想查询的列表名，获得关系图
    :param sku_info_dict:
    :param sku_name_list:
    :return:
    '''
    sku_list = []
    for sku_name in sku_name_list:
        data = sku_info_dict['%s' % sku_name]['quantity-purchased']
        # DataFrame存入字典后取出变成series，故需要转回DataFrame，顺便设置列名

        data.name = sku_name
        # data  = data.to_frame(name=sku_name)
        data  = data.to_frame(name=sku_name)
        sku_list.append(data)
    # 合并数据
    data = pd.concat(sku_list, axis=1)
    _ = data.fillna(0, inplace=True)
    # 绘图
    drawing(data,title=u'每日订单数量走势图')
    return (data)


def get_sku_info(sku_info_dict,sku_name):
    '''
    根据名字获取sku中想要的系列
    :param sku_info_dict:
    :param sku_name:
    :return:
    '''
    sku_info  = sku_info_dict['%s' % sku_name]
    return sku_info


def get_average_price_quantity_purchased(sku_info_dict,sku_name,subplots=True):
    '''
    每日平均销售价格和每日订单量关系图
    :param sku_info_dict:
    :param sku_name:
    :return:
    '''
    sku_info = get_sku_info(sku_info_dict,sku_name)
    day_number = sku_info['quantity-purchased']
    average_price = sku_info['price-amount'] / sku_info['quantity-purchased']
    # Series --> DataFrame
    average_price,day_number = average_price.to_frame(name=u'每日平均价'),day_number.to_frame(name=u'每日订单量')
    data = pd.concat([average_price,day_number], axis=1)
    drawing(data, title=u'%s系列每日均价-订单量对比图' % sku_name,subplots=subplots, ylabel=u'订单量(个)')


def get_profit_day(sku_info_dict,sku_name,subplots=True):
    '''
    获得每日平均售价和每日利润的关系图
    :param sku_info_dict:
    :param sku_name:
    :return:
    '''
    sku_info = get_sku_info(sku_info_dict,sku_name)
    # 获得每日利润数据
    profit_day = sku_info['price-amount'] - sku_info['weight'] * sku_info['freight'] *  sku_info['quantity-purchased']
    # 获得每日均价数据
    average_price = sku_info['price-amount'] / sku_info['quantity-purchased']
    # Series --> DataFrame
    average_price,profit_day = average_price.to_frame(name=u'每日均价'),profit_day.to_frame(name=u'每日利润')
    data = pd.concat([average_price,profit_day], axis=1)
    drawing(data, title=u'%s系列每日均价-利润对比图' % sku_name, subplots=subplots,ylabel = u'美元')


def get_order_refund(df_order,df_refund,sku_name):
    '''
    获得退/订金额关系图
    :param df_order:
    :param df_refund:
    :return:
    '''
    df_order = df_order['sum']
    df_refund = df_refund['sum']
    # Series --> DataFrame
    df_order,df_refund = df_order.to_frame(name=u'订单金额'),df_refund.to_frame(name=u'退款金额')
    df_price_spread = pd.concat([df_order,df_refund],axis=1)
    _ = df_price_spread.fillna(0, inplace=True)
    df_price_spread[u'实际订单金额'] = df_price_spread.sum(axis=1)
    df_price_spread[u'退款金额'] = -df_price_spread[u'退款金额']
    drawing(df_price_spread,title=u'%s订单-退款关系图' % sku_name)


def get_sku_bar(df,section = 5, transaction_type = 'Order',reverse= True):
    sku_quantity_purchased_all_dict = get_sku_quantity_purchased_all(df, transaction_type)
    sku_name_dict_sort = sorted(sku_quantity_purchased_all_dict.items(), key=lambda x:x[1] , reverse=reverse)[:section]
    n = [n[0] for n in sku_name_dict_sort]
    i = [i[1] for i in sku_name_dict_sort]
    sr = pd.DataFrame(i,index=n)
    draw_bar(sr,section,title = u'SKU系列区间订单情况',color ='red',kind='bar',grid=False,legend = False)
    # seaborn_draw(sr)


def drawing(df, kind = 'line', title=u'数据分析', color = None, figsize = (6,6), linewidth = 1.5, alpha = 0.8,
            subplots=False, ylabel = u'', grid = True, legend=True):
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
    df.plot(kind = kind , subplots=subplots,color = color,linewidth = linewidth , linestyle = '-' , title = title, alpha = alpha,rot=0,
             figsize = figsize,fontsize = 7,grid=grid,legend=legend,)

    # 自动化最佳比例
    if kind != 'bar':
        plt.autoscale(tight=True)
    plt.xlabel(u'2018/2/12 - 2018/2/26')
    plt.ylabel(ylabel)
    # 设置y轴范围
    # plt.ylim(0,150)
    # if type(df) == list:
    #     plt.savefig('%s.jpg' % title)
    # elif type(df) == type(pd.DataFrame()):
    #     plt.savefig('%s.jpg' % title)

    path = os.getcwd()
    filepath = path + r'/static/img/data/'
    plt.savefig(filepath+'%s.jpg' % title)
    plt.show()


def draw_bar(df, section = 5, kind = 'line', title=u'数据分析', color = None, figsize = (6,6), linewidth = 1.5,
             alpha = 0.8, subplots=False, ylabel = u'', grid = True, legend=True):
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
    df.plot(kind = kind , subplots=subplots,linewidth = linewidth , linestyle = '-' , title = title, alpha = alpha,rot=0,
             figsize = figsize,fontsize = 7,grid=grid,legend=legend)
    # 标注坐标
    x = [x for x in range(section)]
    y = [int(y[0]) for y in df.values]

    # 添加柱状图值
    for x,y in zip(x,y):
        plt.text(x,y,y,color="black",ha='center',va='bottom')


    plt.xlabel(u'2018/2/12 - 2018/2/26')
    plt.ylabel(ylabel)
    # if type(df) == list:
    #     plt.savefig('%s.jpg' % title)
    # elif type(df) == type(pd.DataFrame()):
    #     plt.savefig('%s.jpg' % title)
    path = os.getcwd()
    filepath = path + r'/static/img/data/'
    plt.savefig(filepath+'%s.jpg' % title)
    plt.show()


def seaborn_draw(df):
    '''
    使用seaborn绘图
    :param df:
    :return:
    '''
    # white, dark, whitegrid, darkgrid, ticks
    sns.set_style('whitegrid')
    # paper, notebook, talk, poster
    sns.set_context('talk')
    sns.set_palette(sns.color_palette('RdBu', n_colors=7))
    sns.countplot(x=0, data=df)
    plt.show()


if __name__ == '__main__':
    path = os.getcwd()
    filename = '0211-0225bak.csv'
    filepath = 'C:\Users\Administrator\PycharmProjects\NWSJonline/static/data/0211-0225bak.csv'
    df = get_csv(filepath)
    sku_name_list = get_sku_name_list(df, reverse=True)
    # csv_day_order = get_day_order(csv)
    order_sku_info_dict = get_sku_info_dict(df, 'Order', sku_name_list)  # 获得订单的总数据
    refund_sku_info_dict = get_sku_info_dict(df, 'Refund', sku_name_list)  # 获得退款的总数据
    get_diagram_day_sku_list(order_sku_info_dict, sku_name_list[:6])  # 每日系列订单数
    get_average_price_quantity_purchased(order_sku_info_dict, sku_name_list[0])  # 每日订单均价和订单量
    get_average_price_quantity_purchased(order_sku_info_dict, sku_name_list[0], subplots=False)  # 每日订单均价和订单量
    get_profit_day(order_sku_info_dict, sku_name_list[0])   # 每日订单均价和订单利润
    get_profit_day(order_sku_info_dict, sku_name_list[0], subplots=False)   # 每日订单均价和订单利润
    # 获得退/订金额关系图
    get_order_refund(order_sku_info_dict[sku_name_list[0]], refund_sku_info_dict[sku_name_list[0]], sku_name_list[0])
    get_sku_bar(df, 10, reverse=True)
