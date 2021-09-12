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


def indexAllM(request):  # 查询所有教师信息
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


def changeAllEm(request):  # 录入、删除、修改学生信息
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

        elif operation == 'delete':  # 删除
            error_count = 0
            if len(student) == 0:
                print("此学生ID不存在")
                messages.error(request, "此学生ID不存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('delete from student where student_id = "%s"' % (student_id))

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
        teacher_id = request.POST.get('teacher_id')
        cursor.execute("select * from teacher where teacher_id = '%s' " % (teacher_id))
        teacher = cursor.fetchall()

        if operation == 'add':  # 录入
            password = request.POST.get('password')
            teacher_name = request.POST.get('teacher_name')
            dept = request.POST.get('dept')

            error_count = 0
            if len(teacher) != 0:
                print("此教师ID已经存在")
                messages.error(request, "此教师ID已经存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('insert into teacher values \
                            ("%s", md5("%s"), "%s", "%s")' % (teacher_id, password, teacher_name, dept))

        elif operation == 'update':  # 修改
            password = request.POST.get('password')
            teacher_name = request.POST.get('teacher_name')
            dept = request.POST.get('dept')

            error_count = 0
            if len(teacher) == 0:
                print("此教师ID不存在")
                messages.error(request, "此教师ID不存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('update teacher set password = md5("%s"), teacher_name = "%s", dept = "%s" \
                            where teacher_id = "%s"' % (password, teacher_name, dept, teacher_id))

        elif operation == 'delete':  # 删除
            error_count = 0
            if len(teacher) == 0:
                print("此教师ID不存在")
                messages.error(request, "此教师ID不存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('delete from teacher where teacher_id = "%s"' % (teacher_id))

        cursor.execute("select * from teacher order by teacher_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"teacher_id": r[0], "password": r[1], 'teacher_name': r[2], 'dept': r[3]})
        return render(request, 'admin3.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def ifdigit(num):
    if num.replace(".", '').isdigit():
        if num.count(".") == 0:
            return True
        elif num.count(".") == 1:
            return True
    else:
        return False


def changeAllT(request):  # 录入、删除、修改课程信息
    page = request.GET.get('page', 1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        course_id = request.POST.get('course_id')

        cursor.execute("select * from course where course_id = '%s' " % (course_id))
        course = cursor.fetchall()

        if operation == 'add':  # 录入
            course_name = request.POST.get('course_name')
            credit = request.POST.get('credits')
            error_count = 0
            if len(course) != 0:
                print("此课程ID已经存在")
                messages.error(request, "此课程ID已经存在")
                error_count += 1
            elif (ifdigit(credit) == False) or ((ifdigit(credit) == True) and (float(credit) < 0)):
                print("您输入的学分不是大于0的数字！")
                messages.error(request, "您输入的学分不是大于0的数字！")
                error_count += 1
            elif error_count == 0:
                credit = float(credit)
                cursor.execute('insert into course values \
                            ("%s", "%s", "%f")' % (course_id, course_name, credit))

        elif operation == 'update':  # 修改
            course_name = request.POST.get('course_name')
            credit = request.POST.get('credits')
            cursor.execute(
                "select * from course where course_id = '%s' and course_name = '%s' " % (course_id, course_name))
            class_course = cursor.fetchall()

            error_count = 0
            if len(course) == 0:
                print("此课程ID不存在")
                messages.error(request, "此课程ID不存在")
                error_count += 1
            elif len(class_course) == 0 and error_count == 0:
                print("此课程ID与课程名不对应")
                messages.error(request, "此课程ID与课程名不对应")
                error_count += 1
            elif (ifdigit(credit) == False) or ((ifdigit(credit) == True) and (float(credit) < 0)):
                print(float(credit))
                print("您输入的学分不是大于0的数字！")
                messages.error(request, "您输入的学分不是大于0的数字！")
                error_count += 1
            elif error_count == 0:
                credit = float(credit)
                cursor.execute('update course set course_name = "%s", credits = "%f" where \
                            course_id = "%s"' % (course_name, credit, course_id))

        elif operation == 'delete':  # 删除
            error_count = 0
            if len(course) == 0:
                print("此课程ID不存在")
                messages.error(request, "此课程ID不存在")
                error_count += 1
            elif error_count == 0:
                cursor.execute('delete from course where course_id = "%s"' % (course_id))

        cursor.execute("select * from course order by course_id;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"course_id": r[0], 'course_name': r[1], 'credits': r[2]})
        return render(request, 'admin4.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

