FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai

RUN apt-get update
RUN apt-get install -y tzdata
RUN echo ${TZ} > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install -y python3 python3-pip pkg-config libcairo2-dev

RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY ./MushroomDjango /MushroomDjango

WORKDIR /MushroomDjango

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh"]