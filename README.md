# 学生就业项目

**项目名称**：学生就业管理系统

**系统实现**：Django+ JQuery 

**运行环境**：Python3.12 + MySQL8.x

**开发工具**：PyCharm

**特别说明**：PyCharm 进行项目开发过程中，需要在工具中进行正确的虚拟环境设置，安装需要的依赖包，同时在本地计算机中也需要安装，也就是说在 PyCharm 虚拟环境中安装 Django、PyMySQL ，本地计算机中也需要使用 **pip install 依赖名称** 的方式安装Django、PyMySQL，或者pip install -r requirements.txt



## 1. 项目预览

![image-20240313122910563.png](https://bk.cyymzy.com/upload/image-20240313122910563.png)

用户登陆页

![image-20240313124355714.png](https://bk.cyymzy.com/upload/image-20240313124355714.png)

系统首页

![image-20240313124430131.png](https://bk.cyymzy.com/upload/image-20240313124430131.png)

数据展示页面

## 2. 项目设计

![image-20240313191543609.png](https://bk.cyymzy.com/upload/image-20240313191543609.png)

系统功能结构图



![image-20240313192815021.png](https://bk.cyymzy.com/upload/image-20240313192815021.png)

用户角色图

![image .png](https://bk.cyymzy.com/upload/image%20.png)

数据库ER图

## 3. 项目结构

![image-20240313133547565.png](https://bk.cyymzy.com/upload/image-20240313133547565.png)



## 4. 项目部署

### 4.1 环境要求



**Python:** 尽量选择 3.11的版本，测试项目代码在3.9以下的环境中运行会有部分代码不兼容

**MySQL:**具体使用版本没有要求，但是推荐8.0 mysql

### 4.2 运行流程

首先，按照 4.1 中的环境要求说明，完成 python、mysql 这些软件安装和配置，同时特别提醒，pycharm 运行项目，除了需要在虚拟环境中安装 Django、PyMySQL 这些依赖外，本地最好在安装 python之后使用  pip install 依赖名称 将这些依赖在本地环境中进行安装



第二，复制第5章数据库相关中找到数据库执行的SQL语句，这些SQL语句可以在命令窗口中执行，也可以在Navicat 等图形化管理窗口中执行，执行过程中请移除注释内容，避免对运行造成干扰，注意：数据库的创建可以复制创建库的语句，之后使用命令语句生成数据库表，最好执行SQL语句中插入的语句将测试数据添加到数据库中



第三，使用 PyCharm 打开项目，并且按照 4.3 中项目运行的相关说明，进行虚拟环境、运行的设置，同时在项目的 settings.py 文件中正确的配置数据库用户名和密码，完成这些之后，点击运行按钮就可以运行项目，项目成功启动之后，在浏览器中输入  http://127.0.0.1:8000/jobs/login ，就可以进入到项目登陆页面，在这个页面中输入账号 admin 密码 admin 就可以完成登陆了



## 5. 项目启动

### 5.1 数据库配置创建

 修改`djangoblog/setting.py` 修改数据库配置，如下所示：

```mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoblog',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 3306,
    }
}

#创建数据库
create schema student_jobs collate utf8mb4_0900_bin;
```



### 5.2 Django数据迁移，启动

然后在终端下执行如下命令:

```python
python manage.py makemigrations
python manage.py migrate


```

再执行： `python manage.py runserver`启动服务

浏览器打开: http://127.0.0.1:8000/  就可以看到效果了。  



## 服务器部署

本地安装部署请参考 [Django官方文档](https://docs.djangoproject.com/zh-hans/5.0/)
有详细的部署介绍.    

本项目已经支持使用docker来部署，如果你有docker环境那么可以使用docker来部署。

项目中有`docker file`,部署请参考 [Docker官方文档](https://www.docker.com/)



## 在线体验

访问https://jygl.cyymzy.com 可以看见预览效果

管理员账号：老师的教务系统账号

企业人员账号：admin，admin

学生账号：学生的教务系统账号



## 问题相关

有任何问题欢迎提Issue,或者将问题描述发送至我邮箱 `2403930241a@gmail.com`.我会尽快解答.推荐提交Issue方式.  

---

 ## 致大家🙋‍♀️🙋‍♂️

 如果本项目帮助到了你，请点亮`stars`，让更多的人看到。
您的小星星将会是我的动力。 
