# -*- coding: utf-8 -*-

import os
import time
from django.shortcuts import render,HttpResponse,redirect
from Pyfun.test import DataFun
from Pyfun import PyDataFun
from Pyfun import PyPlotly
import pickle
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

def DataIndexView(request):
    chart_path = os.getcwd() + r'/templates/index_chart_html/'
    chart_name_list = []
    for root, dirs, files in os.walk(chart_path):
        for i in files:
            chart_name_list.append(i.decode('GB2312').encode('utf-8'))
    return render(request, 'index.html',{'chart_name_list':chart_name_list,})


@csrf_exempt
def DataInputView(request):
    '''
    接收csv文件，解析文件后数据用pickle持续化储存
    :param request:
    :return:
    '''
    if request.method == 'POST':
        file_csv =request.FILES.get('file_csv')
        file_xlsx =request.FILES.get('file_xlsx')
        try:
            if not file_csv or not file_xlsx :
                if not file_csv:
                    time.sleep(1)
                    return HttpResponse(json.dumps({"err": -1, "msg": "请选择csv文件"}), content_type='application/json')
                elif not file_xlsx:
                    time.sleep(1)
                    return HttpResponse(json.dumps({"err": -1, "msg": "请选择xlsx文件"}), content_type='application/json')
            elif file_csv.name[-3:] != 'csv' or file_xlsx.name[-4:] != 'xlsx':
                if file_csv.name[-3:] != 'csv':
                    time.sleep(1)
                    return HttpResponse(json.dumps({"err": -1, "msg": "请传入正确的csv数据"}),content_type='application/json')
                elif file_xlsx.name[-4:] != 'xlsx':
                    time.sleep(1)
                    return HttpResponse(json.dumps({"err": -1, "msg": "请传入正确的运费数据"}),content_type='application/json')
        except:
            time.sleep(1)
            return HttpResponse(json.dumps({"err": -1, "msg": "请选择正确的文件"}), content_type='application/json')


        try:
            path = os.getcwd()
            product_cost_weight_path = os.getcwd() + r'/media/data/product_cost_weight-sample.xlsx'
            filepath = path + r'/media/data/' + file_csv.name
            with open(path + r'/media/data/' + file_csv.name,'wb') as f:
                for i in file_csv.chunks():
                    f.write(i)
            with open(path + r'/media/data/' + file_xlsx.name,'wb') as f:
                for i in file_xlsx.chunks():
                    f.write(i)
            df_csv = PyDataFun.get_df(filepath,usecols =[6,7, 17, 21, 22, 24, 26])
            sku_name_list = PyDataFun.get_sku_name_list(df_csv)  # 获得列表名
            sku_info_dict = PyDataFun.get_sku_info_dict(df_csv, sku_name_list)  # 根据列名获取相关字典信息
            sku_name_list_sort = PyDataFun.get_orderly_sku_list(sku_info_dict, transaction_type='Order', reverse=True, product_cost_weight_path = product_cost_weight_path)
            sku_useful_info_dict = PyDataFun.get_sku_useful_info_dict(sku_name_list_sort, sku_info_dict, product_cost_weight_path = product_cost_weight_path) # 获得处理后，有用，字典信息
            datas_dict = {'sku_useful_info_dict':sku_useful_info_dict,'sku_info_dict':sku_info_dict,'sku_name_list_sort':sku_name_list_sort,}
            with open(path + r'/media/data/data.pkl','wb') as f:
                data = pickle.dumps(datas_dict)
                f.write(data)
            return HttpResponse(json.dumps({"err": 0, "msg": "数据解析完毕"}),content_type='application/json')
        except Exception as e:
            print (e)
            time.sleep(1)
            return HttpResponse(json.dumps({"err": -1, "msg": "数据解析错误"}),content_type='application/json')


@csrf_exempt
def DataAutoDrawView(request):
    '''
    一键构图
    :param request:
    :return:
    '''
    line_dict= PyPlotly.dict_line_day_sku_list()
    PyPlotly.draw_line_day_sku_list(line_dict)
    bar_dict = PyPlotly.dict_bar_sku_count()
    PyPlotly.draw_bar_sku_count(bar_dict)
    pie_dict = PyPlotly.dict_pie_count_profits()
    PyPlotly.draw_pie_count_profits(pie_dict)
    return HttpResponse(json.dumps({"err": 0, "msg": "OK"}), content_type='application/json')


@csrf_exempt
def SkuNameListUpdateView(request):
    '''
    系列名列表显示
    :param request:
    :return:
    '''
    path = os.getcwd()
    try:
        with open(path + r'/media/data/data.pkl', 'rb') as f:
            data = f.read()
            datas = pickle.loads(data)
            sku_name_list = datas['sku_name_list_sort']
        return HttpResponse(json.dumps({"err": 0, "msg": sku_name_list}), content_type='application/json')
    except:
        time.sleep(1)
        return HttpResponse(json.dumps({"err": -1, "msg": '数据包不存在'}),content_type='application/json')


