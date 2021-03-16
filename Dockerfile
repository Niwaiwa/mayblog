# 使用官方的 Python 執行環境作為基本的 Docker 影像
FROM python:3.6-slim

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential

RUN cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime \
    && echo "Asia/Taipei" > /etc/timezone

# 安裝 requirements.txt 中所列的必要套件
COPY requirements.txt /
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# 複製目前目錄下的內容，放進 Docker 容器中的 /myapp
COPY . /myapp

# 設定工作目錄為 /myapp
WORKDIR /myapp

# ENV UWSGI_INI /myapp/uwsgi.ini

# 讓 5050 連接埠可以從 Docker 容器外部存取
EXPOSE 5000

# 當 Docker 容器啟動時，自動執行 index.py
# CMD ["python", "index.py"]
