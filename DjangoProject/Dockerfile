FROM python:3.8.10-alpine

RUN apk add --update make g++ python3-dev cairo-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./MushroomDjango /MushroomDjango

WORKDIR /MushroomDjango

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh"]