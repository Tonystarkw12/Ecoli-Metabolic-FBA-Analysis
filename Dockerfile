# 使用Python 3.9 slim基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量（避免Python缓存文件）
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 复制项目文件
COPY . /app

# 安装依赖（使用清华镜像源加速）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 创建必要的目录
RUN mkdir -p data results

# 设置容器启动命令
CMD ["python", "src/main.py"]

# 容器端口（未来扩展Web界面时使用）
EXPOSE 8080

# 作者信息
LABEL maintainer="zhou-zh23@mails.tsinghua.edu.cn"
LABEL description="E. coli Metabolic FBA Analysis Tool"
LABEL version="1.0.0"