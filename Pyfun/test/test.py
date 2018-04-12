# -*- coding: utf-8 -*-
import os
import pandas as pd
import pickle
import plotly
import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import Pyfun.PyDataFun
trace1 = {
    'x': [1, 2, 3, 4],
    'y': [10, 15, 13, 17],
    'type': 'scatter'
}

trace2 = {
    'x': [1, 2, 3, 4],
    'y': [16, 5, 11, 9],
    'type': 'scatter'
}

data = [trace1, trace2]

py.plot(data)