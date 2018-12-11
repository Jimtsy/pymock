FROM python:3.6-alpine

WORKDIR /pymock
VOLUME /pymock/logs
ADD . /pymock/
RUN pip install --no-cache -U -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt