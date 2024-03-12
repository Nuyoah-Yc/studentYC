import base64
import json
import re
import time
from django.db import IntegrityError
import requests
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from app import models


# 定向到登录页面
def login(request):
    return HttpResponseRedirect('/jobs/login/')




'''
基础处理类，其他处理继承这个类
'''
class BaseView(View):
    '''
    检查指定的参数是否存在
    存在返回 True
    不存在返回 False
    '''
    def isExit(param):

        if (param == None) or (param == ''):
            return False
        else:
            return True

    '''
    转换分页查询信息
    '''
    def parasePage(pageIndex, pageSize, pageTotal, count, data):

        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    转换分页查询信息
    '''
    def parasePage(pageIndex, pageSize, pageTotal, count, data):
        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    成功响应信息
    '''
    def success(msg='处理成功'):
        resl = {'code': 0, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    成功响应信息, 携带数据
    '''
    def successData(data, msg='处理成功'):
        resl = {'code': 0, 'msg': msg, 'data': data}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统警告信息
    '''
    def warn(msg='操作异常，请重试'):
        resl = {'code': 1, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统异常信息
    '''
    def error(msg='系统异常'):
        resl = {'code': 2, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')


'''
系统请求处理
'''
class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'login':
            return render(request, 'login.html')

        elif module == 'exit':

            del request.session["user"]
            del request.session["type"]

            return HttpResponseRedirect('/jobs/login')

        if module == 'info':

            return SysView.getSessionInfo(request)

        elif module == 'show':

            return render(request, 'index.html')

        elif module == 'sysNum':

            return SysView.getSysNums(request)

    def post(self, request, module, *args, **kwargs):

        if module == 'login':

            return SysView.jwxt_login(request)

        if module == 'info':
            return SysView.updSessionInfo(request)

        if module == 'pwd':
            return SysView.updSessionPwd(request)

    def jwxt_login(request):
        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')
        qygly = models.Users.objects.filter(userName=userName)
        if (qygly.exists()):
            user = qygly.first()
            if user.passWord == passWord:
                request.session["user"] = user.id
                request.session['type'] = user.type
                return SysView.success()
        url = 'https://api.cyymzy.com/items/login'
        rsp = requests.post(url, data={'username': userName, 'password': passWord})
        resl = rsp.json()
        if resl['message'] == '登录成功':
            gender = resl['gender']
            age = 18  # 你可以在这里指定年龄
            phone = resl['phone'] if resl['type'] == '教师' else '88888888'
            user_type = 0 if resl['type'] == '教师' else 2

            user_instance = models.Users.objects.create(
                userName=userName,
                passWord=passWord,
                name=resl['name'],
                gender=gender,
                age=age,
                phone=phone,
                type=user_type
            )

            request.session['user'] = user_instance.id
            request.session['type'] = user_instance.type

            if user_type == 2:  # 学生
                college = models.Colleges.objects.get(name=resl['college'])  # 确保数据库中有这个学院
                major = models.Majors.objects.get(name=resl['major'])  # 确保数据库中有这个专业

                student, created = models.Students.objects.get_or_create(
                    id=resl['id'],
                    defaults={
                        'user': user_instance,
                        'address': '无',  # 或从 resl 中提取，如果API有返回
                        'birthday': '无',  # 或从 resl 中提取，如果API有返回
                        'status': 0,  # 需要根据实际逻辑提供正确的状态值
                        'college': college,
                        'major': major,
                        # 根据需要添加其他字段的默认值
                    }
                )

                if not created:
                    # 如果学生记录已经存在，则根据需要更新它
                    # 例如，更新学生的状态或其他信息
                    student.status = 1  # 或根据实际情况更新状态
                    student.save()
                # request.session['user'] = user_instance.id
                # request.session['type'] = user_instance.type
            return SysView.success(resl['message'])
        else:
            SysView.warn(resl['message'])

        return SysView.warn(resl['message'])

    # def login(request):

    #     userName = request.POST.get('userName')
    #     passWord = request.POST.get('passWord')
    #
    #     user = models.Users.objects.filter(userName=userName)  # 查询用户是否存在
    #     if (user.exists()):  # 用户存在
    #         user = user.first()
    #         if user.passWord == passWord:
    #             request.session["user"] = user.id
    #             request.session["type"] = user.type
    #
    #             return SysView.success()
    #         else:
    #             return SysView.warn('用户密码输入错误')
    #     else:
    #         return SysView.warn('用户名输入错误')

    def getSessionInfo(request):

        user = request.session.get('user')

        data = models.Users.objects.filter(id=user)

        resl = {}
        for item in data:
            resl = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'gender': item.gender,
                'name': item.name,
                'age': item.age,
                'phone': item.phone,
                'type': item.type,
            }

        return SysView.successData(resl)

    def getSysNums(request):

        resl = {
            'companiesTotal' : models.Companies.objects.all().count(),
            'jobTotal' : models.Jobs.objects.all().count(),
            'inStuTotal' : models.Students.objects.filter(status=0).count(),
            'outStuTotal' : models.Students.objects.filter(status=1).count()
        }

        return BaseView.successData(resl)

    def updSessionInfo(request):

        user = request.session.get('user')

        models.Users.objects.filter(id=user).update(
            userName=request.POST.get('userName'),
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            phone=request.POST.get('phone'),
        )

        return SysView.success()

    def updSessionPwd(request):

        user = request.session.get('user')

        models.Users.objects.filter(id=user).update(
            passWord=request.POST.get('password'),
        )

        return SysView.success()

'''
学院信息管理
'''
class CollegesView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'colleges.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Colleges.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'createTime': data.createTime
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Colleges.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self,request):

        models.Colleges.objects.create(name=request.POST.get('name'),
                                       createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                      )

        return BaseView.success()

    def updInfo(self, request):

        models.Colleges.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    def delInfo(self, request):

        if models.Students.objects.filter(college__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Colleges.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
专业信息管理
'''
class MajorsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'majors.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Majors.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'createTime': data.createTime,
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Majors.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        models.Majors.objects.create(name=request.POST.get('name'),
                                       createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                       )

        return BaseView.success()

    def updInfo(self, request):

        models.Majors.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    def delInfo(self, request):

        if models.Students.objects.filter(major__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Majors.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
企业信息管理
'''
class CompaniesView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'companies.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Companies.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'phone': data.phone,
            'address': data.address,
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Companies.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'phone': item.phone,
                'address': item.address,
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        models.Companies.objects.create(id=int(time.time()),
                                        name=request.POST.get('name'),
                                        phone=request.POST.get('phone'),
                                        address=request.POST.get('address')
                                        )
        return BaseView.success()

    def updInfo(self, request):

        models.Companies.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address')
        )
        return BaseView.success()

    def delInfo(self, request):

        if models.Jobs.objects.filter(company__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Companies.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
岗位信息管理
'''
class JobsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':

            companies = models.Companies.objects.all().values()

            return render(request, 'jobs.html', {'companies': list(companies)})
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Jobs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'duty': data.duty,
            'ask': data.ask,
            'companyId': data.company.id,
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        companyId = request.GET.get('companyId')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        if BaseView.isExit(companyId):
            qruery = qruery & Q(company__id=companyId)

        data = models.Jobs.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'duty': item.duty,
                'ask': item.ask,
                'companyId': item.company.id,
                'companyName': item.company.name
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        models.Jobs.objects.create(name=request.POST.get('name'),
                                    duty=request.POST.get('duty'),
                                    ask=request.POST.get('ask'),
                                    company=models.Companies.objects.get(id=request.POST.get('companyId'))
                                    )
        return BaseView.success()

    def updInfo(self, request):

        models.Jobs.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name'),
            duty=request.POST.get('duty'),
            ask=request.POST.get('ask'),
            company=models.Companies.objects.get(id=request.POST.get('companyId'))
        )
        return BaseView.success()

    def delInfo(self, request):

        if models.SendLogs.objects.filter(job__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Jobs.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
用户信息管理
'''
class UsersView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'users.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Users.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'userName': data.userName,
            'passWord': data.passWord,
            'name': data.name,
            'gender': data.gender,
            'age': data.age,
            'phone': data.phone,
            'type': data.type
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')
        phone = request.GET.get('phone')

        qruery = Q(type = 1);

        if BaseView.isExit(userName):
            qruery = qruery & Q(userName__contains=userName)

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        if BaseView.isExit(phone):
            qruery = qruery & Q(phone__contains=phone)

        data = models.Users.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'type': item.type
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        models.Users.objects.create(
                                    userName=request.POST.get('userName'),
                                    passWord=request.POST.get('passWord'),
                                    name=request.POST.get('name'),
                                    gender=request.POST.get('gender'),
                                    age=request.POST.get('age'),
                                    phone=request.POST.get('phone'),
                                    type=request.POST.get('type'),
                                    )
        return BaseView.success()

    def updInfo(self, request):

        models.Users.objects.filter(id=request.POST.get('id')) \
            .update(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone'),
        )
        return BaseView.success()

    def delInfo(self, request):

        models.Users.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()

'''
学生信息管理
'''
class StudentsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':

            colleges = models.Colleges.objects.all().values()
            majors = models.Majors.objects.all().values()

            return render(request, 'students.html', {'colleges': list(colleges), 'majors': list(majors)})
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Students.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'address': data.address,
            'birthday': data.birthday,
            'status': data.status,
            'collegeId': data.college.id,
            'majorId': data.major.id,
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        collegeId = request.GET.get('collegeId')
        majorId = request.GET.get('majorId')

        qruery = Q();

        if BaseView.isExit(userName):
            qruery = qruery & Q(user__userName__contains=userName)

        if BaseView.isExit(name):
            qruery = qruery & Q(user__name__contains=name)

        if BaseView.isExit(phone):
            qruery = qruery & Q(user__phone__contains=phone)

        if BaseView.isExit(collegeId):
            qruery = qruery & Q(college__id=collegeId)

        if BaseView.isExit(majorId):
            qruery = qruery & Q(major__id=majorId)

        data = models.Students.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):

            temp = {
                'id': item.id,
                'address': item.address,
                'birthday': item.birthday,
                'status': item.status,
                'collegeId': item.college.id,
                'collegeName': item.college.name,
                'majorId': item.major.id,
                'majorName': item.major.name,
                'userName': item.user.userName,
                'name': item.user.name,
                'gender': item.user.gender,
                'age': item.user.age,
                'phone': item.user.phone,
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        user = models.Users.objects.create(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone'),
            type=request.POST.get('type')
        )

        models.Students.objects.create(
            id=request.POST.get('id'),  #
            address=request.POST.get('address'),
            birthday=request.POST.get('birthday'),
            status=request.POST.get('status'),
            college=models.Colleges.objects.get(id=request.POST.get('collegeId')),
            major=models.Majors.objects.get(id=request.POST.get('majorId')),
            user=user
        )

        return BaseView.success()

    def updInfo(self, request):

        models.Students.objects.filter(id=request.POST.get('id')) \
            .update(
            address=request.POST.get('address'),
            birthday=request.POST.get('birthday'),
            college=models.Colleges.objects.get(id=request.POST.get('collegeId')),
            major=models.Majors.objects.get(id=request.POST.get('majorId'))
        )

        return BaseView.success()

    def delInfo(self, request):

        student = models.Students.objects.filter(id=request.POST.get('id')).first()

        print(request.GET.get('id'), student);
        models.Users.objects.filter(id=student.user.id).delete()
        models.EducationLogs.objects.filter(student__id=student.id).delete()
        models.ProjectLogs.objects.filter(student__id=student.id).delete()
        models.SendLogs.objects.filter(student__id=student.id).delete()

        student.delete()

        return BaseView.success()

'''
教育经历管理
'''
class EducationLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'educationLogs.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo( request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.EducationLogs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'startTime': data.startTime,
            'endTime': data.endTime,
            'studentId': data.student.id,
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        type = request.session.get('type')
        user = request.session.get('user')

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        studentName = request.GET.get('studentName')

        qruery = Q();

        if type == 2:
            student = models.Students.objects.filter(user__id=user).first()
            qruery = qruery & Q(student__id=student.id)

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        if BaseView.isExit(studentName):
            qruery = qruery & Q(student__user__name__contains=studentName)

        if type == 2:
            data = models.EducationLogs.objects.filter(qruery).order_by("-startTime")
            paginator = Paginator(data, pageSize)
        else:
            data = models.EducationLogs.objects.filter(qruery).order_by("student_id")
            paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'startTime': item.startTime,
                'endTime': item.endTime,
                'studentId': item.student.id,
                'studentName': item.student.user.name,
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        user = request.session.get('user')

        models.EducationLogs.objects.create(name=request.POST.get('name'),
                                    startTime=request.POST.get('startTime'),
                                    endTime=request.POST.get('endTime'),
                                    student=models.Students.objects.filter(user__id=user).first()
                                    )
        return BaseView.success()

    def updInfo(self, request):

        models.EducationLogs.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name'),
            startTime=request.POST.get('startTime'),
            endTime=request.POST.get('endTime'),
        )
        return BaseView.success()

    def delInfo(self, request):

        models.EducationLogs.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()

'''
项目经历管理
'''
class ProjectLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'projectLogs.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo( request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.ProjectLogs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'duty': data.duty,
            'detail': data.detail,
            'studentId': data.student.id,
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        type = request.session.get('type')
        user = request.session.get('user')

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        studentName = request.GET.get('studentName')

        qruery = Q();

        if type == 2:
            student = models.Students.objects.filter(user__id=user).first()
            qruery = qruery & Q(student__id=student.id)

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        if BaseView.isExit(studentName):
            qruery = qruery & Q(student__user__name__contains=studentName)

        data = models.ProjectLogs.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'duty': item.duty,
                'detail': item.detail,
                'studentId': item.student.id,
                'studentName': item.student.user.name,
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        user = request.session.get('user')

        models.ProjectLogs.objects.create(name=request.POST.get('name'),
                                        duty=request.POST.get('duty'),
                                        detail=request.POST.get('detail'),
                                        student=models.Students.objects.filter(user__id=user).first()
                                        )
        return BaseView.success()

    def updInfo(self, request):

        models.ProjectLogs.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name'),
            duty=request.POST.get('duty'),
            detail=request.POST.get('detail'),
        )
        return BaseView.success()

    def delInfo(self, request):

        models.ProjectLogs.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()

'''
投递记录管理
'''
class SendLogs(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'sendLogs.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.SendLogs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'snedTime': data.snedTime,
            'status': data.status,
            'jobId': data.job.id,
            'studentId': data.student.id,
        }

        return self.successData(resl)

    def getPageInfo(self, request):

        type = request.session.get('type')
        user = request.session.get('user')

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        jobName = request.GET.get('jobName')
        studentName = request.GET.get('studentName')

        qruery = Q();

        if type == 2:
            student = models.Students.objects.filter(user__id=user).first()
            qruery = qruery & Q(student__id=student.id)

        if BaseView.isExit(jobName):
            qruery = qruery & Q(job__name__contains=jobName)

        if BaseView.isExit(studentName):
            qruery = qruery & Q(student__user__name__contains=studentName)

        data = models.SendLogs.objects.filter(qruery).order_by("-snedTime")
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'snedTime': item.snedTime,
                'status': item.status,
                'jobId': item.job.id,
                'jobName': item.job.name,
                'jobDuty': item.job.duty,
                'companyName': item.job.company.name,
                'studentId': item.student.id,
                'studentName': item.student.user.name,
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self, request):

        user = request.session.get('user')
        jobId = request.POST.get('jobId')
        student = models.Students.objects.filter(user__id=user).first()

        qruery = Q();

        qruery = qruery & Q(job__id=jobId)
        qruery = qruery & Q(student__id=student.id)

        if ((models.EducationLogs.objects.filter(student__id=student.id).exists()) &
                (models.ProjectLogs.objects.filter(student__id=student.id).exists())):

            if models.SendLogs.objects.filter(qruery).exists():

                return BaseView.warn('已投递，请勿重复')
            else:

                models.SendLogs.objects.create(status=request.POST.get('status'),
                                                  snedTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                  student=student,
                                                  job=models.Jobs.objects.filter(id=jobId).first()
                                                  )
                return BaseView.success()
        else:

            return BaseView.warn('完善个人项目和教育经历后才可投递简历')

    def updInfo(self, request):

        status = request.POST.get('status')

        if  int(status) == 1:

            sendLog =  models.SendLogs.objects.filter(id=request.POST.get('id')).first()

            student = models.Students.objects.filter(id=sendLog.student.id).first()

            if student.status == 0:

                models.SendLogs.objects.filter(id=request.POST.get('id')).update(
                    status=request.POST.get('status'),
                )

                models.Students.objects.filter(id=sendLog.student.id) \
                    .update(
                    status=1,
                )

                return BaseView.success()
            else:

                return BaseView.warn('学生已被录取')

        else:
            models.SendLogs.objects.filter(id=request.POST.get('id')) \
                .update(
                status=request.POST.get('status'),
            )
            return BaseView.success()

    def delInfo(self, request):

        models.SendLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()
