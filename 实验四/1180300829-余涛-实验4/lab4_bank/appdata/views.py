import re

import pymysql
from django.shortcuts import render, redirect
import time
from appdata.models import bankuser


def signin(request):
    # 用于登录
    if request.method == "POST":
        username = request.POST.get("username")
        passwd = request.POST.get("passwd")
        if username == "manager" and passwd == "yutao19981119":  # 分配权限的管理员
            # request.session['username'] = username
            # request.session['info'] = ""
            return redirect("/bank/admin")
        else:
            user = bankuser.objects.get(username=username)
            if user.passwd == passwd:
                if user.isadmin == 0:
                    journal = open('journal.txt', 'a')  # 写日志
                    localtime = time.asctime(time.localtime(time.time()))
                    journal.write(localtime+" 用户"+user.username+"从主登录页面登录\n")  # 写入日志
                    return redirect("/bank/users/"+username)
                if user.isadmin == 1:
                    journal = open('journal.txt', 'a')  # 写日志
                    localtime = time.asctime(time.localtime(time.time()))
                    journal.write(localtime+" 中级管理员" + user.username + "从主登录页面登录\n")  # 写入日志
                    return redirect("/bank/middlemanager_look/"+username)
                if user.isadmin == 2:
                    journal = open('journal.txt', 'a')  # 写日志
                    localtime = time.asctime(time.localtime(time.time()))
                    journal.write(localtime+" 顶级管理员" + user.username + "从主登录页面登录\n")  # 写入日志
                    return redirect("/bank/topmanager_look/"+username)
    else:
        return render(request, "appdata/signin.html")


def admin(request):
    # 权限管理员页面的后端处理
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


def users(request, username):
    # 用户和管理员页面的后端处理
    if request.method == "POST":
        money = request.POST.get("money")
        operate = request.POST.get("operate")
        request.session["money"] = money
        request.session["operate"] = operate
        user = bankuser.objects.get(username=username)
        journal = open('journal.txt', 'a')  # 写日志
        localtime = time.asctime(time.localtime(time.time()))
        journal.write(localtime+" 用户" + user.username + "请求为" + operate + ",金额为" + money + "\n")  # 写入日志
        return redirect("/bank/rightsignin/"+username)
    user = bankuser.objects.get(username=username)
    currency = user.currency
    request.session["currency"] = currency
    return render(request, "appdata/users.html", {'username': username, 'currency': currency})


def rightsignin(request, username):
    # 管理员登录的处理
    if request.method == "POST":
        name = request.POST.get("name")
        passwd = request.POST.get("passwd")
        money = request.session.get("money")
        user = bankuser.objects.get(username=name)
        if user.passwd == passwd:
            if user.isadmin == 1:  # 中级管理员
                if int(money) <= 100000:
                    journal = open('journal.txt', 'a')  # 写日志
                    localtime = time.asctime(time.localtime(time.time()))
                    journal.write(localtime+" 中级管理员登录了处理请求页面\n")  # 写入日志
                    return redirect("/bank/middlemanager/" + username)
                else:
                    return redirect("/bank/error/" + username)
            if user.isadmin == 2:  # 顶级管理员
                journal = open('journal.txt', 'a')  # 写日志
                localtime = time.asctime(time.localtime(time.time()))
                journal.write(localtime + " 顶级管理员登录了处理请求页面\n")  # 写入日志
                return redirect("/bank/topmanager/" + username)
    money = request.session.get("money")
    operate = request.session.get("operate")
    currency = request.session.get("currency")
    return render(request, "appdata/rightsignin.html", {'username': username, 'money': money, 'operate': operate, 'currency': currency})

def error(request, username):
    return render(request, "appdata/error.html")

