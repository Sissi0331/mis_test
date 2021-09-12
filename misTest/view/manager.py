#经理子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from misTest.view.pageholder import pageBuilder

def manager(request):#个人信息
    return render(request, 'templates/manager.html')

def indexManager(request):#查询经理个人信息
    print("查询经理自己的信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'manager':
        manager_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select * from managerinfo where Manager_id='%s'" % manager_id)
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Manager_id":r[0],'Manager_name':r[2],'Manager_Age':r[3]})
        return render(request, 'templates/manager1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexMTask(request):#查询发布项目信息
    print("查询经理发布的项目")
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'manager':
        Manager_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select taskinfo.Task_id,taskinfo.Start_time,taskinfo.End_time \
                        from taskinfo \
                        where Manager_id='%s' \
                        order by Start_time;" % Manager_id)
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Manager_id":r[0],'Start_time':r[1],'End_time':r[2]})
        return render(request, 'manager2.html', pageBuilder(result_list,page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexMCredit(request):#查询所管辖项目员工绩效信息
    print("查询员工绩效信息")
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'manager':
        Manager_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        # cursor.execute("select tc.Task_id,tc.Employee_id,tc.Credit,tc.Start_time,tc.End_time,tc.End_time \
        #                 from taskcredit As tc left join taskinfo\
        #                 on taskinfo.Manager_id ='%s' \
        #                 order by tc.Task_id, tc.Employee_id;" % (Manager_id))
        cursor.execute("select taskinfo.Task_id,taskcredit.Employee_id,taskcredit.Credit,taskcredit.Start_time,taskcredit.End_time \
                                from taskinfo\
                                inner join taskcredit on taskcredit.Task_id = taskinfo.Task_id\
                                where taskinfo.Manager_id ='%s';" % (Manager_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Task_id":r[0],'Employee_id':r[1],'Credit':r[2],\
                                'Start_time':r[3],'End_time':r[4]})
        return render(request, 'templates/manager3.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def ifdigit(num):
    return True
    # if num.replace(".",'').isdigit():
    #     if num.count(".")==0:
    #         return True
    #     elif num.count(".")==1:
    #         return True
    # else:
    #     return False


def changeCredit(request):#录入、删除、修改发布项目员工绩效信息
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'manager':
        Manager_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        Employee_id = request.POST.get('Employee_id')
        Task_id = request.POST.get('Task_id')

        cursor.execute("select * from taskcredit where Employee_id = '%s' " % Employee_id)
        employee = cursor.fetchall()
        cursor.execute("select * from taskcredit where Task_id = '%s' " % (Task_id))
        task = cursor.fetchall()

        if operation == 'update': #修改
            credit = request.POST.get('Credit')
            cursor.execute("select Task_id,Employee_id,Credit from taskcredit \
                            where Task_id = '%s' and Employee_id = '%s'" % (Task_id, Employee_id))
            credits = cursor.fetchall()
            error_count = 0
            if len(employee) == 0:
                print("该员工不存在")
                messages.error(request,"该员工不存在")
                error_count += 1
            elif len(task) == 0:
                print("该项目不存在")
                messages.error(request,"该项目不存在")
                error_count += 1
            elif len(credits) ==0 and (error_count == 0):
                print("该员工没有参与此项目")
                messages.error(request,"该员工没有参与此项目")
                error_count += 1
            elif (ifdigit(credit) == False) or ((ifdigit(credit) == True) and ((float(credit) < 0) or (float(credit) > 100))):
                print(credit)
                print("请输入0到5之间的数字")
                messages.error(request,"请输入0到5之间的数字")
                error_count += 1
            elif error_count == 0:
                credit = float(credit)
                cursor.execute('update taskcredit set \
                                Credit = "%d" where (Employee_id = "%s") \
                                and (Task_id = "%s")' % (credit, Employee_id, Task_id))

        # cursor.execute("select take.student_id,student_name,take.course_id,course_name,credits,grade \
        #                 from student natural join course natural join take natural join teach \
        #                 where teacher_id ='%s' \
        #                 order by take.student_id, take.course_id;" % (manager_id))
        # result = cursor.fetchall()
        # connection.close()
        # result_list = []
        # for r in result:
        #     result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2],\
        #                         'course_name':r[3],'credits':r[4],'grade':r[5]})
        # return render(request, 'templates/manager3.html', pageBuilder(result_list, page))
        cursor.execute("select taskinfo.Task_id,taskcredit.Employee_id,taskcredit.Credit,taskcredit.Start_time,taskcredit.End_time \
                                from taskinfo\
                                inner join taskcredit on taskcredit.Task_id = taskinfo.Task_id\
                                where taskinfo.Manager_id ='%s';" % (Manager_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Task_id": r[0], 'Employee_id': r[1], 'Credit': r[2], \
                            'Start_time': r[3], 'End_time': r[4]})
        return render(request, 'templates/manager3.html', pageBuilder(result_list, page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')