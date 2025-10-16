FROM python:3.9-buster

# RUN echo "deb https://mirrors.aliyun.com/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian-security/ buster/updates main contrib non-free" >> /etc/apt/sources.list


# RUN apt-get update && \
#     apt-get install -y gcc libc-dev libsasl2-dev libldap2-dev libssl-dev zip jq libgl1 && \
#     apt-get clean


RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/
RUN pip config set install.trusted-host artifact.enflame.cn
    
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY ./ /app/

CMD "python -m ai_phs_news workflow schdule_daily"
