# -*- coding: utf-8 -*-

import os
import time
from django.shortcuts import render,HttpResponse,redirect
from Pyfun import DataFun
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
        res = {}
        fl =request.FILES.get('file')
        path = os.getcwd()
        # print(f.name)
        # print(f.size)
        # print(f.read())
        try:
            if not fl :
                time.sleep(1)
                return HttpResponse(json.dumps({"err": -1, "msg": "请选择文件"}), content_type='application/json')
            elif fl.name[-3:] != 'csv':
                res['err'] = 0
                res['err_info'] = '请传入正确的格式'
                time.sleep(1)
                return HttpResponse(json.dumps({"err": -1, "msg": "请传入csv格式的文件"}),content_type='application/json')
        except:
            time.sleep(1)
            return HttpResponse(json.dumps({"err": -1, "msg": "请选择正确的文件"}), content_type='application/json')
        try:
            with open(path + r'/static/datas/' + fl.name,'wb') as f:
                for i in fl.chunks():
                    f.write(i)
            filepath = path + r'/static/datas/' + fl.name
            df = DataFun.get_csv(filepath)
            sku_name_list = DataFun.get_sku_name_list(df, reverse=True)
            order_sku_info_dict = DataFun.get_sku_info_dict(df, 'Order', sku_name_list)  # 获得订单的总数据
            refund_sku_info_dict = DataFun.get_sku_info_dict(df, 'Refund', sku_name_list)  # 获得退款的总数据

            datas_dic = {'sku_list':sku_name_list,'order_datas':order_sku_info_dict,'refund_datas':refund_sku_info_dict,'df':df}
            with open(path + r'/static/datas/datas.pkl','wb') as f:
                data = pickle.dumps(datas_dic)
                f.write(data)
            return HttpResponse(json.dumps({"err": 0, "msg": "数据解析完毕"}),content_type='application/json')
        except:
            time.sleep(1)
            return HttpResponse(json.dumps({"err": -1, "msg": "数据解析错误"}),content_type='application/json')


@csrf_exempt
def DataAutoDrawView(request):
    path = os.getcwd()
    with open(path + r'/static/datas/datas.pkl', 'rb') as f:
        data = f.read()
        datas = pickle.loads(data)
        sku_name_list = datas['sku_list']
        order_sku_info_dict = datas['order_datas']
        refund_sku_info_dict = datas['refund_datas']
        df = datas['df']

    DataFun.get_diagram_day_sku_list(order_sku_info_dict, sku_name_list[:6])  # 每日系列订单数
    # get_average_price_quantity_purchased(order_sku_info_dict, sku_name_list[0])  # 每日订单均价和订单量
    DataFun.get_average_price_quantity_purchased(order_sku_info_dict, sku_name_list[0], subplots=False)  # 每日订单均价和订单量
    # get_profit_day(order_sku_info_dict, sku_name_list[0])  # 每日订单均价和订单利润
    DataFun.get_profit_day(order_sku_info_dict, sku_name_list[0], subplots=True)  # 每日订单均价和订单利润
    # 获得退/订金额关系图
    DataFun.get_order_refund(order_sku_info_dict[sku_name_list[0]], refund_sku_info_dict[sku_name_list[0]], sku_name_list[0])
    DataFun.get_sku_bar(df, 10, reverse=True)

    # 获得存储图片文件夹下的文件名称
    path_datas = path + r'/static/imgs/datas/'
    img_name_list = []
    for root, dirs, files in os.walk(path_datas):
        for i in files:
            img_name_list.append(i.decode('GB2312').encode('utf-8'))


    return HttpResponse(json.dumps({"err": 0, "msg": "OK","img_name_list":img_name_list}), content_type='application/json')


@csrf_exempt
def SkuNameListUpdateView(request):
    path = os.getcwd()
    try:
        with open(path + r'/static/datas/datas.pkl', 'rb') as f:
            data = f.read()
            datas = pickle.loads(data)
            sku_name_list = datas['sku_list']
        return HttpResponse(json.dumps({"err": 0, "msg": sku_name_list}), content_type='application/json')
    except:
        time.sleep(1)
        return HttpResponse(json.dumps({"err": -1, "msg": '数据包不存在'}),content_type='application/json')


@csrf_exempt
def ImgsNameListView(request):
    path = os.getcwd()
    # 获得存储图片文件夹下的文件名称
    path_datas = path + r'/static/imgs/datas/'
    img_name_list = []
    for root, dirs, files in os.walk(path_datas):
        for i in files:
            img_name_list.append(i.decode('GB2312').encode('utf-8'))
    return HttpResponse(json.dumps({"err": 0, "msg": "OK", "img_name_list": img_name_list}),
                        content_type='application/json')