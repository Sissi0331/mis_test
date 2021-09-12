# -*- coding = utf-8 -*-
# @Time : 2021/9/10 20:00
# @Author:SissiH
# @File : employee.py
# @Software : PyCharm


# 员工子系统
from django.shortcuts import render, redirect
from django.db import connection
from misTest.view.pageholder import pageBuilder


def employee(request):
    return render(request, 'employee.html')


def indexEmployee(request):  # 查询员工个人信息
    print("查询员工自己的信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'employee':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select employeeinfo.Employee_id,employeeinfo.Employee_name,employeeinfo.Employee_Age,managerinfo.Manager_name,employeeinfo.Manager_id\
                        from employeeinfo\
                        inner join managerinfo on employeeinfo.Manager_id = managerinfo.Manager_id\
                        where employeeinfo.Employee_id=%s;", [request.session['id']])  # 根据具体员工id查询员工数据“
        tmp = ('Employee_id', 'Employee_name', 'Employee_Age', 'Manager_name', 'Manager_id')  # 返回的字段名
        result_list = []
        result = cursor.fetchone()
        result_list.append(dict(zip(tmp, result)))
        return render(request, 'employee1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def indexECredit(request):  # 查询员工绩效
    print("查询学生选课信息")
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'employee':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select taskinfo.Task_id,taskcredit.Credit,taskinfo.Manager_id\
                        from taskinfo\
                        inner join  taskcredit on taskcredit.Task_id = taskinfo.Task_id\
                        where taskcredit.Employee_id=%s;", [request.session['id']])  # 根据具体员工id查询任务绩效信息
        tmp = ('Task_id', 'Credit', 'Manager_id')  # 返回的字段名
        result_list = []
        result = cursor.fetchone()
        while result:
            result_list.append(dict(zip(tmp, result)))
            result = cursor.fetchone()
        # html网页做表格结构动态变化并且将cmd输出的内容更新到界面上进行对应显示
        return render(request, 'employee2.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

# def indexSGPA(request):  # 查询选修成绩信息
#     print("查询学生自己的成绩")
#     page = request.GET.get('page', 1)
#     if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
#         connection.connect()
#         cursor = connection.cursor()
#         cursor.execute("select t.course_id,course_name,grade\
#                         from take as t,course as c\
#                         where student_id=%s and t.course_id=c.course_id \
#                         order by t.course_id;", [request.session['id']])  # 根据具体学生id查询课程成绩列表
#         result_list = []
#         result = cursor.fetchone()
#         tmp = ('course_id', 'course_name', 'grade')
#         while result:
#             result_list.append(dict(zip(tmp, result)))
#             result = cursor.fetchone()
#         return render(request, 'student3.html', pageBuilder(result_list, page))
#     else:
#         print("用户身份不合法")
#         return redirect('/pro/illegalUser/')
