# -*- coding: utf-8 -*-
from django.db import models

class AccountOrderData(models.Model):
    settlement_start_date = models.DateTimeField(verbose_name='数据开始日期', auto_now_add=False)
    settlement_end_date = models.DateTimeField(verbose_name='数据结束日期', auto_now_add=False)
    transaction_type = models.CharField(verbose_name='事务类型', max_length=12)
    order_id = models.CharField(verbose_name='订单ID', max_length=64)
    posted_date = models.DateTimeField(verbose_name='发布时间', auto_now_add=False)
    sku = models.CharField(verbose_name='sku', max_length=64)
    quantity_purchased = models.IntegerField(default=0, verbose_name='订单数')
    price_amount = models.IntegerField(default=0, verbose_name='订单总价')
    item_related_fee_amount = models.IntegerField(default=0, verbose_name='项目相关的费用金额')
    promotion_amount = models.IntegerField(default=0, verbose_name='促销金额')

    account_choices = [
        (1,'admin')
    ]
    account = models.IntegerField(choices=account_choices,default=1)