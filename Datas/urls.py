"""NWSJonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from Datas.views import DataIndexView, DataInputView, DataAutoDrawView, SkuNameListUpdateView, ImgsNameListView
from Datas.views import ChooseSkuDrawView, SkuChartView, SkuChartTableView
from Datas.views import echo_once,socket_test,socket_test2,echo


urlpatterns = [
    url(r'^$', DataIndexView, name='index'),
    url(r'^data-input/$', DataInputView, name='data-input'),
    url(r'^data-auto-draw/$', DataAutoDrawView, name='data-auto-draw'),
    url(r'^sku-list-update/$', SkuNameListUpdateView, name='sku-list-update'),
    url(r'^img-name-list/$', ImgsNameListView, name='img-name-list'),
    url(r'^choose-sku-draw/$', ChooseSkuDrawView, name='choose-sku-draw'),
    url(r'^sku-chart/$', SkuChartView, name='sku-chart'),
    url(r'^sku-chart_table/$', SkuChartTableView, name='sku-chart-table'),
    url(r'^echo_once/$', echo_once, name='echo_once'),
    url(r'^echo$', echo, name='echo'),
    url(r'^socket_test/$', socket_test, name='socket_test'),
    url(r'^socket_test2/$', socket_test2, name='socket_test2'),
]
