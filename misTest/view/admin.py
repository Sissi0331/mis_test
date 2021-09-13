# -*- coding = utf-8 -*-
# @Time : 2021/9/12 21:01
# @Author:Dcclandbest
# @File : admin.py
# @Software : PyCharm

# 管理员子系统
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from misTest.view.pageholder import pageBuilder
from django.contrib import messages


def admin(request):  # 个人信息
    return render(request, 'admin.html')


def indexAdmin(request):  # 查询管理员个人信息
    print("查询管理员个人信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        admin_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select * from admininfo where Admin_id='%s'" % (admin_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"admin_id": r[0], 'admin_name': r[1]})
        for i in range(0, len(result_list)):
            print("管理员ID:%s 姓名:%s" % (result_list[i]['admin_id'], result_list[i]['admin_name']))
        return render(request, 'admin1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def indexAllEm(request):  # 查询所有员工信息
    print("查询所有员工信息")
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        admin_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select e.Employee_id,e.Employee_name,e.password,e.Employee_Age,e.Manager_id\
                        from employeeinfo as e\
                        order by Employee_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Employee_id": r[0], 'Employee_name': r[1], 'password': r[2], \
                                'Employee_Age': r[3], 'Manager_id': r[4]})
        return render(request, 'admin2.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def indexAllM(request):  # 查询所有经理信息
    print("查询所有教师信息")
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select * from managerinfo order by Manager_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Manager_id": r[0], "Manager_name": r[1], 'password': r[2], 'Manager_Age': r[3]})
        return render(request, 'admin3.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def indexAllT(request):  # 查询所有项目信息
    print("查询所有项目信息")
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select * from taskinfo order by Task_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Task_id": r[0], 'Manager_id': r[1], 'Start_time': r[2],'End_time':r[3]})
        return render(request, 'admin4.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def changeAllEm(request):  # 录入、修改员工信息
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        admin_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        e_id = request.POST.get('employee_id')

        cursor.execute("select * from employeeinfo where Employee_id = '%s' " % (e_id))
        e = cursor.fetchall()

        if operation == 'add':  # 录入
            password = request.POST.get('password')
            e_name = request.POST.get('name')
            m_id = request.POST.get('manager')
            e_age = request.POST.get('age')

            cursor.execute("select * from employeeinfo where Manager_id = '%s' " % (m_id))
            m = cursor.fetchall()

            error_count = 0
            if len(e) != 0:
                print("此员工ID已经存在")
                messages.error(request, "此员工ID已经存在")
                error_count += 1
            elif len(m) == 0:
                print("此经理不存在")
                messages.error(request, "该经理不存在")
                error_count += 1
            elif error_count == 0:
                print(e_age)
                if(e_age !=''):
                    cursor.execute('insert into employeeinfo values \
                                ("%s", "%s", "%s","%s","%d")' % (e_id, e_name, password, m_id,int(e_age)))
                else:
                    cursor.execute('insert into employeeinfo values \
                                                    ("%s", "%s", "%s","%s",null)' % (e_id, e_name, password, m_id))

        elif operation == 'update':  # 修改
            password = request.POST.get('password')
            e_name = request.POST.get('name')
            m_id = request.POST.get('manager')
            e_age = request.POST.get('age')

            cursor.execute("select * from employeeinfo where Manager_id = '%s' " % (m_id))
            Class = cursor.fetchall()
            cursor.execute("select * from employeeinfo where Employee_id = '%s' and Manager_id = '%s'" % (e_id, m_id))
            stu_class = cursor.fetchall()

            error_count = 0
            if len(e) == 0:
                print("此员工ID不存在")
                messages.error(request, "此员工ID不存在")
                error_count += 1
            elif len(Class) == 0:
                print("该经理不存在")
                messages.error(request, "该经理不存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('update employeeinfo set \
                password = "%s", Employee_name = "%s", Manager_id = "%s",Employee_Age="%d"\
                where Employee_id = "%s"' % (password, e_name, m_id, int(e_age),e_id))

        cursor.execute("select e.Employee_id,e.Employee_name,e.password,e.Employee_Age,e.Manager_id\
                        from employeeinfo as e\
                        order by Employee_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Employee_id": r[0], 'Employee_name':r[1],'password': r[2], \
                                'Manager_id': r[3], \
                                'Employee_Age': r[4]})
        return render(request, 'admin2.html', pageBuilder(result_list, page))

    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def changeAllM(request):  # 录入、删除、修改教师信息
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        m_id = request.POST.get('m_id')
        cursor.execute("select * from managerinfo where Manager_id = '%s' " % (m_id))
        manager = cursor.fetchall()

        if operation == 'add':  # 录入
            password = request.POST.get('password')
            m_name = request.POST.get('name')
            m_age = request.POST.get('age')

            error_count = 0
            if len(manager) != 0:
                print("此经理ID已经存在")
                messages.error(request, "此经理ID已经存在")
                error_count += 1
            elif error_count == 0:
                if (m_age != ''):
                    cursor.execute('insert into managerinfo values \
                                                ("%s", "%s", "%s","%d")' % (
                    m_id, m_name, password, int(m_age)))
                else:
                    cursor.execute('insert into managerinfo values \
                                                ("%s", "%s", "%s",null)' % (
                    m_id, m_name, password))

        elif operation == 'update':  # 修改
            password = request.POST.get('password')
            m_name = request.POST.get('name')
            m_age = request.POST.get('age')

            error_count = 0
            if len(manager) == 0:
                print("此经理ID不存在")
                messages.error(request, "此经理ID不存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('update managerinfo set password = "%s", Manager_name = "%s", Manager_Age = "%d" \
                            where Manager_id = "%s"' % (password, m_name,  int(m_age),m_id))

        cursor.execute("select * from managerinfo order by Manager_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Manager_id": r[0], 'Manager_name': r[1],"password": r[2], 'Manager_Age': r[3]})
        return render(request, 'admin3.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def isdate(str_date):
    import time
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str_date, "%Y-%m-%d")
        return True
    except Exception:
        # traceback.print_exc()
        raise Exception("时间参数错误 near : {}".format(str_date))
        return False


def ifdigit(num):
    if num.replace(".", '').isdigit():
        if num.count(".") == 0:
            return True
        elif num.count(".") == 1:
            return True
    else:
        return False


def changeAllT(request):  # 录入、修改项目信息
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        t_id = request.POST.get('t_id')

        cursor.execute("select * from taskinfo where Task_id = '%s' " % (t_id))
        task = cursor.fetchall()
        import datetime

        if operation == 'add':  # 录入
            m_id = request.POST.get('m_id')
            start=request.POST.get('start')
            end=request.POST.get('end')
            error_count = 0
            if len(task) != 0:
                print("此项目ID已经存在")
                messages.error(request, "此项目ID已经存在")
                error_count += 1
            elif(isdate(start)==False) or (isdate(end)==False):
                messages.error(request, "您输入的不是日期")
                error_count += 1
            elif error_count == 0:
                cursor.execute('insert into taskinfo values \
                            ("%s", "%s", "%s","%s")' % (t_id, m_id, start,end))

        elif operation == 'update':  # 修改
            m_id = request.POST.get('m_id')
            start = request.POST.get('start')
            end = request.POST.get('end')
            cursor.execute(
                "select Manager_id from taskinfo where Manager_id = '%s' " % (m_id))
            m = cursor.fetchall()

            error_count = 0
            if len(task) == 0:
                print("此项目ID不存在")
                messages.error(request, "此项目ID不存在")
                error_count += 1
            elif (len(m) == 0):
                messages.error(request, "此经理不存在")
                error_count += 1
            elif (isdate(start) == False) or (isdate(end) == False):
                messages.error(request, "您输入的不是日期")
                error_count += 1
            elif error_count == 0:
                cursor.execute('update taskinfo set Start_time = "%s", End_time = "%s" where \
                            Task_id = "%s" and Manager_id="%s"' % (start, end, t_id,m_id))


        cursor.execute("select * from taskinfo order by Task_id")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Task_id": r[0], 'Manager_id': r[1], 'Start_time': r[2],'End_time':r[3]})
        return render(request, 'admin4.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

