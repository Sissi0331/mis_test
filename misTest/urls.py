# -*- coding = utf-8 -*-
# @Time : 2021/9/10 22:07
# @Author:SissiH
# @File : urls.py
# @Software : PyCharm
from django.urls import path
from misTest.view import enroll, stat, employee,manager,admin

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
    path('indexMCredit/', manager.indexMCredit),
    path('changeCredit', manager.changeCredit),
    path('indexManager/', manager.indexManager),
    path('indexMDistSelect', stat.indexMDistSelect),
    path('indexMDistShow', stat.indexMDistShow),
    path('admin/', admin.admin),
    path('indexAdmin', admin.indexAdmin),
    path('indexAllEm', admin.indexAllEm),
    path('indexAllM', admin.indexAllM),
    path('indexAllT', admin.indexAllT),
    path('changeAllEm', admin.changeAllEm),
    path('changeAllM', admin.changeAllM)
]