def middlemanager(request, username):
    # 中级管理员处理请求页面
    if request.method == "POST":
        money = request.session.get("money")
        operate = request.session.get("operate")
        manageroperate = request.POST.get("manageroperate")
        if manageroperate == "agree":  # 管理员同意
            if operate == "recharge":
                user = bankuser.objects.get(username=username)
                money = int(money)
                user.currency = user.currency + money
                user.save()
                journal = open('journal.txt', 'a')  # 写日志
                localtime = time.asctime(time.localtime(time.time()))
                journal.write(localtime+" 中级管理员同意了" + user.username + "请求为" + operate + ",金额为" + str(money) + "的请求，请求已执行\n")  # 写入日志
                return redirect("/bank/users/" + username)
            if operate == "withdraw":
                user = bankuser.objects.get(username=username)
                money = int(money)
                user.currency = user.currency - money
                user.save()
                journal = open('journal.txt', 'a')  # 写日志
                localtime = time.asctime(time.localtime(time.time()))
                journal.write(localtime+" 中级管理员同意了" + user.username + "请求为" + operate + ",金额为" + str(money) + "的请求，请求已执行\n")  # 写入日志
                return redirect("/bank/users/" + username)
        elif manageroperate == "deny":  # 管理员拒绝
            user = bankuser.objects.get(username=username)
            journal = open('journal.txt', 'a')  # 写日志
            localtime = time.asctime(time.localtime(time.time()))
            journal.write(localtime+" 中级管理员拒绝了" + user.username + "请求为" + operate + ",金额为" + money + "的请求\n")  # 写入日志
            return redirect("/bank/users/" + username)
    money = request.session.get("money")
    operate = request.session.get("operate")
    return render(request, "appdata/middlemanager.html", {'username': username, 'money': money, 'operate': operate})


def topmanager(request, username):
    # 顶级管理员处理请求页面
    if request.method == "POST":
        money = request.session.get("money")
        operate = request.session.get("operate")
        manageroperate = request.POST.get("manageroperate")
        if manageroperate == "agree":  # 管理员同意
            if operate == "recharge":
                user = bankuser.objects.get(username=username)
                money = int(money)
                user.currency = user.currency + money
                user.save()
                journal = open('journal.txt', 'a')  # 写日志
                localtime = time.asctime(time.localtime(time.time()))
                journal.write(localtime+" 顶级管理员同意了" + user.username + "请求为" + operate + ",金额为" + str(money) + "的请求，请求已执行\n")  # 写入日志
                request.session.clear()
                return redirect("/bank/users/" + username)
            if operate == "withdraw":
                user = bankuser.objects.get(username=username)
                money = int(money)
                user.currency = user.currency - money
                user.save()
                journal = open('journal.txt', 'a')  # 写日志
                localtime = time.asctime(time.localtime(time.time()))
                journal.write(localtime+" 顶级管理员同意了" + user.username + "请求为" + operate + ",金额为" + str(money) + "的请求，请求已执行\n")  # 写入日志
                request.session.clear()
                return redirect("/bank/users/" + username)
        elif manageroperate == "deny":  # 管理员拒绝
            user = bankuser.objects.get(username=username)
            journal = open('journal.txt', 'a')  # 写日志
            localtime = time.asctime(time.localtime(time.time()))
            journal.write(localtime+" 顶级管理员拒绝了" + user.username + "请求为" + operate + ",金额为" + money + "的请求\n")  # 写入日志
            return redirect("/bank/users/" + username)
    money = request.session.get("money")
    operate = request.session.get("operate")
    return render(request, "appdata/topmanager.html", {'username': username, 'money': money, 'operate': operate})


def middlemanager_look(request, username):
    # 中级管理员登录后页面
    journal = open('journal.txt', 'a')  # 写日志
    localtime = time.asctime(time.localtime(time.time()))
    journal.write(localtime + " 中级管理员查看了所有用户余额\n")  # 写入日志
    currency_list = bankuser.objects.all()
    return render(request, "appdata/middlemanager_look.html", {'username': username, 'currency_list': currency_list})


def topmanager_look(request, username):
    # 顶级管理员登录后页面
    journal = open('journal.txt', 'a')  # 写日志
    localtime = time.asctime(time.localtime(time.time()))
    journal.write(localtime + " 顶级管理员查看了所有用户余额\n")  # 写入日志
    currency_list = bankuser.objects.all()
    return render(request, "appdata/topmanager_look.html", {'username': username, 'currency_list': currency_list})


