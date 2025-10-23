FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    gcc \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# 升级pip
RUN pip install --upgrade pip

# 复制requirements.txt并安装依赖
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ .

# 确保日志目录存在
RUN mkdir -p static/log static/uploads static/backupdb

EXPOSE 8081

# 默认命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8081"]