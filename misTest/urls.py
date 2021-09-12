# -*- coding = utf-8 -*-
# @Time : 2021/9/10 22:07
# @Author:SissiH
# @File : urls.py
# @Software : PyCharm
from django.urls import path
from misTest.view import enroll, stat, employee,manager

urlpatterns = [
    path('welcome/', enroll.welcome),
    path('login/', enroll.login),
    path('logout/', enroll.logout),
    path('indexEmployee', employee.indexEmployee),
    path('indexECredit', employee.indexECredit),
    path('indexSGPADIST', stat.indexSGPADIST),
    path('employee/', employee.employee),
    path('manager/', manager.manager),
    path('indexMTask/', manager.indexMTask),
    path('indexManager', manager.indexManager)
]
