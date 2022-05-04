FROM ubuntu:20.04

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
# RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN sed -i "s/archive.ubuntu.com/mirrors.163.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get install -y python3 python3-pip

RUN useradd -m rank

WORKDIR /rank

COPY ./requirements.txt /requirements.txt

RUN python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r /requirements.txt

CMD exec su rank -c "python3 -u main.py 2>err 1>out"

EXPOSE 9031