@csrf_exempt
def ImgsNameListView(request):
    '''
    刷新主页面的数据图表
    :param request:
    :return:
    '''
    path = os.getcwd()
    # 获得存储图片文件夹下的文件名称
    path_datas = path + r'/static/img/data/'
    img_name_list = []
    for root, dirs, files in os.walk(path_datas):
        for i in files:
            img_name_list.append(i.decode('GB2312').encode('utf-8'))
    return HttpResponse(json.dumps({"err": 0, "msg": "OK", "img_name_list": img_name_list}),
                        content_type='application/json')

@csrf_exempt
def ChooseSkuDrawView(request):
    '''
    选择系列构图
    :param request:
    :return:
    '''
    path = os.getcwd()
    product_cost_weight_path = os.getcwd() + r'/media/data/product_cost_weight-sample.xlsx'
    with open(path + r'/media/data/data.pkl', 'rb') as f:
        data = f.read()
        datas = pickle.loads(data)
    sku_info_dict = datas['sku_info_dict']

    sku_name_str = request.GET.get('sku_name_list')
    sku_name_str = sku_name_str.replace("，".decode('utf-8'),',')
    sku_name_list = sku_name_str.split("," or "，")
    sku_name_list = list(set(sku_name for sku_name in sku_name_list))

    err_sku_name = []
    sus_sku_name = []

    for sku_name in sku_name_list:
        try:
            sku_info = sku_info_dict[sku_name]
            sku_useful_info = PyDataFun.get_sku_useful_info(sku_name, sku_info, transaction_type='Order',
                                                  product_cost_weight_path=product_cost_weight_path)  # 获得订单单个有用信息，根据需求,处理后的sku信息
            refund_sku_useful_info = PyDataFun.get_sku_useful_info(sku_name, sku_info, transaction_type='Refund',
                                                         product_cost_weight_path=product_cost_weight_path)  # 获得退款单个有用信息，根据需求,处理后的sku信息

            order_price_day = sku_useful_info['price-amount']
            refund_price_day = refund_sku_useful_info['price-amount']
            order_profit_day, refund_profit_day = order_price_day.to_frame(name=u'订单金额'), refund_price_day.to_frame(
                name=u'退款金额')
            df_price_spread = pd.concat([order_profit_day, refund_profit_day], axis=1)
            _ = df_price_spread.fillna(0, inplace=True)
            df_price_spread[u'实际订单金额'] = df_price_spread.sum(axis=1)
            df_price_spread[u'退款金额'] = -df_price_spread[u'退款金额']
            PyPlotly.draw_day_order_refund(df_price_spread,sku_name)
            sus_sku_name.append(sku_name)
        except Exception as e:
            print e
            err_sku_name.append(sku_name)

    return HttpResponse(json.dumps({"err": 0, "msg": 'OK','err_sku_name':err_sku_name,'sus_sku_name':sus_sku_name}), content_type='application/json')

def SkuChartView(request):
    '''
    SKU系列页面
    :param request:
    :return:
    '''
    chart_path = os.getcwd() + r'/templates/line_chart_html/'
    chart_name_list = []
    for root, dirs, files in os.walk(chart_path):
        for i in files:
            chart_name_list.append(i.decode('GB2312').encode('utf-8'))
    print chart_name_list
    return render(request, 'chart.html',{'chart_name_list':chart_name_list,})




def SkuChartTableView(request):
    '''
    SKU系列图和数据表页面
    :param request:
    :return:
    '''
    chart_path = os.getcwd() + r'/static/img/chart_table/'
    chart_name_list = []
    for root, dirs, files in os.walk(chart_path):
        for i in files:
            chart_name_list.append(i.decode('GB2312').encode('utf-8'))

    return render(request, 'chart_table.html',{'chart_name_list':chart_name_list,})



#  ---------------websocket长连接测试---------------------
from dwebsocket import require_websocket
def socket_test(request):
    return render(request,'socket_test.html')

@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send('你好')
    time.sleep(5)
    request.websocket.send('5秒后，你好')
    time.sleep(5)
    request.websocket.send('10秒后，你好')


from dwebsocket.decorators import accept_websocket,require_websocket
def socket_test2(request):
    return render(request,'socket_test2.html')

@accept_websocket
def echo(request):
    if not request.is_websocket():#判断是不是websocket连接
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'index.html')
    else:
        n = 1
        for message in request.websocket:
            request.websocket.send('第%s次' % n)#发送消息到客户端
            n +=1
#  ---------------websocket长连接测试---------------------