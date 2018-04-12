# -*- coding: utf-8 -*-
import pickle

with open('data.pkl','rb') as f:
    data = f.read()
    d = pickle.loads(data)

for i in d['sku_useful_info_dict']:
    print i