import re

import pymysql
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import time
# Create your views here.
from appdata.models import bankuser


def signin(request):
    # 用于登录
    if request.method == "POST":
        username = request.POST.get("username")
        passwd = request.POST.get("passwd")
        if username == "manager" and passwd == "yutao19981119":
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user=username,
                password=passwd,
                db='bank',
                charset='utf8'
            )
            # request.session['username'] = username
            # request.session['info'] = ""
            return redirect("/bank/admin")
    else:
        return render(request, "appdata/signin.html")

def admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        rignt = request.POST.get("right")
        table = request.POST.get("table")
        operate = request.POST.get("operate")
        # request.session['username'] = "manager"
        if operate == "check":
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user="manager",
                password="yutao19981119",
                db='bank',
                charset='utf8'
            )
            whom = []
            if (username != ""):  # 分隔开读取的用户字符串
                if (',' in username):
                    whom = username.split(',')
                else:
                    whom.append(username)
            temp1 = ""
            for w in whom:
                cursor = conn.cursor()  # 得到数据库的一个游标对象
                sql = "show grants for " + w + "@'localhost'" + ';'
                print(sql, "\n")  # 打印信息
                cursor.execute(sql)  # 数据库执行该sql语句
                # print(cursor)
                priv = []
                for i in cursor:
                    priv.append(tuple(re.split(r' TO ', str(*i))[0].split(r' ON ')))

                print(''.center(80, '~'))
                # print("用户", username)
                temp = "用户" + w + ":\n"
                for j in priv:
                    privs = j[0].replace('GRANT', '')
                    privs_info = j[1]
                    temp = temp + '{0} {1:<20} {2} {3}'.format('库(表):', privs_info, '权限:', privs) + "\n"
                    print('{0} {1:<20} {2} {3}'.format('库(表):', privs_info, '权限:', privs))
                print(''.center(80, '~'))
                print('\n')
                localtime = time.asctime(time.localtime(time.time()))
                journal = open('journal.txt', 'a')  # 写日志
                journal.write(sql + "        " + localtime + "\n")  # 写入日志
                conn.commit()  # 提交
                cursor.close()
                temp1 = temp1 + temp
            # request.session['info'] = temp1
            # return redirect("../admin")
            return render(request, "appdata/admin.html", {'username': "manager", 'data': temp1})

        if operate == "give":
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user="manager",
                password="yutao19981119",
                db='bank',
                charset='utf8'
            )
            whom = []
            allrignt = []
            if (username != ""):  # 分隔开读取的用户字符串
                if (',' in username):
                    whom = username.split(',')
                else:
                    whom.append(username)
            if (rignt!= ""):  # 分隔开读取的用户字符串
                if (',' in rignt):
                    allrignt = rignt.split(',')
                else:
                    allrignt.append(rignt)
            temp = ""
            for w in whom:
                for r in allrignt:
                    cursor = conn.cursor()  # 得到数据库的一个游标对象
                    sql = 'grant ' + r + ' on bank.' + table + ' to ' + w + "@'localhost'" + ';'  # 为每个用户赋予权限
                    print(sql, "\n")  # 打印信息
                    cursor.execute(sql)  # 数据库执行该sql语句
                    journal = open('journal.txt', 'a')  # 写日志
                    localtime = time.asctime(time.localtime(time.time()))
                    journal.write(sql + "        " + localtime + "\n")  # 写入日志
                    conn.commit()  # 提交
                    cursor.close()
                    temp = temp + sql + "\n"
            # request.session['info'] = temp
            # return redirect("../admin")
            return render(request, "appdata/admin.html", {'username': "manager", 'data': temp})

        if operate == "withdraw":
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user="manager",
                password="yutao19981119",
                db='bank',
                charset='utf8'
            )
            whom = []
            allrignt = []
            if (username != ""):  # 分隔开读取的用户字符串
                if (',' in username):
                    whom = username.split(',')
                else:
                    whom.append(username)
            if (rignt != ""):  # 分隔开读取的用户字符串
                if (',' in rignt):
                    allrignt = rignt.split(',')
                else:
                    allrignt.append(rignt)
            temp = ""
            for w in whom:
                for r in allrignt:
                    cursor = conn.cursor()  # 得到数据库的一个游标对象
                    sql = 'revoke ' + r + ' on bank.' + table + ' from ' + w + "@'localhost'" + ';'
                    print(sql, "\n")  # 打印信息
                    cursor.execute(sql)  # 数据库执行该sql语句
                    journal = open('journal.txt', 'a')  # 写日志
                    localtime = time.asctime(time.localtime(time.time()))
                    journal.write(sql + "        " + localtime + "\n")  # 写入日志
                    conn.commit()  # 提交
                    cursor.close()
                    temp = temp + sql + "\n"
            # request.session['info'] = temp
            # return redirect("../admin")
            return render(request, "appdata/admin.html", {'username': "manager", 'data': temp})
    return render(request, "appdata/admin.html", {'username': "manager", 'data': ""})