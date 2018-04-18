# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    '''
    用户信息表，基础了基础用户表
    '''
    # username = models.CharField(max_length=150,verbose_name=u'姓名',unique=True)
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=7, choices=(('male', u'男'),('female', u'女')))
    address = models.CharField(max_length=100, default=u'')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default = u'image/default.jpg', max_length = 100)
    # USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username