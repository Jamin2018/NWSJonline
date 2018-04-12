# -*- coding: utf-8 -*-

import os
import time
from django.shortcuts import render,HttpResponse,redirect
from Pyfun import DataFun
from Pyfun import PyDataFun
import pickle
import json
from django.views.decorators.csrf import csrf_exempt

def DataIndexView(request):
    return render(request, 'index.html')

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
            product_cost_weight_path = os.getcwd() + r'/static/datas/product_cost_weight-sample.xlsx'
            filepath = path + r'/static/datas/' + file_csv.name
            with open(path + r'/static/datas/' + file_csv.name,'wb') as f:
                for i in file_csv.chunks():
                    f.write(i)
            with open(path + r'/static/datas/' + file_xlsx.name,'wb') as f:
                for i in file_xlsx.chunks():
                    f.write(i)
            df_csv = PyDataFun.get_df(filepath,usecols =[6,7, 17, 21, 22, 24, 26])
            sku_name_list = PyDataFun.get_sku_name_list(df_csv)  # 获得列表名
            sku_info_dict = PyDataFun.get_sku_info_dict(df_csv, sku_name_list)  # 根据列名获取相关字典信息
            sku_name_list_sort = PyDataFun.get_orderly_sku_list(sku_info_dict, transaction_type='Order', reverse=True, product_cost_weight_path = product_cost_weight_path)
            sku_useful_info_dict = PyDataFun.get_sku_useful_info_dict(sku_name_list_sort[:5], sku_info_dict, product_cost_weight_path = product_cost_weight_path) # 获得处理后，有用，字典信息
            datas_dict = {'sku_useful_info_dict':sku_useful_info_dict,'sku_info_dict':sku_info_dict,'sku_name_list_sort':sku_name_list_sort,}
            with open(path + r'/static/datas/datas.pkl','wb') as f:
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
    path = os.getcwd()
    product_cost_weight_path = os.getcwd() + r'/static/datas/product_cost_weight-sample.xlsx'
    with open(path + r'/static/datas/datas.pkl', 'rb') as f:
        data = f.read()
        datas = pickle.loads(data)
    sku_useful_info_dict = datas['sku_useful_info_dict']
    PyDataFun.draw_day_sku_list(sku_useful_info_dict)
    PyDataFun.draw_day_profits_list(sku_useful_info_dict)
    # 获得存储图片文件夹下的文件名称
    path_datas = path + r'/static/imgs/datas/'
    img_name_list = []
    for root, dirs, files in os.walk(path_datas):
        for i in files:
            img_name_list.append(i.decode('GB2312').encode('utf-8'))
    return HttpResponse(json.dumps({"err": 0, "msg": "OK","img_name_list":img_name_list}), content_type='application/json')


@csrf_exempt
def SkuNameListUpdateView(request):
    '''
    系列名列表显示
    :param request:
    :return:
    '''
    path = os.getcwd()
    try:
        with open(path + r'/static/datas/datas.pkl', 'rb') as f:
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
    path_datas = path + r'/static/imgs/datas/'
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
    product_cost_weight_path = os.getcwd() + r'/static/datas/product_cost_weight-sample.xlsx'
    with open(path + r'/static/datas/datas.pkl', 'rb') as f:
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
            PyDataFun.draw_day_profit_price(sku_name, sku_info_dict, product_cost_weight_path = product_cost_weight_path)
            PyDataFun.draw_day_order_refund(sku_name, sku_info_dict, product_cost_weight_path = product_cost_weight_path)
            sus_sku_name.append(sku_name)
        except:
            err_sku_name.append(sku_name)

    return HttpResponse(json.dumps({"err": 0, "msg": 'OK','err_sku_name':err_sku_name,'sus_sku_name':sus_sku_name}), content_type='application/json')

def SkuChartView(request):
    '''
    SKU系列页面
    :param request:
    :return:
    '''
    chart_path = os.getcwd() + r'/static/imgs/chart/'
    chart_name_list = []
    for root, dirs, files in os.walk(chart_path):
        for i in files:
            chart_name_list.append(i.decode('GB2312').encode('utf-8'))
    return render(request, 'chart.html',{'chart_name_list':chart_name_list,})