from django.db import models

class Colleges(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('学院名称',  max_length=32, null=False)
    createTime = models.CharField('建立时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'colleges'

class Majors(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('专业名称',  max_length=32, null=False)
    createTime = models.CharField('建立时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'majors'

class Companies(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('企业名称', max_length=30, null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=64, null=False)
    class Meta:
        db_table = 'companies'

class Jobs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('岗位名称', max_length=30, null=False)
    duty = models.CharField('岗位职责', max_length=125, null=False)
    ask = models.CharField('岗位要求', max_length=125, null=False)
    company = models.ForeignKey(Companies, db_column='company_id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'jobs'

class Users(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', db_column='pass_word', max_length=32, null=False)
    name = models.CharField('用户姓名', max_length=20, null=False)
    gender = models.CharField('用户性别', max_length=4, null=False)
    age = models.IntegerField('用户年龄', null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    type = models.IntegerField('用户身份', null=False)
    class Meta:
        db_table = 'users'

class Students(models.Model):
    id = models.CharField('学生学号', max_length=20, primary_key=True)
    address = models.CharField('学生籍贯', max_length=64, null=False)
    birthday = models.CharField('出生日期', max_length=10, null=False)
    status = models.IntegerField('学生状态', null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE, db_column='college_id')
    major = models.ForeignKey(Majors, on_delete=models.CASCADE, db_column='major_id')
    class Meta:
        db_table = 'students'

class EducationLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('学校名称', max_length=20, null=False)
    startTime = models.CharField('开始时间', max_length=10, null=False)
    endTime = models.CharField('结束时间', max_length=10, null=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='student_id')
    class Meta:
        db_table = 'education_logs'

class ProjectLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('项目名称', max_length=20, null=False)
    duty = models.CharField('工作职责', max_length=64, null=False)
    detail = models.CharField('项目详情', max_length=64, null=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='student_id')
    class Meta:
        db_table = 'project_logs'

class SendLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    snedTime = models.CharField('发送时间', db_column='sned_time', max_length=19, null=False)
    status = models.IntegerField('处理状态', null=False)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, db_column='job_id')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='student_id')
    class Meta:
        db_table = 'send_logs'  #