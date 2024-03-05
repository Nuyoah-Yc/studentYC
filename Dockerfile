# 使用官方 Python 3.11 运行时作为父镜像
FROM python:3.11-rc-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 安装系统依赖，您可能需要的其他依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 将项目依赖复制到容器中
COPY requirements.txt /app/

# 安装项目依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 将项目代码复制到容器中
COPY . /app/


# 指定启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
