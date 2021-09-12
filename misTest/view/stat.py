# 统计子系统
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import matplotlib

matplotlib.use('Agg')  # 使用matplotlib的非交互式后端Agg，以解决Tcl_AsyncDelete问题
import matplotlib.pyplot as plt
import os
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 能显示中文标签


# 某个员工所有绩效的统计函数：0 1 2 3 4 5
def indexSGPADIST(request):
    print("查询绩效分布")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'employee':
        employeeId = request.session['id']
        # 首先先将之前该员工对应的统计图片删掉
        picreg = "^[^_]*_" + employeeId + "\.jpg$"
        for pic in os.listdir("static/employee_stat_img/"):
            if re.match(picreg, pic) is not None:
                os.remove("static/employee_stat_img/" + pic)
        connection.connect()
        cursor = connection.cursor()
        # 获取员工名字
        cursor.execute("select employeeinfo.Employee_name\
                        from employeeinfo\
                        where Employee_id=%s;", [request.session['id']])
        result = cursor.fetchone()
        employee_name = result[0]
        # 查询员工绩效分布
        cursor.execute("select Credit,count(Credit) as counts\
                        from taskcredit\
                        where taskcredit.Employee_id=%s\
                        group by Credit;", [employeeId])  # 根据具体学生id查询成绩分布
        result_list = []
        result = cursor.fetchone()
        tmp = ('credit', 'counts')
        while result:
            result_list.append(dict(zip(tmp, result)))
            result = cursor.fetchone()
        for i in range(0, len(result_list)):
            print("取得成绩:%d 对应次数:%d" % (result_list[i]['credit'], result_list[i]['counts']))
        num_list = [0, 0, 0, 0, 0, 0]
        label_list = ["0", "1", "2", "3", "4", "5"]
        color_list = ["royalblue", "darkcyan", "yellowgreen", "yellow", "orangered", "red"]
        for i in range(len(result_list)):
            grade = result_list[i]['credit']
            if grade == 0:
                num_list[0] += result_list[i]['counts']
            elif grade == 1:
                num_list[1] += result_list[i]['counts']
            elif grade == 2:
                num_list[2] += result_list[i]['counts']
            elif grade == 3:
                num_list[3] += result_list[i]['counts']
            elif grade == 4:
                num_list[4] += result_list[i]['counts']
            else:
                num_list[5] += result_list[i]['counts']
        # 柱状图
        plt.title('直方图')
        plt.xlabel('分数段')
        plt.ylabel('计数')
        if max(num_list) <= 5:
            plt.yticks(list(range(max(num_list) + 1)))
        plt.bar(range(len(num_list)), num_list, color=color_list, tick_label=label_list)
        plt.savefig("static/employee_stat_img/bar_" + employeeId + ".jpg")  # 图片拿学生id作为标识
        plt.close()
        # 饼图
        # 获得个数非0的成绩段（以及相应的label_list和color_list）
        pie_num_list, pie_label_list, pie_color_list = [], [], []
        for i in range(len(num_list)):
            if num_list[i] > 0:
                pie_num_list.append(num_list[i])
                pie_label_list.append(label_list[i])
                pie_color_list.append(color_list[i])
        plt.title('饼状图')
        plt.pie(pie_num_list, labels=pie_label_list, colors=pie_color_list, autopct='%1.2f%%',
                textprops={'fontsize': 12, 'color': 'black'})
        plt.axis('equal')
        plt.savefig("static/employee_stat_img/pie_" + employeeId + ".jpg")  # 图片拿学生id作为标识
        plt.close()
        # 将具体数据和图片所在路径包装成一个字典返回给前端
        data = {}
        data["data"] = result_list
        data["bar"] = "employee_stat_img/bar_" + employeeId + ".jpg"
        data["pie"] = "employee_stat_img/pie_" + employeeId + ".jpg"
        data["employee_name"] = employee_name
        return render(request, 'templates/employee3.html', data)
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


