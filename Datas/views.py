# -*- coding: utf-8 -*-

import os
from django.shortcuts import render,HttpResponse,redirect
from Pyfun import DataFun
import pickle
import json
from django.views.decorators.csrf import csrf_exempt

def DataIndexView(request):
    return render(request, 'index.html')

@csrf_exempt
def DataInputView(request):
    if request.method == 'POST':
        res = {}
        fl =request.FILES.get('file')
        path = os.getcwd()
        # print(f.name)
        # print(f.size)
        # print(f.read())
        if not fl :
            return HttpResponse(json.dumps({"err": -1, "msg": "请选择文件"}), content_type='application/json')
        elif fl.name[-3:] != 'csv':
            res['err'] = 0
            res['err_info'] = '请传入正确的格式'
            print('错误格式')
            return HttpResponse(json.dumps({"err": -1, "msg": "传入文件格式错误"}),content_type='application/json')

        try:
            with open(path + r'/static/datas/' + fl.name,'wb') as f:
                for i in fl.chunks():
                    f.write(i)
            filepath = path + r'/static/datas/' + fl.name
            df = DataFun.get_csv(filepath)
            sku_name_list = DataFun.get_sku_name_list(df, reverse=True)
            order_sku_info_dict = DataFun.get_sku_info_dict(df, 'Order', sku_name_list)  # 获得订单的总数据
            refund_sku_info_dict = DataFun.get_sku_info_dict(df, 'Refund', sku_name_list)  # 获得退款的总数据
            with open(path + r'/static/datas/order.pkl','wb') as f:
                data = pickle.dumps(order_sku_info_dict)
                f.write(data)
            with open(path + r'/static/datas/refund.pkl','wb') as f:
                data = pickle.dumps(refund_sku_info_dict)
                f.write(data)
            return HttpResponse(json.dumps({"err": 0, "msg": "数据解析完毕"}),content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps({"err": -1, "msg": "数据解析错误"}),content_type='application/json')