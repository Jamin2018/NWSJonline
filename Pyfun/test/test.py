# -*- coding: utf-8 -*-

import pandas as pd

x = pd.read_excel('biaotou.xlsx')
print x
print '==' * 100
print x[u'物流方式']
print x['Unnamed: 10']
print x['Unnamed: 11']