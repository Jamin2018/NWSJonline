# -*- coding: utf-8 -*-
import plotly.offline as off

import pandas as pd
import numpy as np

from sqlalchemy import create_engine

# 连接数据库
engine = create_engine("mysql://root:q8850063@localhost:3306/test?charset=utf8", pool_pre_ping=True)

off.init_notebook_mode(connected=False)
#
# df = pd.read_csv('0211-0225bak.csv',usecols=[1, 2, 6, 7, 17, 21, 22, 24, 26,32])
# df.to_sql('csvtest',con=engine, schema='test', if_exists='append', index=False,chunksize=10000)

sql = "select * from csvtest"


df = pd.read_sql(sql,engine,)


aa=pd.DataFrame(df)


print aa.columns