# 经理绩效分布的统计函数
def indexMDistSelect(request):  # 获取下拉框
    print("查询经理负责的任务")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'manager':
        manager_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select taskinfo.Task_id,taskcredit.Credit \
                        from taskinfo \
                        inner join taskcredit on taskcredit.Task_id = taskinfo.Task_id\
                        where Manager_id='%s'" % manager_id)
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"Task_id": r[0], 'Credit': r[1]})
        for i in range(0, len(result_list)):
            print("任务ID:%s" % (result_list[i]['Task_id']))
        return render(request, 'templates/manager4-1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def indexMDistShow(request):  # 获取下拉框和成绩统计分布的对应图片
    print("查询经理管理的项目以及该项目所有员工的绩效分布")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'manager':
        manager_id = request.session['id']
        task_id = request.POST.get('my_select')
        # 首先先将之前该经理对应项目的统计图片删掉
        picreg = "^[^_]*_" + manager_id + '_' + task_id + "\.jpg$"
        for pic in os.listdir("static/manager_stat_img/"):
            if re.match(picreg, pic) != None:
                os.remove("static/manager_stat_img/" + pic)
        # 先查询经理管理的所有任务信息
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select taskinfo.Task_id,taskcredit.Credit \
                        from taskinfo \
                        inner join taskcredit on taskcredit.Task_id = taskinfo.Task_id\
                        where taskinfo.Manager_id='%s'" % manager_id)
        result = cursor.fetchall()
        result_list = []
        task_name = ""
        for r in result:
            result_list.append({"task_id": r[0], 'credits': r[1]})
            # if r[0] == course_id:
            #     task_name = r[0]
        # 查询该项目的员工绩效分布
        cursor.execute("select taskcredit.Credit,count(Credit) as counts\
                        from taskcredit\
                        where Task_id=%s\
                        group by Credit;", [task_id])  # 根据具体课程id查询成绩分布
        grade_list = []
        result = cursor.fetchone()
        tmp = ('grade', 'counts')
        while result:
            grade_list.append(dict(zip(tmp, result)))
            result = cursor.fetchone()
        connection.close()
        for i in range(0, len(grade_list)):
            print("取得成绩:%d 对应次数:%d" % (grade_list[i]['grade'], grade_list[i]['counts']))
        num_list = [0, 0, 0, 0, 0, 0]
        label_list = ["0", "1", "2", "3", "4", "5"]
        color_list = ["royalblue", "darkcyan", "yellowgreen", "yellow", "orangered", "red"]
        for i in range(len(grade_list)):
            grade = grade_list[i]['grade']
            if grade == 0:
                num_list[0] += grade_list[i]['counts']
            elif grade == 1:
                num_list[1] += grade_list[i]['counts']
            elif grade == 2:
                num_list[2] += grade_list[i]['counts']
            elif grade == 3:
                num_list[3] += grade_list[i]['counts']
            elif grade == 4:
                num_list[4] += grade_list[i]['counts']
            else:
                num_list[5] += grade_list[i]['counts']
        # 柱状图
        plt.figure(figsize=(5, 5))
        plt.title('直方图')
        plt.xlabel('分数段')
        plt.ylabel('计数')
        if max(num_list) <= 5:
            plt.yticks(list(range(max(num_list) + 1)))
        plt.bar(range(len(num_list)), num_list, color=color_list, tick_label=label_list)
        plt.savefig("static/manager_stat_img/bar_" + manager_id + '_' + task_id + ".jpg")  # 图片拿教师id+课程id作为标识
        plt.close()
        # 饼图
        # 获得个数非0的成绩段（以及相应的label_list和color_list）
        pie_num_list, pie_label_list, pie_color_list = [], [], []
        for i in range(len(num_list)):
            if num_list[i] > 0:
                pie_num_list.append(num_list[i])
                pie_label_list.append(label_list[i])
                pie_color_list.append(color_list[i])
        plt.figure(figsize=(5.3, 5.3))
        plt.title('饼状图')
        plt.pie(pie_num_list, labels=pie_label_list, colors=pie_color_list, autopct='%1.2f%%',
                textprops={'fontsize': 12, 'color': 'black'})
        plt.axis('equal')
        plt.savefig("static/manager_stat_img/pie_" + manager_id + '_' + task_id + ".jpg")  # 图片拿教师id+课程id作为标识
        plt.close()
        #将经理负责的全部任务信息、该任务所有员工绩效分布的数据、图片所在路径包装成一个字典返回给前端
        data = {}
        data["taskinfo"] = result_list
        data["creditinfo"] = grade_list
        data["bar"] = "manager_stat_img/bar_" + manager_id + '_' + task_id + ".jpg"
        data["pie"] = "manager_stat_img/pie_" + manager_id + '_' + task_id + ".jpg"
        data["task_name"] = task_id
        return render(request, 'templates/manager4-2.html', data)
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')
